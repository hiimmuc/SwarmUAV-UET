from typing import Any, Dict


class OutputLayerShape:
    def __init__(self) -> None:
        self.model_config = {
            'Caffe': {'shape': (300, 300),
                      'scale': 1.0,
                      'mean': (104.0, 177.0, 123.0),
                      'swapRB': False,
                      'crop': False},
            'TensorFlow': {'shape': (300, 300),
                           'scale': 1.0,
                           'mean': (127.5, 127.5, 127.5),
                           'swapRB': True,
                           'crop': False},
            'Torch': {'shape': (300, 300),
                      'scale': 1.0,
                      'mean': (0, 0, 0),
                      'swapRB': False,
                      'crop': False},
            'Darknet': {'shape': (416, 416),
                        'scale': 1.0/255.0,
                        'mean': (0, 0, 0),
                        'swapRB': True,
                        'crop': False}

        }
        pass

    def get_output_layer_shape(self, model_name: str) -> Dict[str, Any]:
        return self.model_config[model_name]
