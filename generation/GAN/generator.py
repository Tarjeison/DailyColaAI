import torch
from torch import nn

from generation.GAN.GAN_utils import ones_target


class GeneratorNet(torch.nn.Module):
    """
    A three hidden-layer generative neural network
    """

    optimizer: torch.optim.Adam

    def __init__(self, lr=0.0002):
        super(GeneratorNet, self).__init__()
        n_features = 32
        n_out = 65536

        self.hidden0 = nn.Sequential(
            nn.Linear(n_features, 512),
            nn.LeakyReLU(0.2)
        )
        self.hidden1 = nn.Sequential(
            nn.Linear(512, 1024),
            nn.LeakyReLU(0.2)
        )
        self.hidden2 = nn.Sequential(
            nn.Linear(1024, 2048),
            nn.LeakyReLU(0.2)
        )

        self.out = nn.Sequential(
            nn.Linear(2048, n_out),
            nn.Tanh()
        )

        self.optimizer = torch.optim.Adam(self.parameters(), lr=lr)

    def forward(self, x):
        x = self.hidden0(x)
        x = self.hidden1(x)
        x = self.hidden2(x)
        x = self.out(x)
        return x

    def train_generator(self, fake_data, discriminator, loss):
        N = fake_data.size(0)
        # Reset gradients
        self.optimizer.zero_grad()
        # Sample noise and generate fake data
        prediction = discriminator(fake_data)
        # Calculate error and backpropagate
        error = loss(prediction, ones_target(N))
        error.backward()
        # Update weights with gradients
        self.optimizer.step()
        # Return error
        return error
