import torch
import torchvision
from torch.utils.data import DataLoader
from torchvision import transforms, datasets


def sample_data(path, batch_size, image_size, n_channels):
    transform = transforms.Compose(
        [
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5,) * n_channels, (1,) * n_channels),
        ]
    )

    dataset = datasets.ImageFolder(path, transform=transform)
    loader = DataLoader(dataset, shuffle=True, batch_size=batch_size, num_workers=8)
    loader = iter(loader)

    while True:
        try:
            yield next(loader)

        except StopIteration:
            loader = DataLoader(
                dataset, shuffle=True, batch_size=batch_size, num_workers=4
            )
            loader = iter(loader)
            yield next(loader)


def memory_mnist(batch_size, image_size, n_channels):
    transform = transforms.Compose(
        [
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5,) * n_channels, (1,) * n_channels),
        ]
    )
    train_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST(
            "~/datasets/mnist/", train=True, download=True, transform=transform
        ),
        batch_size=batch_size,
        shuffle=True,
    )

    loader = iter(train_loader)

    while True:
        try:
            yield next(loader)

        except StopIteration:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.MNIST(
                    "~/datasets/mnist/", train=True, download=True, transform=transform
                ),
                batch_size=batch_size,
                shuffle=True,
            )
            loader = iter(train_loader)
            yield next(loader)


def memory_fashion(batch_size, image_size, n_channels):
    transform = transforms.Compose(
        [
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5,) * n_channels, (1,) * n_channels),
        ]
    )
    train_loader = torch.utils.data.DataLoader(
        torchvision.datasets.FashionMNIST(
            "~/datasets/fashion_mnist/", train=True, download=True, transform=transform
        ),
        batch_size=batch_size,
        shuffle=True,
    )

    loader = iter(train_loader)

    while True:
        try:
            yield next(loader)

        except StopIteration:
            train_loader = torch.utils.data.DataLoader(
                torchvision.datasets.FashionMNIST(
                    "~/datasets/fashion_mnist/", train=True, download=True,
                    transform=transform
                ),
                batch_size=batch_size,
                shuffle=True,
            )
            loader = iter(train_loader)
            yield next(loader)
