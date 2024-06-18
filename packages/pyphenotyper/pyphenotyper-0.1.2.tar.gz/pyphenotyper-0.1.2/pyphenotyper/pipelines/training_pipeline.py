import os
import typer
import shutil
from pyphenotyper.utils.metrics import f1, iou
from model import unet_model
from train_model import train_model
from plotting import plot_loss, plot_iou
from keras.optimizers import Adam, SGD, RMSprop
from data_generators import create_generators
from keras.models import load_model
from data_prep_pipeline import main as data_prep_main

app = typer.Typer()


def move_files(src_dir: str, dst_dir: str):
    """
    Move files from the source directory to the destination directory.
    """
    for file_name in os.listdir(src_dir):
        src_path = os.path.join(src_dir, file_name)
        dst_path = os.path.join(dst_dir, file_name)
        shutil.move(src_path, dst_path)


def copy_files(src_dir: str, dst_dir: str):
    """
    Copy files from the source directory to the destination directory.
    """
    for file_name in os.listdir(src_dir):
        src_path = os.path.join(src_dir, file_name)
        dst_path = os.path.join(dst_dir, file_name)
        shutil.copy2(src_path, dst_path)


def validate_checkpoint_path(checkpoint_path: str):
    if not os.path.isfile(checkpoint_path):
        typer.echo(f"The checkpoint file '{checkpoint_path}' does not exist.")
        raise typer.Exit()


def validate_data_folders(patch_dir: str):
    required_dirs = [
        'train_images/train', 'train_masks/train',
        'val_images/val', 'val_masks/val',
        'test_images/test', 'test_masks/test'
    ]
    missing_dirs = [d for d in required_dirs if not os.path.isdir(os.path.join(patch_dir, d))]
    if missing_dirs:
        typer.echo(
            f"The directory '{patch_dir}' is missing the following required subdirectories: {', '.join(missing_dirs)}.")
        raise typer.Exit()


@app.command()
def main(
        patch_size: int = 256,
        batch_size: int = 32,
        epochs: int = 2,
        patience: int = 10,
        learning_rate: float = 0.001,
        optimizer_name: str = 'adam',
        checkpoint_dir: str = 'checkpoints',
        continue_training: bool = False,
        checkpoint_path: str = ''
):
    # Ensure checkpoint directory exists
    os.makedirs(checkpoint_dir, exist_ok=True)

    # Create checkpoint path with hyperparameters in the name
    checkpoint_path_template = os.path.join(checkpoint_dir,
                                            f'model_lr_{learning_rate}_opt_{optimizer_name}_epoch_{{epoch:02d}}.h5')

    # Ask the user if they want to train from scratch
    train_from_scratch = typer.confirm("Do you want to train from scratch?")

    if train_from_scratch:
        typer.echo("Would you like to train from scratch:")
        typer.echo("1. With only pre-prepared data?")
        typer.echo("2. With only your own data?")
        typer.echo("3. With your own data + the pre-prepared data?")

        choice = typer.prompt("Please enter 1, 2, or 3")

        if choice == '1':
            # Use the default patch directory for pre-prepared data
            patch_dir = 'data_patched_final'

        elif choice == '2':
            # Ask if the user has already passed their data through the data preparation pipeline
            run_data_prep = typer.confirm("Have you already passed your data through the data preparation pipeline?")

            if not run_data_prep:
                # Prompt the user for image and mask folder paths for data preparation
                image_folder = typer.prompt("Enter the path to the folder containing images")
                masks_folder = typer.prompt("Enter the path to the folder containing masks")

                # Run the data preparation pipeline
                data_prep_main(image_folder=image_folder, masks_folder=masks_folder)

            # Prompt the user for the directory containing the prepared data
            patch_dir = typer.prompt("Enter the path to the folder containing the prepared data patches")
            validate_data_folders(patch_dir)

        elif choice == '3':
            # Ask if the user has already passed their data through the data preparation pipeline
            run_data_prep = typer.confirm("Have you already passed your data through the data preparation pipeline?")

            if not run_data_prep:
                # Prompt the user for image and mask folder paths for data preparation
                image_folder = typer.prompt("Enter the path to the folder containing images")
                masks_folder = typer.prompt("Enter the path to the folder containing masks")

                # Run the data preparation pipeline
                data_prep_main(image_folder=image_folder, masks_folder=masks_folder)

            # Prompt the user for the directory containing the prepared data
            patch_dir = typer.prompt("Enter the path to the folder containing the prepared data patches")
            validate_data_folders(patch_dir)

            # Move test data to train data
            move_files(os.path.join(patch_dir, 'test_images/test'), os.path.join(patch_dir, 'train_images/train'))
            move_files(os.path.join(patch_dir, 'test_masks/test'), os.path.join(patch_dir, 'train_masks/train'))

            # Copy pre-prepared data to user's data
            pre_prepared_dir = 'data_patched_final'
            copy_files(os.path.join(pre_prepared_dir, 'train_images/train'),
                       os.path.join(patch_dir, 'train_images/train'))
            copy_files(os.path.join(pre_prepared_dir, 'train_masks/train'),
                       os.path.join(patch_dir, 'train_masks/train'))
            copy_files(os.path.join(pre_prepared_dir, 'val_images/val'), os.path.join(patch_dir, 'val_images/val'))
            copy_files(os.path.join(pre_prepared_dir, 'val_masks/val'), os.path.join(patch_dir, 'val_masks/val'))
            copy_files(os.path.join(pre_prepared_dir, 'test_images/test'), os.path.join(patch_dir, 'test_images/test'))
            copy_files(os.path.join(pre_prepared_dir, 'test_masks/test'), os.path.join(patch_dir, 'test_masks/test'))

        else:
            typer.echo("Invalid choice. Please enter 1, 2, or 3.")
            raise typer.Exit()

        # Initialize Model
        model = unet_model((patch_size, patch_size, 1))

    else:
        typer.echo("Would you like to train:")
        typer.echo("1. From a model checkpoint?")
        typer.echo("2. From a pre-trained model?")

        choice = typer.prompt("Please enter 1 or 2")

        if choice == '1':
            # Prompt the user for the checkpoint path
            checkpoint_path = typer.prompt("Enter the path to the model checkpoint")
            validate_checkpoint_path(checkpoint_path)

            # Ask how to continue training
            typer.echo("Would you like to continue training with:")
            typer.echo("1. The pre-prepared data?")
            typer.echo("2. Your own data?")
            typer.echo("3. Your own data + the pre-prepared data?")

            data_choice = typer.prompt("Please enter 1, 2, or 3")

            if data_choice == '1':
                patch_dir = 'data_patched_w_extra_labels'

            elif data_choice == '2':
                typer.echo(
                    "WARNING: Make sure you passed your own data through the data pipeline before training with it.")
                patch_dir = typer.prompt("Enter the path to the folder containing the prepared data patches")
                validate_data_folders(patch_dir)

            elif data_choice == '3':
                typer.echo(
                    "WARNING: Make sure you passed your own data through the data pipeline before training with it.")
                patch_dir = typer.prompt("Enter the path to the folder containing the prepared data patches")
                validate_data_folders(patch_dir)

                # Move test data to train data
                move_files(os.path.join(patch_dir, 'test_images/test'), os.path.join(patch_dir, 'train_images/train'))
                move_files(os.path.join(patch_dir, 'test_masks/test'), os.path.join(patch_dir, 'train_masks/train'))

                # Copy pre-prepared data to user's data
                pre_prepared_dir = 'data_patched_w_extra_labels'
                copy_files(os.path.join(pre_prepared_dir, 'train_images/train'),
                           os.path.join(patch_dir, 'train_images/train'))
                copy_files(os.path.join(pre_prepared_dir, 'train_masks/train'),
                           os.path.join(patch_dir, 'train_masks/train'))
                copy_files(os.path.join(pre_prepared_dir, 'val_images/val'), os.path.join(patch_dir, 'val_images/val'))
                copy_files(os.path.join(pre_prepared_dir, 'val_masks/val'), os.path.join(patch_dir, 'val_masks/val'))
                copy_files(os.path.join(pre_prepared_dir, 'test_images/test'),
                           os.path.join(patch_dir, 'test_images/test'))
                copy_files(os.path.join(pre_prepared_dir, 'test_masks/test'),
                           os.path.join(patch_dir, 'test_masks/test'))

            else:
                typer.echo("Invalid choice. Please enter 1, 2, or 3.")
                raise typer.Exit()

            # Load the model architecture
            model = unet_model((patch_size, patch_size, 1))

            # Load the weights
            print(f"Loading model from {checkpoint_path}")
            model.load_weights(checkpoint_path)

        elif choice == '2':
            # Step 1: Ask for the model location
            model_path = typer.prompt("Enter the path to the pre-trained model")
            if not os.path.isfile(model_path):
                typer.echo(f"The model file '{model_path}' does not exist.")
                raise typer.Exit()

            # Step 2: Ask for the location of the new data patches
            typer.echo("WARNING: Make sure you passed your own data through the data pipeline before training with it.")
            patch_dir = typer.prompt("Enter the path to the folder containing the prepared data patches")
            validate_data_folders(patch_dir)

            # Step 3: Load the data and the model
            print(f"Loading model from {model_path}")
            model = load_model(model_path, custom_objects={'f1': f1, 'iou': iou})

            # Adjust the learning rate for incremental learning
            learning_rate = typer.prompt(
                f"Enter the learning rate for incremental learning (default is {learning_rate / 10}): ",
                default=learning_rate / 10, type=float)

    # Choose optimizer
    if optimizer_name == 'adam':
        optimizer = Adam(learning_rate=learning_rate)
    elif optimizer_name == 'sgd':
        optimizer = SGD(learning_rate=learning_rate)
    elif optimizer_name == 'rmsprop':
        optimizer = RMSprop(learning_rate=learning_rate)
    else:
        raise ValueError(f"Unsupported optimizer: {optimizer_name}")

    # Create Data Generators
    train_gen, val_gen, test_gen, (train_count, val_count, test_count) = create_generators(patch_dir, patch_size,
                                                                                           batch_size)

    # Train the Model
    history = train_model(model, train_gen, val_gen, train_count, val_count, epochs, checkpoint_path_template, patience,
                          optimizer)

    model.save('best_model.h5')

    # Plotting the training metrics
    plot_loss(history)
    plot_iou(history)


if __name__ == "__main__":
    app()
