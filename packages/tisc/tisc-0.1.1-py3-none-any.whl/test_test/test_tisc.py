from test_dev.tisc import make_model_registry, build_classifier
from test_dev.tisc import import_module_from_string

import torch
import torch.nn as nn
import torch.optim as optim
from test_dev.modules import TiscNetwork

# function to test make_model_registry with pytest
def test_make_model_registry():
    package_dir, registry = make_model_registry()
    print(package_dir, registry)
    assert registry == {'LSTM': '.modules.LSTM.LSTMBuilder', 'BiLSTM': '.modules.BiLSTM.BiLSTMBuilder', 'Transformer': '.modules.Transformer.TransformerBuilder'}
    package_dir, registry = make_model_registry(custom_modules_dir="mymodules")
    print(package_dir, registry)
    assert registry == {'LSTM': 'mymodules.LSTM.LSTMBuilder', 'BiLSTM': 'mymodules.BiLSTM.BiLSTMBuilder'}


# function to test build_classifier with pytest
def test_build_classifier():
    classifier = build_classifier("LSTM",
                                 timestep=10,
                                 dimentions=108,
                                 num_classes=2)
    assert classifier.model_name == "LSTM"
    assert classifier.num_classes == 2
    assert classifier.model.__class__ == TiscNetwork
    assert classifier.device.__class__ == torch.device
    assert classifier.criterion.__class__ == nn.CrossEntropyLoss
    assert classifier.optimizer.__class__ == optim.Adam
    assert classifier.scheduler is None
    assert classifier.outout_base == "tisc_output"
    assert classifier.classes == ["0", "1"]
    assert classifier.training_loss_list == []
    assert classifier.validation_loss_list == []
    assert classifier.training_accuracy_list == []
    assert classifier.validation_accuracy_list == []
    print(classifier.model)

    classifier = build_classifier("LSTM",
                                 timestep=10,
                                 dimentions=108,
                                 num_classes=0)
    assert classifier.model_name == "LSTM"
    assert classifier.num_classes == 0
    assert classifier.model.__class__ == TiscNetwork
    assert classifier.device.__class__ == torch.device
    assert classifier.criterion.__class__ == nn.CrossEntropyLoss
    assert classifier.optimizer.__class__ == optim.Adam
    assert classifier.scheduler is None
    assert classifier.outout_base == "tisc_output"
    assert classifier.classes == []
    assert classifier.training_loss_list == []
    assert classifier.validation_loss_list == []
    assert classifier.training_accuracy_list == []
    assert classifier.validation_accuracy_list == []
    print(classifier.model)

    classifier = build_classifier("BiLSTM",
                                 timestep=10,
                                 dimentions=3,
                                 num_classes=2,
                                 custom_modules_dir="mymodules")
    assert classifier.model_name == "BiLSTM"
    assert classifier.num_classes == 2
    # assert classifier.model.__class__ == TiscNetwork
    assert classifier.device.__class__ == torch.device
    assert classifier.criterion.__class__ == nn.CrossEntropyLoss
    assert classifier.optimizer.__class__ == optim.Adam
    assert classifier.scheduler is None
    assert classifier.outout_base == "tisc_output"
    assert classifier.classes == ["0", "1"]
    assert classifier.training_loss_list == []
    assert classifier.validation_loss_list == []
    assert classifier.training_accuracy_list == []
    assert classifier.validation_accuracy_list == []

    classifier = build_classifier("BiLSTM",
                                 timestep=10,
                                 dimentions=3,
                                 num_classes=2)
    assert classifier.model_name == "BiLSTM"
    assert classifier.num_classes == 2
    assert classifier.model.__class__ == TiscNetwork
    assert classifier.device.__class__ == torch.device
    assert classifier.criterion.__class__ == nn.CrossEntropyLoss
    assert classifier.optimizer.__class__ == optim.Adam
    assert classifier.scheduler is None
    assert classifier.outout_base == "tisc_output"
    assert classifier.classes == ["0", "1"]
    assert classifier.training_loss_list == []
    assert classifier.validation_loss_list == []
    assert classifier.training_accuracy_list == []
    assert classifier.validation_accuracy_list == []

    # classifier = build_classifier("LSTM",
    #                              timestep=10,
    #                              dimentions=3,
    #                              num_classes=2,
    #                              model_path="test_dev/tisc_output/LSTM/20210904123456/weights/model.pth",
    #                              history_path="test_dev/tisc_output/LSTM/20210904123456/training_history.npz")
    # assert classifier.model_name == "LSTM"
    # assert classifier.num_classes == 2
    # assert classifier.model.__class__ == TiscNetwork
    # assert classifier.device.__class__ == torch.device
    # assert classifier.criterion.__class__ == nn.CrossEntropyLoss
    # assert classifier.optimizer.__class__ == optim.Adam
    # assert classifier.scheduler is None
    # assert classifier.outout_base == "tisc_output"
    # assert classifier.classes == ["0", "1"]


# fuction to test import_module_from_string with pytest
# def test_import_module_from_string():
#     module = import_module_from_string("test_dev.tisc")
#     assert module.__name__ == "test_dev.tisc"
#     module = import_module_from_string("test_dev.tisc.make_model_registry")
#     assert module.__name__ == "test_dev.tisc"
#     module = import_module_from_string("test_dev.tisc.make_model_registry()")
#     assert module.__name__ == "test_dev.tisc"

