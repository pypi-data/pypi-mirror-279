import logging
import os

import typer
from keras.models import load_model

from data_generators import create_generators
from pyphenotyper.utils.metrics import f1, iou

# Create a Typer app
app = typer.Typer()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.command()
def main(
        patch_size: int = typer.Option(256, help="Patch size for image segmentation"),
        batch_size: int = typer.Option(32, help="Batch size for data generators"),
        model_path: str = typer.Option("root_4_ss.h5", help="Path to the model file")
) -> None:
    """
    Evaluate UNet model on test data using specified model parameters.

    :param patch_size: Patch size for image segmentation.
    :param batch_size: Batch size for data generators.
    :param model_path: Path to the model file.
    :return: None
    """
    # Set TensorFlow log level to minimize logs
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # Constants
    PATCH_DIR = 'data_patched_final'

    # Create data generators
    logger.info("\nCreating data generators...")
    train_gen, val_gen, test_gen, (train_count, val_count, test_count) = create_generators(PATCH_DIR, patch_size,
                                                                                           batch_size)
    logger.info("Data generators created successfully.")

    # Load the best model saved during training, providing custom metrics
    logger.info("\nLoading model...")
    model = load_model(model_path, custom_objects={'f1': f1, 'iou': iou})
    logger.info(f"Model loaded from {model_path}.")

    # Evaluate the model on the test set
    logger.info("\nEvaluating model on test data...")
    score = model.evaluate(test_gen, steps=test_count)
    logger.info("\nModel evaluation completed.")

    # Print the evaluation metrics
    logger.info(f'\nTest Loss: {score[0]}')
    logger.info(f'Test Accuracy: {score[1]}')
    logger.info(f'Test F1 Score: {score[2]}')
    logger.info(f'Test IoU: {score[3]}')


if __name__ == "__main__":
    app()
