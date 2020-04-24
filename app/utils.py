from fastai.vision import torch, load_learner, defaults

def load_model(args):
    """
    Take the the argument as a tuple containing path and the model name
    :args : tuple containing the path as Path object and the model name as string
    :return learner
    """
    if not isinstance(args,tuple):
        raise TypeError('Tuple expected with path and filename for loading model.')
    defaults.device = torch.device('cpu')
    print('Model Loaded')
    return load_learner(*args)
