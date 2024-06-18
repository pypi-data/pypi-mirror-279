import logging
import os
import re
import shutil
from typing import List, Tuple

import cv2
import numpy as np
import typer

from pyphenotyper.data.data_processing import roi_extraction_coords_direct, padder, \
    patch_image

# Set up logging
logging.basicConfig(
    filename='data_preparation.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = typer.Typer()


def validate_folder(folder: str, folder_type: str) -> List[str]:
    """
    Validate if all files in the folder are .png and if the names between the files in both folders match.

    :param folder: Path to the folder to be validated.
    :param folder_type: Type of the folder (image or mask).
    :return: List of .png files in the folder.
    :raises typer.Exit: If the folder does not exist or does not contain any .png files.
    """
    if not os.path.isdir(folder):
        logging.error(f"The {folder_type} folder '{folder}' does not exist.")
        typer.echo(f"The {folder_type} folder '{folder}' does not exist.")
        raise typer.Exit()

    files = [f for f in os.listdir(folder) if f.endswith('.png')]
    if not files:
        logging.error(f"The {folder_type} folder '{folder}' does not contain any .png files.")
        typer.echo(f"\n\nThe {folder_type} folder '{folder}' does not contain any .png files.")
        raise typer.Exit()

    logging.info(f"Validated {folder_type} folder: {folder} with {len(files)} .png files.")
    return files


def create_folder_structure(base_path: str) -> None:
    """
    Create the folder structure for train, validation, and test sets.

    :param base_path: Base path where the folder structure will be created.
    """
    folders = [
        'test_images/test', 'test_masks/test',
        'train_images/train', 'train_masks/train',
        'val_images/val', 'val_masks/val'
    ]
    for folder in folders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)
        logging.info(f"Created folder: {os.path.join(base_path, folder)}")


def split_data(files: List[str], train_ratio: float, val_ratio: float) -> Tuple[List[str], List[str], List[str]]:
    """
    Split data into train, validation, and test sets.

    :param files: List of files to be split.
    :param train_ratio: Proportion of files to be used for training.
    :param val_ratio: Proportion of files to be used for validation.
    :return: Three lists containing filenames for train, validation, and test sets respectively.
    """
    np.random.shuffle(files)  # Shuffle the files list to ensure random distribution
    total = len(files)
    train_count = int(total * train_ratio)
    val_count = int(total * val_ratio)

    train_files = files[:train_count]
    val_files = files[train_count:train_count + val_count]
    test_files = files[train_count + val_count:]

    logging.debug(
        f"Data split into {len(train_files)} train, {len(val_files)} validation, and {len(test_files)} test files.")
    return train_files, val_files, test_files


def copy_files(files: List[str], src_folder: str, dest_folder: str) -> None:
    """
    Copy files from source folder to destination folder.

    :param files: List of filenames to be copied.
    :param src_folder: Source folder path.
    :param dest_folder: Destination folder path.
    """
    for file_name in files:
        src_path = os.path.join(src_folder, file_name)
        dest_path = os.path.join(dest_folder, file_name)
        shutil.copy2(src_path, dest_path)  # Use shutil.copy2 to copy file metadata as well
        logging.info(f"Copied {file_name} from {src_folder} to {dest_folder}")


def normalize_masks(mask_folder: str) -> None:
    """
    Normalize mask files to be binary (0 and 1). If they are between 0 and 255, they are divided by 255.

    :param mask_folder: Path to the folder containing mask files.
    """
    for file_name in os.listdir(mask_folder):
        file_path = os.path.join(mask_folder, file_name)
        mask = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            logging.error(f"Failed to read the mask file {file_name}.")
            typer.echo(f"\n\nFailed to read the mask file {file_name}.")
            raise typer.Exit()

        if np.max(mask) > 1:
            mask = mask / 255.0  # Normalize mask to be between 0 and 1
            mask = (mask > 0.5).astype(np.uint8)  # Binarize the mask
            cv2.imwrite(file_path, mask)  # Save the normalized mask
            logging.debug(f"Normalized mask file {file_name}")


def pad_and_save(folder: str, patch_size: int) -> None:
    """
    Pad images to the specified patch size and save them.

    :param folder: Path to the folder containing images or masks to be padded.
    :param patch_size: Size of the patches to pad to.
    """
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        image = cv2.imread(file_path, 0)
        padded_image = padder(image, patch_size)
        cv2.imwrite(file_path, padded_image)
        logging.debug(f"Padded and saved {file_name} in {folder}")


def patch_and_save(folder: str, patch_size: int) -> None:
    """
    Patch images into smaller patches and save them.

    :param folder: Path to the folder containing images or masks to be patched.
    :param patch_size: Size of the patches.
    """
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        image = cv2.imread(file_path, 0)
        patches, patches_shape = patch_image(image, patch_size)
        base_name = os.path.splitext(file_name)[0]
        for i, patch in enumerate(patches):
            patch_file_name = f"{base_name}_patch_{i + 1}.png"
            patch_file_path = os.path.join(folder, patch_file_name)
            cv2.imwrite(patch_file_path, patch.squeeze())
            logging.debug(f"Patched and saved {patch_file_name} in {folder}")


def validate_and_cleanup(images_folder: str, masks_folder: str) -> None:
    """
    Validate that image and mask files match and clean up padded images.

    :param images_folder: Path to the folder containing images.
    :param masks_folder: Path to the folder containing masks.
    """
    image_files = set(os.path.splitext(f)[0] for f in os.listdir(images_folder))
    mask_files = set(os.path.splitext(f)[0] for f in os.listdir(masks_folder))

    if image_files != mask_files:
        logging.error(f"Mismatch between image and mask files in {images_folder} and {masks_folder}.")
        typer.echo(f"\n\nMismatch between image and mask files in {images_folder} and {masks_folder}.")
        raise typer.Exit()

    # Only delete the full padded images, not the patches
    patch_pattern = re.compile(r'.+_patch_\d+\.png$')

    for file_name in os.listdir(images_folder):
        if not patch_pattern.match(file_name):
            os.remove(os.path.join(images_folder, file_name))
            logging.debug(f"Deleted padded image {file_name} from {images_folder}")

    for file_name in os.listdir(masks_folder):
        if not patch_pattern.match(file_name):
            os.remove(os.path.join(masks_folder, file_name))
            logging.debug(f"Deleted padded mask {file_name} from {masks_folder}")


@app.command()
def main(
        image_folder: str = typer.Argument(..., help="Path to the folder containing images"),
        masks_folder: str = typer.Argument(..., help="Path to the folder containing masks")
) -> Tuple[str, str, str, str, str, str]:
    """
    Main function to process images and masks.

    :param image_folder: Path to the folder containing images.
    :param masks_folder: Path to the folder containing masks.
    :return: Paths to the directories containing the processed train, validation, and test sets.
    """
    typer.echo("The data is being thoroughly checked...")
    logging.info("Starting data validation...")

    # Validate image and masks folders
    image_files = validate_folder(image_folder, 'image')
    mask_files = validate_folder(masks_folder, 'mask')

    # Check if the number of files match
    if len(image_files) != len(mask_files):
        logging.error("The number of files in the image and mask folders do not match.")
        typer.echo("\n\nThe number of files in the image and mask folders do not match.")
        raise typer.Exit()

    # Check if the filenames match
    image_filenames = set(os.path.splitext(f)[0] for f in image_files)
    mask_filenames = set(os.path.splitext(f)[0] for f in mask_files)

    if image_filenames != mask_filenames:
        logging.error("The filenames in the image and mask folders do not match.")
        typer.echo("\n\nThe filenames in the image and mask folders do not match.")
        raise typer.Exit()

    # Check if there are enough images (minimum 10)
    if len(image_files) < 10:
        logging.error("There are not enough images to perform the split (minimum 10 required).")
        typer.echo("\n\nThere are not enough images to perform the split (minimum 10 required).")
        raise typer.Exit()

    # Normalize masks
    normalize_masks(masks_folder)

    logging.info("All tests passed!")
    typer.echo("\nAll tests passed!")

    # Ask user if they want to crop the images
    crop = typer.confirm(
        "Would you like to crop your images? \nWARNINGs: \nIf you decide to crop them, you should check the directory of the images and your masks to check that the cropping was done correctly.\n If you are running this within the training pipeline you should choose to crop the image")

    if crop:
        cropped_image_folder = f"{image_folder}_cropped"
        cropped_masks_folder = f"{masks_folder}_cropped"
        os.makedirs(cropped_image_folder, exist_ok=True)
        os.makedirs(cropped_masks_folder, exist_ok=True)

        for file_name in image_files:
            image_path = os.path.join(image_folder, file_name)
            mask_path = os.path.join(masks_folder, file_name)

            original_image = cv2.imread(image_path, 0)
            original_mask = cv2.imread(mask_path, 0)

            coords = roi_extraction_coords_direct(original_image)

            y1, y2, x1, x2 = coords
            if y1 < y2 and x1 < x2:
                cropped_image = original_image[y1:y2, x1:x2]
                cropped_mask = original_mask[y1:y2, x1:x2]

                cropped_image_path = os.path.join(cropped_image_folder, file_name)
                cropped_mask_path = os.path.join(cropped_masks_folder, file_name)

                cv2.imwrite(cropped_image_path, cropped_image)
                cv2.imwrite(cropped_mask_path, cropped_mask)

                logging.info(f"Cropped and saved {file_name} to {cropped_image_folder} and {cropped_masks_folder}")

        typer.echo(
            f"\n\nCropped images and masks have been saved in '{cropped_image_folder}' and '{cropped_masks_folder}' respectively.")

    # Step 1: Create folder structure
    base_path = os.path.dirname(image_folder)
    create_folder_structure(base_path)

    # Step 2: Split data
    train_files, val_files, test_files = split_data(image_files, 0.6, 0.2)

    # Paths to the directories containing the split data
    train_image_dir = os.path.join(base_path, 'train_images/train')
    train_mask_dir = os.path.join(base_path, 'train_masks/train')
    val_image_dir = os.path.join(base_path, 'val_images/val')
    val_mask_dir = os.path.join(base_path, 'val_masks/val')
    test_image_dir = os.path.join(base_path, 'test_images/test')
    test_mask_dir = os.path.join(base_path, 'test_masks/test')

    # Copy the files to their respective directories
    copy_files(train_files, cropped_image_folder if crop else image_folder, train_image_dir)
    copy_files(train_files, cropped_masks_folder if crop else masks_folder, train_mask_dir)
    copy_files(val_files, cropped_image_folder if crop else image_folder, val_image_dir)
    copy_files(val_files, cropped_masks_folder if crop else masks_folder, val_mask_dir)
    copy_files(test_files, cropped_image_folder if crop else image_folder, test_image_dir)
    copy_files(test_files, cropped_masks_folder if crop else masks_folder, test_mask_dir)

    typer.echo("\n\nImages and masks have been divided and copied to their respective folders.")
    logging.info("Images and masks have been divided and copied to their respective folders.")

    # Step 4: Pad images and masks
    patch_size = typer.prompt("\n\nPlease enter the desired patch size for training (256 or 512): ", type=int)

    if patch_size not in [256, 512]:
        logging.error("Invalid patch size. Please enter either 256 or 512.")
        typer.echo("\nInvalid patch size. Please enter either 256 or 512.")
        raise typer.Exit()

    for folder in [train_image_dir, train_mask_dir, val_image_dir, val_mask_dir, test_image_dir, test_mask_dir]:
        pad_and_save(folder, patch_size)

    typer.echo("\n\nImages and masks have been padded.")
    logging.info("Images and masks have been padded.")

    # Step 5: Patch images and masks
    for folder in [train_image_dir, train_mask_dir, val_image_dir, val_mask_dir, test_image_dir, test_mask_dir]:
        patch_and_save(folder, patch_size)

    # Step 6: Ensure all files in matching folders have the same name and delete padded images
    for img_folder, mask_folder in zip(
            [train_image_dir, val_image_dir, test_image_dir],
            [train_mask_dir, val_mask_dir, test_mask_dir]
    ):
        validate_and_cleanup(img_folder, mask_folder)

    typer.echo("\n\nPatching complete and padded images cleaned up.")
    logging.info("Patching complete and padded images cleaned up.")


if __name__ == "__main__":
    app()
