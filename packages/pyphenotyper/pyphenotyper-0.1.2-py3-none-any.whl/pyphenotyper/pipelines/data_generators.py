import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def create_generators(patch_dir: str, patch_size: int, batch_size: int):
    """
    Creates training, validation, and testing data generators.

    Args:
        patch_dir (str): Directory containing patched images and masks.
        patch_size (int): The desired patch size.
        batch_size (int): The batch size for the generators.

    Returns:
        tuple: Training, validation, and testing generators.
    """
    # Data augmentation for the training set
    train_image_datagen = ImageDataGenerator(
        rescale=1. / 255,
        horizontal_flip=True
    )

    train_image_generator = train_image_datagen.flow_from_directory(
        os.path.join(patch_dir, 'train_images'),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        class_mode=None,
        color_mode='grayscale',
        seed=42
    )

    train_image_count = train_image_generator.samples // batch_size

    train_mask_datagen = ImageDataGenerator(
        horizontal_flip=True
    )

    train_mask_generator = train_mask_datagen.flow_from_directory(
        os.path.join(patch_dir, 'train_masks'),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        class_mode=None,
        color_mode='grayscale',
        seed=42
    )

    train_generator = zip(train_image_generator, train_mask_generator)

    # Validation set
    val_image_datagen = ImageDataGenerator(
        rescale=1. / 255,
        horizontal_flip=True
    )

    val_image_generator = val_image_datagen.flow_from_directory(
        os.path.join(patch_dir, 'val_images'),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        class_mode=None,
        color_mode='grayscale',
        seed=42
    )

    val_image_count = val_image_generator.samples // batch_size

    val_mask_datagen = ImageDataGenerator(
        horizontal_flip=True
    )

    val_mask_generator = val_mask_datagen.flow_from_directory(
        os.path.join(patch_dir, 'val_masks'),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        class_mode=None,
        color_mode='grayscale',
        seed=42
    )

    val_generator = zip(val_image_generator, val_mask_generator)

    # Testing set
    test_image_datagen = ImageDataGenerator(rescale=1. / 255)

    test_image_generator = test_image_datagen.flow_from_directory(
        os.path.join(patch_dir, 'test_images'),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        class_mode=None,
        color_mode='grayscale',
        seed=42
    )

    test_image_count = test_image_generator.samples // batch_size

    test_mask_datagen = ImageDataGenerator()

    test_mask_generator = test_mask_datagen.flow_from_directory(
        os.path.join(patch_dir, 'test_masks'),
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        class_mode=None,
        color_mode='grayscale',
        seed=42
    )

    test_generator = zip(test_image_generator, test_mask_generator)

    return train_generator, val_generator, test_generator, (train_image_count, val_image_count, test_image_count)
