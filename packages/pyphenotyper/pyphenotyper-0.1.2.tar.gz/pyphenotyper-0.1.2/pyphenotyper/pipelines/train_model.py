from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import Model

from pyphenotyper.utils.metrics import f1, iou


def train_model(model: Model, train_generator, val_generator, train_count, val_count, epochs: int, checkpoint_path: str,
                patience: int, optimizer):
    """
    Trains the model with the option to save checkpoints after every epoch and
    stop early if no improvement is seen in the validation loss.

    Args:
        model (Model): The Keras model to train.
        train_generator: Generator for training data.
        val_generator: Generator for validation data.
        train_count: Number of samples of train_generator divided by the batch_size
        val_count: Number of samples of val_generator divided by the batch_size
        epochs (int): Number of epochs to train.
        checkpoint_path (str): Path where the checkpoint will be saved.
        patience (int): Number of epochs with no improvement after which training will be stopped.
        optimizer: Optimizer to use for training.
    """
    # Set up the model checkpoint callback to save the model after every epoch
    model_checkpoint_callback = ModelCheckpoint(
        filepath=checkpoint_path,
        save_weights_only=True,
        save_best_only=False,
        verbose=1)

    # Set up early stopping to halt the training when validation loss is not improving
    early_stopping_callback = EarlyStopping(
        monitor='val_loss',
        patience=patience,
        verbose=1,
        restore_best_weights=True)

    # Compile the model
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy', f1, iou])

    # Start training
    history = model.fit(
        train_generator,
        epochs=epochs,
        steps_per_epoch=train_count,
        validation_data=val_generator,
        validation_steps=val_count,
        callbacks=[model_checkpoint_callback, early_stopping_callback],
        verbose=1)

    return history
