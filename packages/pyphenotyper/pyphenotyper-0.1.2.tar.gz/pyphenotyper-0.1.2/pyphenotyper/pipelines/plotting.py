import plotly.graph_objects as go
import plotly.offline as pyo


def plot_loss(history):
    """
    Plots the training and validation loss from the training history.

    :param history: The training history object, which contains 'loss' and 'val_loss' keys.
    :type history: keras.callbacks.History or similar

    This function creates an interactive line plot of the training and validation loss
    over epochs using Plotly. It also saves the plot to an HTML file.
    """
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(loss) + 1)
    epochs_list = list(epochs)  # Convert range to list

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epochs_list, y=loss, mode='lines', name='Training Loss'))
    fig.add_trace(go.Scatter(x=epochs_list, y=val_loss, mode='lines', name='Validation Loss'))

    fig.update_layout(title='Training and Validation Loss',
                      xaxis_title='Epoch',
                      yaxis_title='Loss',
                      legend=dict(x=0, y=1, traceorder='normal'))
    fig.show()

    # Save the plot as an HTML file
    pyo.plot(fig, filename='training_validation_loss.html')


def plot_iou(history):
    """
    Plots the training and validation IoU (Intersection over Union) from the training history.

    :param history: The training history object, which contains 'iou' and 'val_iou' keys.
    :type history: keras.callbacks.History or similar

    This function creates an interactive line plot of the training and validation IoU
    over epochs using Plotly. It also saves the plot to an HTML file.
    """
    iou = history.history['iou']
    val_iou = history.history['val_iou']

    epochs = range(1, len(iou) + 1)
    epochs_list = list(epochs)  # Convert range to list

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epochs_list, y=iou, mode='lines', name='Training IoU'))
    fig.add_trace(go.Scatter(x=epochs_list, y=val_iou, mode='lines', name='Validation IoU'))

    fig.update_layout(title='Training and Validation IoU',
                      xaxis_title='Epoch',
                      yaxis_title='IoU',
                      legend=dict(x=0, y=1, traceorder='normal'))
    fig.show()

    # Save the plot as an HTML file
    pyo.plot(fig, filename='training_validation_iou.html')
