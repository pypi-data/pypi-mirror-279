import torch
import mlflow
import matplotlib.pyplot as plt
import pandas as pd
import torch.nn as nn
from datasets import Dataset
from transformers import (
    Trainer, TrainingArguments, RobertaTokenizerFast,
    EarlyStoppingCallback, BertTokenizer
)
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from torch.utils.data import DataLoader, TensorDataset
from typing import Tuple, Dict, Any

def train_and_evaluate_roberta(
    roberta_model: nn.Module,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    output_dir: str = './',
    logging_dir: str = './',
    num_train_epochs: int = 1,
    per_device_train_batch_size: int = 4,
    per_device_eval_batch_size: int = 8,
    gradient_accumulation_steps: int = 16,
    learning_rate: float = 2e-5,
    warmup_steps: int = 500,
    weight_decay: float = 0.01,
    logging_steps: int = 8,
    disable_tqdm: bool = False,
    dataloader_num_workers: int = 8,
    seed: int = 42,
    early_stopping_patience: int = 3,
    cloud_logging: bool = False
) -> Tuple[nn.Module, Dict[str, Any]]:
    """
    Train and evaluate a RoBERTa model using the given training and test data.

    Args:
        roberta_model: Pre-trained RoBERTa model to fine-tune.
        train_data: Training data in a pandas DataFrame.
        test_data: Test data in a pandas DataFrame.
        output_dir: Directory to save the model and outputs.
        logging_dir: Directory to save the logs.
        num_train_epochs: Number of training epochs.
        per_device_train_batch_size: Batch size for training.
        per_device_eval_batch_size: Batch size for evaluation.
        gradient_accumulation_steps: Number of gradient accumulation steps.
        learning_rate: Learning rate for training.
        warmup_steps: Number of warmup steps.
        weight_decay: Weight decay for the optimizer.
        logging_steps: Frequency of logging.
        disable_tqdm: Disable tqdm progress bar if True.
        dataloader_num_workers: Number of worker threads for data loading.
        seed: Random seed for reproducibility.
        early_stopping_patience: Patience for early stopping.
        cloud_logging: Enable cloud logging with MLflow if True.

    Returns:
        A tuple containing the trained model and evaluation results.
        
    Author: Rebecca Borski
    """
    # Load tokenizer
    tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base', max_length=512)

    def tokenization(batched_text: Dict[str, Any]) -> Dict[str, Any]:
        return tokenizer(batched_text['text'], padding=True, truncation=True)

    # Map the tokenization function to your DataFrame
    tokenized_train_data = Dataset.from_pandas(train_data).map(
        tokenization, batched=True, batch_size=len(train_data)
    )
    tokenized_test_data = Dataset.from_pandas(test_data).map(
        tokenization, batched=True, batch_size=len(test_data)
    )

    tokenized_train_data.set_format('torch', columns=['input_ids', 'attention_mask', 'label'])
    tokenized_test_data.set_format('torch', columns=['input_ids', 'attention_mask', 'label'])

    # Define compute_metrics function
    def compute_metrics(pred: Any) -> Dict[str, float]:
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
        acc = accuracy_score(labels, preds)
        return {
            'accuracy': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }

    # Define the TrainingArguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        eval_strategy="epoch",
        save_strategy="epoch",  # Set save_strategy to match eval_strategy
        logging_dir=logging_dir,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_eval_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        num_train_epochs=num_train_epochs,
        logging_steps=logging_steps,
        learning_rate=learning_rate,
        warmup_steps=warmup_steps,
        weight_decay=weight_decay,
        disable_tqdm=disable_tqdm,
        dataloader_num_workers=dataloader_num_workers,
        seed=seed,
        report_to=[],  # Disable wandb and other logging services
        load_best_model_at_end=True,
        metric_for_best_model='eval_loss',
    )

    # Instantiate Trainer with EarlyStoppingCallback
    trainer = Trainer(
        model=roberta_model,
        args=training_args,
        train_dataset=tokenized_train_data,
        eval_dataset=tokenized_test_data,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=early_stopping_patience)]
    )

    if cloud_logging:
        mlflow.start_run()

    # Start training
    trainer.train()

    # Evaluate the model
    eval_results = trainer.evaluate()

    if cloud_logging:
        for key, value in eval_results.items():
            mlflow.log_metric(key, value)
        mlflow.end_run()

    # Return the trained model and evaluation results
    return trainer.model, eval_results


def train_and_evaluate_rnn(
    model: nn.Module,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    num_epochs: int = 3,
    early_stopping_patience: int = 3,
    cloud_logging: bool = False
) -> nn.Module:
    """
    Train and evaluate an RNN model using the given training and test data.

    Args:
        model: RNN model to train.
        train_data: Training data in a pandas DataFrame.
        test_data: Test data in a pandas DataFrame.
        num_epochs: Number of training epochs.
        early_stopping_patience: Patience for early stopping.
        cloud_logging: Enable cloud logging with MLflow if True.

    Returns:
        The trained RNN model.
        
    Author: Rebecca Borski
    """
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def tokenize(text: str, tokenizer: BertTokenizer, max_len: int = 512) -> torch.Tensor:
        return tokenizer.encode(text, max_length=max_len, truncation=True, padding='max_length')

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    train_data['input_ids'] = train_data['text'].apply(lambda x: tokenize(x, tokenizer))
    test_data['input_ids'] = test_data['text'].apply(lambda x: tokenize(x, tokenizer))

    train_dataset = TensorDataset(
        torch.tensor(train_data['input_ids'].tolist()), torch.tensor(train_data['label'].tolist())
    )
    test_dataset = TensorDataset(
        torch.tensor(test_data['input_ids'].tolist()), torch.tensor(test_data['label'].tolist())
    )

    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    best_val_loss = float('inf')
    patience_counter = 0
    best_epoch = 0
    best_model = None

    if cloud_logging:
        mlflow.start_run()

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for input_ids, labels in train_loader:
            input_ids, labels = input_ids.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(input_ids)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        model.eval()
        eval_loss = 0
        all_preds = []
        all_labels = []
        with torch.no_grad():
            for input_ids, labels in test_loader:
                input_ids, labels = input_ids.to(device), labels.to(device)
                outputs = model(input_ids)
                loss = criterion(outputs, labels)
                eval_loss += loss.item()
                preds = torch.argmax(outputs, dim=1)
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

        train_loss = total_loss / len(train_loader)
        eval_loss /= len(test_loader)

        precision, recall, f1, _ = precision_recall_fscore_support(
            all_labels, all_preds, average='weighted', zero_division=1
        )
        accuracy = accuracy_score(all_labels, all_preds)

        print(f'Epoch {epoch + 1}/{num_epochs}')
        print(f'Train Loss: {train_loss:.4f}')
        print(f'Val Loss: {eval_loss:.4f}, Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}')

        if cloud_logging:
            mlflow.log_metric("train_loss", train_loss, step=epoch + 1)
            mlflow.log_metric("eval_loss", eval_loss, step=epoch + 1)
            mlflow.log_metric("accuracy", accuracy, step=epoch + 1)
            mlflow.log_metric("precision", precision, step=epoch + 1)
            mlflow.log_metric("recall", recall, step=epoch + 1)
            mlflow.log_metric("f1_score", f1, step=epoch + 1)

        # Implementing early stopping
        if eval_loss < best_val_loss:
            best_val_loss = eval_loss
            best_epoch = epoch
            best_model = model
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= early_stopping_patience:
                print(f'Early stopping at epoch {epoch + 1} with best validation loss: {best_val_loss:.4f}')
                if cloud_logging:
                    mlflow.end_run()
                return best_model

    if cloud_logging:
        # Plot the training and validation loss and accuracies for each epoch using matplotlib and log the image to MLflow
        fig = plt.figure()
        plt.plot(train_loss, label='train_loss')
        plt.plot(eval_loss, label='val_loss')
        plt.plot(accuracy, label='accuracy')
        plt.plot(precision, label='precision')
        plt.title("Learning curves")
        plt.xlabel("Epochs")
        plt.ylabel("Metrics")
        plt.legend(loc="lower left")
        plt.savefig("learning_metrics.png")
        mlflow.log_artifact("learning_metrics.png")
        mlflow.end_run()
        mlflow.end_run()

    return model
