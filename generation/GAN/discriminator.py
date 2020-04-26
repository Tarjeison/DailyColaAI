import torch
from torch import nn, optim

from generation.GAN.GAN_utils import ones_target, zeros_target


class DiscriminatorNet(torch.nn.Module):
    """
    A three hidden-layer discriminative neural network
    """
    optimizer: torch.optim.Adam

    def __init__(self, lr=0.0002):
        super(DiscriminatorNet, self).__init__()
        n_features = 65536
        n_out = 1

        self.hidden0 = nn.Sequential(
            nn.Linear(n_features, 512),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3)
        )
        self.hidden1 = nn.Sequential(
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3)
        )
        self.hidden2 = nn.Sequential(
            nn.Linear(256, 64),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3)
        )
        self.out = nn.Sequential(
            torch.nn.Linear(64, n_out),
            torch.nn.Sigmoid()
        )

        self.optimizer = optim.Adam(self.parameters(), lr=lr)

    def forward(self, x):
        x = self.hidden0(x)
        x = self.hidden1(x)
        x = self.hidden2(x)
        x = self.out(x)
        return x

    def train_discriminator(self, real_data: torch.Tensor,
                            fake_data: torch.Tensor, loss: nn.BCELoss):
        N = real_data.size(0)
        # Reset gradients
        self.optimizer.zero_grad()

        # 1.1 Train on Real Data
        prediction_real = self(real_data)
        # Calculate error and backpropagate
        error_real = loss(prediction_real, ones_target(N))
        error_real.backward()

        # 1.2 Train on Fake Data
        prediction_fake = self(fake_data)
        # Calculate error and backpropagate
        error_fake = loss(prediction_fake, zeros_target(N))
        error_fake.backward()

        # 1.3 Update weights with gradients
        self.optimizer.step()

        # Return error and predictions for real and fake inputs
        return error_real + error_fake, prediction_real, prediction_fake
