try:
    from services.models import *
except:
    from mingus.service.models import *

import inspect
import sys


register_models = [i for i, j in globals().copy().items() if inspect.isclass(j) and j.__mro__[1].__name__ == 'BaseModel']
objects = {model.lower(): getattr(sys.modules[__name__], model) for model in register_models} # objects = {'Song': Song}


if __name__ == '__main__':
    print(objects)
