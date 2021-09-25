
import pickle
from app.utils.models import MLP

class CustomUnpickler(pickle.Unpickler):
    
    def find_class(self, module, name):
        try:
            return super().find_class(__name__, name)
        except AttributeError:
            return super().find_class(module, name)