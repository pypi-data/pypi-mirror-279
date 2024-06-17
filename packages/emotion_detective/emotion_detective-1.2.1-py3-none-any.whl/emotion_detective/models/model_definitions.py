import torch
import torch.nn as nn
from transformers import RobertaForSequenceClassification, RobertaConfig
from transformers import BertTokenizer
from emotion_detective.logger.logger import setup_logging
import h5py
from typing import Any

def roberta_model(num_labels: int) -> RobertaForSequenceClassification:
    """
    Creates a classification model using the RoBERTa architecture.

    Args:
        num_labels (int): The number of labels/classes for the classification task.

    Returns:
        RobertaForSequenceClassification: A RoBERTa model initialized with the specified number of labels.
        
    Author: Rebecca Borski
    """
    try:
        logger = setup_logging()
        logger.info("Creating a classification model.")
        
        config = RobertaConfig.from_pretrained(
            "roberta-base", num_labels=num_labels, force_download=True)

        model = RobertaForSequenceClassification.from_pretrained(
            "roberta-base", config=config, force_download=True)

        logger.info("Model created successfully.")
        return model

    except Exception as e:
        logger.error(f"Error in create_model: {e}")
        logger.info("Model creation failed.")
        return None

class RNNModel(nn.Module):
    def __init__(self, vocab_size: int, embedding_dim: int, hidden_dim: int, output_dim: int):
        super(RNNModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.5)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        embedded = self.embedding(x)
        output, (hidden, cell) = self.rnn(embedded)
        return self.fc(output[:, -1, :])

def rnn_model(num_labels: int, embedding_dim: int = 128, hidden_dim: int = 256) -> Any:
    """
    Creates a classification model using an RNN architecture.

    Args:
        num_labels (int): Number of output labels/classes.
        embedding_dim (int, optional): Dimension of word embeddings. Defaults to 128.
        hidden_dim (int, optional): Dimension of hidden states in the RNN. Defaults to 256.

    Returns:
        RNNModel: An RNN model initialized with the specified parameters.
        
    Author: Martin Vladimirov
    """
    logger = setup_logging()
    
    try:
        logger.info("Creating tokenizer.")
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        vocab_size = tokenizer.vocab_size

        logger.info("Creating RNN model.")
        model = RNNModel(vocab_size, embedding_dim, hidden_dim, num_labels)
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = model.to(device)
        logger.info("Model created successfully.")
        return model

    except Exception as e:
        logger.error(f"Error in creating RNN model: {e}")
        return None

def load_model(model_path: str) -> torch.nn.Module:
    """
    Load a pre-trained model from the specified path.

    Args:
        model_path (str): Path to the model file.

    Returns:
        torch.nn.Module: The loaded model.
        
    Author: Rebecca Borski, Martin Vladimirov
    """
    try:
        logger = setup_logging()

        logger.info("Loading a pre-trained model.")
        model = torch.load(model_path)
        logger.info("Loading successful.")

        return model

    except Exception as e:
        logger.error(f"Error in load_model: {e}")
        logger.info("Model loading failed.")
        return None
