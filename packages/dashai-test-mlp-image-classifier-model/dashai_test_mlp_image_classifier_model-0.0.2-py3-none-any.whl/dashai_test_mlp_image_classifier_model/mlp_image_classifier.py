import datasets
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data
from torch.utils.data import DataLoader
from torchvision import transforms

from DashAI.back.core.schema_fields import BaseSchema, int_field, schema_field
from DashAI.back.models.base_model import BaseModel
from DashAI.back.models.image_classification_model import ImageClassificationModel


class MLPImageClassifierSchema(BaseSchema):
    epochs: schema_field(
        int_field(ge=1),
        placeholder=10,
        description=(
            "The number of epochs to train the model. An epoch is a full iteration over "
            "the training data. It must be an integer greater or equal than 1"
        ),
    )  # type: ignore


class ImageDataset(torch.utils.data.Dataset):
    def __init__(self, dataset: datasets.Dataset):
        self.dataset = dataset
        self.transforms = transforms.Compose(
            [
                transforms.Resize((30, 30)),
                transforms.ToTensor(),
            ]
        )

        column_names = list(self.dataset.features.keys())
        self.image_col_name = column_names[0]
        if len(column_names) > 1:
            self.label_col_name = column_names[1]
        else:
            self.label_col_name = None
        self.tensor_shape = self.transforms(self.dataset[0][self.image_col_name]).shape

    def num_classes(self):
        if self.label_col_name is None:
            return 0
        label_column = self.dataset[self.label_col_name]
        return len(set(label_column))

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        if self.label_col_name is None:
            image = self.dataset[idx][self.image_col_name]
            image = self.transforms(image)
            return image
        image = self.dataset[idx][self.image_col_name]
        image = self.transforms(image)
        label = self.dataset[idx][self.label_col_name]
        return image, label


class MLP(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)
        self.relu = nn.ReLU()

    def forward(self, input: torch.Tensor):
        batch_size = input.shape[0]
        x = input.view(batch_size, -1)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def fit_model(
    model: nn.Module,
    train_loader: DataLoader,
    epochs: int,
    criterion: nn.Module,
    optimizer: optim.Optimizer,
    device: torch.device,
):
    model.train()
    for epoch in range(epochs):
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    return model


def predict(
    model: nn.Module,
    dataloader: DataLoader,
    device: torch.device,
):
    model.eval()
    probs_predicted = []
    with torch.no_grad():
        for images in dataloader:
            images = images.to(device)
            output_probs: torch.Tensor = model(images)
            probs_predicted += output_probs.tolist()
    return probs_predicted


class MLPImageClassifier(ImageClassificationModel, BaseModel):

    SCHEMA = MLPImageClassifierSchema

    def __init__(self, epochs: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.epochs = epochs
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    def fit(self, x: datasets.Dataset, y: datasets.Dataset):
        dataset = datasets.Dataset.from_dict(
            {
                "image": x["image"],
                "label": y["label"],
            }
        )
        image_dataset = ImageDataset(dataset)
        input_dim = (
            image_dataset.tensor_shape[0]
            * image_dataset.tensor_shape[1]
            * image_dataset.tensor_shape[2]
        )
        output_dim = image_dataset.num_classes()
        train_loader = DataLoader(image_dataset, batch_size=32, shuffle=True)
        self.model = MLP(input_dim, output_dim).to(self.device)
        if output_dim == 2:
            self.criteria = nn.BCEWithLogitsLoss()
        else:
            self.criteria = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.005)
        self.model = fit_model(
            self.model,
            train_loader,
            self.epochs,
            self.criteria,
            self.optimizer,
            self.device,
        )

    def predict(self, x: datasets.Dataset):
        image_dataset = ImageDataset(x)
        test_loader = DataLoader(image_dataset, batch_size=32, shuffle=False)
        probs = predict(self.model, test_loader, self.device)
        return probs

    def save(self, filename: str) -> None:
        """Save the model in the specified path."""
        torch.save(self.model, filename)

    @staticmethod
    def load(filename: str) -> None:
        """Load the model of the specified path."""
        model = torch.load(filename)
        return model
