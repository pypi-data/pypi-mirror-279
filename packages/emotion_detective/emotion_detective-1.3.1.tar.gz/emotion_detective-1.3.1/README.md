
![Emotion Detective](https://bredauniversityadsai.github.io/2023-24d-fai2-adsai-group-nlp1/_images/emotion_detective.png)

## Overview

This NLP project provides functions to analyze emotions in video or audio files. It offers a comprehensive set of tools to detect and analyze emotions at a sentence level, producing valuable insights into the emotional content of multimedia sources. It includes a package with all necessary functions, two pipelines -- one for training the NLP model and one for inference, and Sphinx documentation.

## Installation

To install the package and its dependencies, use the following pip command:

```bash
pip install emotion_detective
```

### Additional Dependencies

The package also requires to have the following dependencies installed on your system. To install the additional dependencies, refer to the installation documentation linked below:

- [Rust](https://www.rust-lang.org/tools/install)
- [Cuda Toolkit](https://developer.nvidia.com/cuda-downloads)

## Usage

### Package

To use the package in your Python code, import it as follows:

```python
import emotion_detective
```

The package has the following structure:

```
───emotion_detective
   ├───data
   │   ├───inference
   │   │   └───data_ingestion.py
   │   │   └───data_preprocessing.py
   │   └───training
   │       └───data_ingestion.py
   │       └───data_preprocessing.py
   ├───logger
   │   └───logger.py
   │───models
   │   ├───model_definitions.py
   │   ├───model_predict.py
   │   ├───model_saving.py
   │   └───model_training.py
   │───main.py
   └───training.py   
```

### Files and Functions

#### data/inference/data_ingestion.py

- `mov_to_mp3_audio`: Extracts audio from a video file and saves it as an mp3 file. *(Author: Kacper Janczyk)*

#### data/inference/data_preparation.py

- `transcribe_translate`: Transcribes and translates audio files. *(Author: Kacper Janczyk)*
- `dataset_loader`: Creates a PyTorch DataLoader for a given DataFrame. *(Author: Kacper Janczyk)*

#### data/training/data_ingestion.py

- `load_data`: Load CSV or JSON file and return a DataFrame with specified text and emotion columns. *(Author: Martin Vladimirov)*

#### data/training/data_preprocessing.py

- `preprocess_text`: Preprocesses text data in a specified DataFrame column by:
    1. Lowercasing all text.
    2. Tokenizing each lowercased text into individual words.
    3. Lemmatizing each token to its base form using WordNetLemmatizer.
    4. Converting tokens to input IDs using the provided tokenizer.
    5. Mapping emotion labels from strings to integers and storing in a new column.
    6. Automatically determining the maximum length of input sequences and padding/truncating accordingly.
*(Author: Martin Vladimirov)*
- `balancing_multiple_classes`: Balance the classes in a DataFrame containing multiple classes. *(Author: Amy Suneeth)*
- `spell_check_and_correct`: Perform spell checking and correction on the input column of a DataFrame. *(Author: Amy Suneeth)*

#### logger/logger.py

- `setup_logging`: Sets up logging for the application. *(Author: Andrea Tosheva)*

#### models/model_definitions.py

- `roberta_model`: Creates a classification model using the Roberta architecture. *(Author: Rebecca Borski)*
- `rnn_model`: Creates a classification model using the RNN architecture. *(Author: Martin Vladimirov)*
- `load_model`: Load a pre-trained PyTorch model from the specified path. *(Author: Rebecca Borski, Martin Vladimirov)*

#### models/model_predict.py

- `get_predictions`: Obtain predictions from a model based on the input DataFrame. *(Author: Amy Suneeth)*

#### models/model_saving.py

- `save_model`: Saves the state of a PyTorch model to a binary file. *(Author: Andrea Tosheva)*

#### models/model_training.py

- `train_and_evaluate_roberta`: Trains and evaluates a neural network model for emotion detection using the RoBerta model. *(Author: Rebecca Borski)*
- `train_and_evaluate_rnn`: Trains and evaluates a neural network model for emotion detection using the RNN model. *(Author: Rebecca Borski)*

#### main.py

- `main`: Function to run the prebuilt inference pipeline. *(Authors: Rebecca Borski, Kacper Janczyk, Martin Vladimirov, Amy Suneeth, Andrea Tosheva)*

#### training.py

- `training_pipeline`: Function to run the prebuilt training pipeline. *(Authors: Rebecca Borski, Kacper Janczyk, Martin Vladimirov, Amy Suneeth, Andrea Tosheva)*

For further information on the functions, please refer to our [Emotion Detective Documentation](https://bredauniversityadsai.github.io/2023-24d-fai2-adsai-group-nlp1/).

### Pipelines

#### Training Pipeline

The training pipeline in this NLP project is the training pipeline for an emotion classification model. This pipeline executes the following steps:

1. **Data Loading**: It loads the input data from the specified file path, including text data and emotion labels.

2. **Class Balancing**: It balances the dataset to ensure equal representation of all emotion classes.

3. **Spelling Correction**: It corrects spelling mistakes in the text data.

4. **Text Preprocessing**: It preprocesses the text data, including tokenization and encoding.

5. **Model Training and Evaluation**: It trains and evaluates a RoBERTa-based emotion classification model using the preprocessed data, specified learning rate, batch size, number of epochs, and patience for early stopping.

6. **Model Saving**: It saves the trained model to the specified directory with the given name.

This pipeline takes the following parameters:

- `train_data_path`: Path to the file containing the training data
- `test_data_path`: Path to the file containing the testing data
- `text_column`: Name of the column in the DataFrame containing text data
- `emotion_column`: Name of the column in the DataFrame containing emotion labels
- `num_epochs`: Number of epochs to train the model
- `model_type`: Type of model that is going to be used (roberta, rnn)
- `model_dir`: Directory where the trained model will be saved
- `model_name`: Name to use when saving the trained model
- `learning_rate`: Learning rate for the optimizer
- `train_batch_size`: Batch size for training
- `eval_batch_size`: Batch size for evaluation
- `cloud_logging`: Set argument to 'True' if you are using AzureML cloud services

Upon completion, this pipeline does not return any value but logs the completion status.

#### Inference Pipeline

The first pipeline in this NLP project is the inference pipeline for emotion detection from video and audio files. This pipeline performs the following steps:

1. **Data Ingestion**: It ingests the input audio (mp3) or video file (mp4). If the input is a video file, it converts it to audio format and saves it to the specified output path.

2. **Data Preprocessing**: It transcribes and translates the audio using NLP techniques.

3. **Model Loading**: It loads the pre-trained NLP model specified by the `model_path`.

4. **Prediction**: It utilizes the loaded model to predict emotions from the transcribed sentences.

5. **Logging**: It logs the program's execution process, including information, warnings, and errors, to a log file (`logs/emotion_detective.txt`) and the console.

The pipeline takes the following parameters:

- `input_path`: Path to the input audio or video file.
- `output_audio_path` (optional): Path to save the transcribed audio file, required only when the input is a video file.  Ensure the file extension is .mp3.
- `model_path` (optional): Path to the saved NLP model, defaulting to "roberta-base".
- `batch_size` (optional): Batch size used for model prediction, defaulting to 32.

The pipeline returns a DataFrame containing transcribed sentences, predicted emotions, their values, and probabilities.

#### Pipelines Overview

![Visualisation of the pipeline](https://bredauniversityadsai.github.io/2023-24d-fai2-adsai-group-nlp1/_images/pipelines.png)

## Sphinx Documentation

To see the full documentation of the functions and their usage, please refer to the [Emotion Detective Documentation](https://bredauniversityadsai.github.io/2023-24d-fai2-adsai-group-nlp1/)

## API

The Emotion Detective package also offers an API for the training and inference pipeline.

To use the API, create a simple POST request containing the arguments for the specific pipeline.

Here is an example using the python library 'requests':

```python   
   import requests
   import json

   url = "localhost:8000/train" # still needs to be updated to our real url

   payload = json.dumps({
   "train_data_path": "./data/CSV/5000_sampled_emotions_neutral.csv",
   "test_data_path": "./data/CSV/val_set_5000.csv",
   "text_column": "text",
   "emotion_column": "label",
   "num_epochs": 1,
   "model_type": "rnn",
   "model_dir": "./models",
   "model_name": "rnn_test_api",
   "learning_rate": 0.001,
   "train_batch_size": 4,
   "eval_batch_size": 8,
   "cloud_logging": False
   })
   headers = {
   'Content-Type': 'application/json'
   }

   response = requests.request("POST", url, headers=headers, data=payload)

   print(response.text)
```

## Examples

### Building your own Training Pipeline

First, import the needed functions:

```python
    import pandas as pd
    from emotion_detective.logger.logger import setup_logging
    from emotion_detective.data.training.data_ingestion import load_data
    from emotion_detective.data.training.data_preprocessing import balancing_multiple_classes, preprocess_text, spell_check_and_correct
    from emotion_detective.models.model_saving import save_model
    from emotion_detective.models.model_training import train_and_evaluate_rnn, train_and_evaluate_roberta
```

Secondly, define the training pipeline:

```python
    def training_pipeline(
        train_data_path: str,
        test_data_path: str,
        text_column: str,
        emotion_column: str,
        num_epochs: int,
        model_type: str,
        model_dir: str,
        model_name: str,
        learning_rate: float = 0.001,
        train_batch_size: int = 4,
        eval_batch_size: int = 8,
        cloud_logging: bool = True
    ):
        logger = setup_logging()

        try:
            # Load data
            logger.info("Loading data...")
            train_data = load_data(train_data_path, text_column, emotion_column)
            test_data = load_data(test_data_path, text_column, emotion_column)
            
            # Preprocess text
            logger.info("Preprocessing text...")
            train_data = preprocess_text(train_data, text_column, 'label')
            test_data = preprocess_text(test_data, text_column, 'label')
            
            # Balance classes
            logger.info("Balancing classes...")
            train_data = balancing_multiple_classes(train_data, 'label')
            
            # Correct spelling mistakes
            logger.info("Correcting spelling mistakes...")
            train_data = spell_check_and_correct(train_data, text_column)

            NUM_LABELS = train_data['label'].nunique()
            
            # Initialize model based on model_type
            if model_type == 'roberta':
                model = roberta_model(NUM_LABELS)
                # Train and evaluate RoBERTa model
                logger.info("Training and evaluating RoBERTa model...")
                trained_model, eval_results = train_and_evaluate_roberta(
                    model, train_data, test_data,
                    num_train_epochs=num_epochs,
                    learning_rate=learning_rate,
                    eval_batch_size=eval_batch_size,
                    train_batch_size=train_batch_size,
                    cloud_logging=cloud_logging
                )
            elif model_type == 'rnn':
                model = rnn_model(NUM_LABELS)
                # Train and evaluate RNN model
                logger.info("Training and evaluating RNN model...")
                trained_model = train_and_evaluate_rnn(
                    model, train_data, test_data,
                    num_epochs=num_epochs,
                    learning_rate=learning_rate,
                    eval_batch_size=eval_batch_size,
                    train_batch_size=train_batch_size,
                    cloud_logging=cloud_logging
                )
            else:
                raise ValueError(f"Unsupported model type: {model_type}")

            # Save trained model
            logger.info("Saving model...")
            save_model(trained_model, model_dir, model_name)

            logger.info("Training pipeline completed successfully.")

        except Exception as e:
            logger.error(f"Error in training pipeline: {e}")
            raise
```

Lastly, use the function to train your model:

```python
# Example usage:
    if __name__ == "__main__":
        train_data_path = 'path_to_train_data.csv'
        test_data_path = 'path_to_test_data.csv'
        text_column = 'text'
        emotion_column = 'emotion'
        num_epochs = 5
        model_type = 'roberta'  # or 'rnn'
        model_dir = './models/'
        model_name = 'my_model'

        training_pipeline(
            train_data_path,
            test_data_path,
            text_column,
            emotion_column,
            num_epochs,
            model_type,
            model_dir,
            model_name,
            learning_rate=0.001,
            train_batch_size=4,
            eval_batch_size=8,
            cloud_logging=True
        )
```

### Building your own Inference Pipeline

First, import the needed functions:

```python
from emotion_detective.data.inference.data_ingestion import mov_to_mp3_audio
from emotion_detective.data.inference.data_preprocessing import transcribe_translate
from emotion_detective.models.model_definitions import load_model
from emotion_detective.models.model_predict import get_predictions
```

Secondly, define the inference pipeline:

```python
def main(
    input_path: str, 
    model_path: str , 
    output_audio_path: str = None, 
    batch_size: int = 32
    ):
    """Inference pipeline for emotion detection from video and audio files.

    Args:
        input_path (str): Path to input audio (mp3) or video file (mp4).
        output_audio_path (str, optional): Path to save the transcribed audio file. Required only when the input is a video file. Defaults to None.
        model_path (str, optional): Path to the saved NLP model. Defaults to "roberta-base".
        batch_size (int, optional): Batch size used for model prediction. Defaults to 32.

    Returns:
        pd.DataFrame: DataFrame containing transcribed sentences, predicted emotions, their values, and probability.
        
    Authors: Rebecca Borski, Kacper Janczyk, Martin Vladimirov, Amy Suneeth, Andrea Tosheva
    """
    logger = setup_logging()

    logger.info('Starting program...')

    model = load_model(model_path)

    if output_audio_path:
        logger.info("Converting video to audio...")
        mov_to_mp3_audio(input_path, output_audio_path)
        logger.info("Transcribing and translating audio...")
        transcribed_df = transcribe_translate(output_audio_path)
        print(transcribed_df)
    else:
        transcribed_df = transcribe_translate(input_path)
        print(transcribed_df)

    logger.info("Getting predictions...")
    predictions_df = get_predictions(model, transcribed_df, batch_size=batch_size, text_column='sentence')

    logger.info("Program finished.")
    
    return predictions_df
```

Lastly, use the function to train your model:

```python
predictions_df = main(
                    input_path='path/to/input/video.mov', 
                    model_path='path/to/saved/model.pth', 
                    output_audio_path='path/to/save/generated/audio.mp3', 
                    batch_size=32
                    )
```

## Credits

Amy Suneeth, Martin Vladimirov, Andrea Tosheva, Kacper Janczyk, Rebecca Borski
