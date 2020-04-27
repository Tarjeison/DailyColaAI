import torch
from torch import nn, utils
from torch.autograd.variable import Variable
from torchvision import transforms, datasets

from generation.GAN.GAN_utils import noise, images_to_vectors, vectors_to_images
from generation.GAN.discriminator import DiscriminatorNet
from generation.GAN.generator import GeneratorNet
from utils.logger import Logger


def train_gan(model_name: str, data_name: str) -> None:
    # Load data
    data = datasets.ImageFolder(root='data/images/pre_processed/', transform=transforms.Compose([
        transforms.Grayscale(), transforms.ToTensor()
    ]))
    # Create loader with data, so that we can iterate over it
    data_loader = torch.utils.data.DataLoader(data, batch_size=30, shuffle=True)
    # Num batches
    num_batches = len(data_loader)
    discriminator = DiscriminatorNet()
    generator = GeneratorNet()
    loss = nn.BCELoss()
    num_test_samples = 1
    test_noise = noise(num_test_samples)

    # Create logger instance
    logger = Logger(model_name=model_name, data_name=data_name)
    # Total number of epochs to train
    num_epochs = 100
    for epoch in range(num_epochs):
        for n_batch, (real_batch, _) in enumerate(data_loader):
            N = real_batch.size(0)
            # 1. Train Discriminator
            real_data = Variable(images_to_vectors(real_batch))
            # Generate fake data and detach
            # (so gradients are not calculated for generator)
            fake_data = generator(noise(N)).detach()
            # Train D
            d_error, d_pred_real, d_pred_fake = \
                discriminator.train_discriminator(real_data, fake_data, loss)

            # 2. Train Generator
            fake_data = generator(noise(N))
            # Train G
            g_error = generator.train_generator(fake_data, discriminator, loss)
            # Log batch error
            logger.log(d_error, g_error, epoch, n_batch, num_batches)
            # Display Progress every few batches
            if epoch % 10 == 0 and n_batch == 0:
                test_images = vectors_to_images(generator(test_noise))
                test_images = test_images.data
                logger.log_images(
                    test_images, num_test_samples,
                    epoch, n_batch, num_batches
                )
                # Display status Logs
                logger.display_status(
                    epoch, num_epochs, n_batch, num_batches,
                    d_error, g_error, d_pred_real, d_pred_fake
                )

            # Dummy exit condition
            if epoch == 100:
                return
