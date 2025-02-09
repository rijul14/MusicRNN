import os
import torch
import json
from models.LSTM_model import MusicRNN, MusicRNNParams

PARENT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
PARSING_DATA_DIR = os.path.join(PARENT_DIR, 'data')
DATA_DIR = os.path.join(PARENT_DIR, 'fake_data')

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def check_gpu():
    print("----Checking GPU----")

    print("CUDA available: " + str(torch.cuda.is_available()))
    print("Device: " + str(DEVICE))
    print("GPU: " + str(torch.cuda.get_device_name(0)))
    print("GPU Cores: " + str(torch.cuda.device_count()))
    print("GPU Memory: " + str(torch.cuda.get_device_properties(DEVICE).total_memory))
    print("")


def check_data():
    print("----Checking Data----")
    train_notes_tensor = torch.load(os.path.join(DATA_DIR, 'train_notes_tensor.pt')).to(DEVICE)
    train_chords_tensor = torch.load(os.path.join(DATA_DIR, 'train_chords_tensor.pt')).to(DEVICE)

    dev_notes_tensor = torch.load(os.path.join(DATA_DIR, 'dev_notes_tensor.pt')).to(DEVICE)
    dev_chords_tensor = torch.load(os.path.join(DATA_DIR, 'dev_chords_tensor.pt')).to(DEVICE)

    test_notes_tensor = torch.load(os.path.join(DATA_DIR, 'test_notes_tensor.pt')).to(DEVICE)
    test_chords_tensor = torch.load(os.path.join(DATA_DIR, 'test_chords_tensor.pt')).to(DEVICE)


    # check if data is cuda
    print("train notes cuda: " + str(train_notes_tensor.is_cuda))
    print("train chords cuda: " + str(train_chords_tensor.is_cuda))
    print("")

    print("dev notes cuda: " + str(dev_notes_tensor.is_cuda))
    print("dev chords cuda: " + str(dev_chords_tensor.is_cuda))
    print("")

    print("test notes cuda: " + str(test_notes_tensor.is_cuda))
    print("test chords cuda: " + str(test_chords_tensor.is_cuda))
    print("")


def check_model():
    print("----Checking Model----")
    chords_vocab = []
    with open(os.path.join(DATA_DIR, 'chords_vocab.json')) as json_file:
        chords_vocab = json.load(json_file)

    notes_vocab = []
    with open(os.path.join(DATA_DIR, 'pitches_vocab.json')) as json_file:
        notes_vocab = json.load(json_file)

    print("----------------- Done Loading Testing Tensors -----------------")
    print("")

    # create model
    params = MusicRNNParams(
        vocab_dim = len(notes_vocab),
        chord_dim = len(chords_vocab)
    )
    
    model = MusicRNN(params).to(DEVICE)

    # load model
    model.load_state_dict(torch.load(os.path.join(DATA_DIR, 'best_model_2.pt')))

    # check if model is cuda
    print("model cuda: " + str(next(model.parameters()).is_cuda))
    print("")


if __name__ == "__main__":
    check_gpu()
    check_data()
    check_model()