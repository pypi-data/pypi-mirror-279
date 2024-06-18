import tensorflow as tf
class trueloss:
  """comments"""
  def __init__(self, model, loss_after = 'epoch', plots = 1):
      self.model = model
      self.loss_after = loss_after

  def fit(self, *args, **kwargs):
    kwargs = self.prepare_input(*args, **kwargs)
    history = self.model.fit(**kwargs)
    return history

  def prepare_input(self, *args, **kwargs):
    #input standadized with callback added.
    params = {'x' : None,
            'y':None,
            'batch_size':None,
            'epochs':1,
            'verbose':'auto',
            'callbacks':None,
            'validation_split':0.0,
            'validation_data':None,
            'shuffle':True, 'class_weight':None,
            'sample_weight':None, 'initial_epoch':0,
            'steps_per_epoch':None,
            'validation_steps':None,
            'validation_batch_size':None,
            'validation_freq':1,
            'max_queue_size':10,
            'workers':1,
            'use_multiprocessing':False}
    if len(args)>0:
      if isinstance(args[0], (tf.data.Dataset, tf.keras.utils.Sequence)):
        #X is dataloader
        del params['y']
        for key, val in kwargs.items():
          params[key] = val

        for arg, key in zip(args, params.keys()):
          params[key] = arg

        if params['callbacks'] is None:
          callbacks = []
        else:
          callbacks = params['callbacks']
        callbacks.append(TruePerformanceCallback(params['x']))
        params['callbacks'] = callbacks

        return params

      else:
        #X and y are there
        for key, val in kwargs.items():
          params[key] = val

        for arg, key in zip(args, params.keys()):
          params[key] = arg

        if params['callbacks'] is None:
          callbacks = []
        else:
          callbacks = params['callbacks']
        callbacks.append(TruePerformanceCallback(params['x'], params['y']))
        params['callbacks'] = callbacks

        return params

    else:
      #when args is empty
      for key, val in kwargs.items():
        params[key] = val

      #add loss after/before epoch parameter here
      if params['callbacks'] is None:
        callbacks = []
      else:
        callbacks = params['callbacks']
      #assumes x and y are present
      callbacks.append(TruePerformanceCallback(params['x'], params['y']))
      params['callbacks'] = callbacks
      return params

class TruePerformanceCallback(tf.keras.callbacks.Callback):
  """A custom callback to compute the primary loss and accuracy of the model on training data without regularization effects."""

  def __init__(self, x, y= None):
      super().__init__()
      self.x = x
      self.y = y

  def on_epoch_end(self, epoch, logs= None):
      if logs is not None:
        # Evaluate the model on the training data
        if (self.y is None):
          results = self.model.evaluate(self.x, verbose=0)
        else:
          results = self.model.evaluate(self.x, self.y, verbose=0)
        # Log the evaluation results
        logs['base_loss'] = results[0]
        logs['base_accuracy'] = results[1]
