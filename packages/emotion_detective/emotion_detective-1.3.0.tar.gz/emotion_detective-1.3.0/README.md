
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
   └───models
       ├───model_definitions.py
       ├───model_predict.py
       ├───model_saving.py
       └───model_training.py
       
```

### Files and Functions

#### data/inference/data_ingestion.py

- `mov_to_mp3_audio`: Extracts audio from a video file and saves it as an mp3 file.

#### data/inference/data_preparation.py

- `transcribe_translate`: Transcribes and translates audio files.
- `dataset_loader`: Creates a PyTorch DataLoader for a given DataFrame.

#### data/training/data_ingestion.py

- `load_data`: Load CSV or JSON file and return a DataFrame with specified text and emotion columns.

#### data/training/data_preprocessing.py

- `preprocess_text`: Preprocesses text data in a specified DataFrame column by:
    1. Lowercasing all text.
    2. Tokenizing each lowercased text into individual words.
    3. Lemmatizing each token to its base form using WordNetLemmatizer.
    4. Converting tokens to input IDs using the provided tokenizer.
    5. Mapping emotion labels from strings to integers and storing in a new column.
    6. Automatically determining the maximum length of input sequences and padding/truncating accordingly.

- `balancing_multiple_classes`: Balance the classes in a DataFrame containing multiple classes.
- `spell_check_and_correct`: Perform spell checking and correction on the input column of a DataFrame.

#### logger/logger.py

- `setup_logging`: Sets up logging for the application.

#### models/model_definitions.py

- `create_model`: Creates a classification model using the Roberta architecture.
- `load_model`: Load a pre-trained RobertaForSequenceClassification model from the specified path.

#### models/model_predict.py

- `get_predictions`: Obtain predictions from a model based on the input DataFrame.

#### models/model_saving.py

- `save_model`: Saves the state of a PyTorch model to a binary file.

#### models/model_training.py

- `train_and_evaluate`: Trains and evaluates a neural network model for emotion detection.

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

- `file_path`: Path to the file containing the input data.
- `text_column`: Name of the column in the DataFrame containing text data.
- `emotion_column`: Name of the column in the DataFrame containing emotion labels.
- `mapped_emotion_column`: Name of the column in the DataFrame containing mapped emotion labels.
- `input_id_column`: Name of the column in the DataFrame containing input IDs.
- `learning_rate`: Learning rate for the optimizer.
- `batch_size`: Batch size for training and validation DataLoaders.
- `num_epochs`: Number of epochs to train the model.
- `patience`: Patience for early stopping.
- `model_dir`: Directory where the trained model will be saved.
- `model_name`: Name to use when saving the trained model.

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

#### Pipeline Overview

![Visualisation of the pipeline](https://bredauniversityadsai.github.io/2023-24d-fai2-adsai-group-nlp1/_images/pipelines.png)

### Sphinx Documentation

To see the full documentation of the functions and their usage, please refer to the [Emotion Detective Documentation](https://bredauniversityadsai.github.io/2023-24d-fai2-adsai-group-nlp1/)

## Examples

### Example Training Pipeline

First, import the needed functions:

```python
from emotion_detective.logger.logger import setup_logging
from emotion_detective.data.training.data_ingestion import load_data
from emotion_detective.data.training.data_preprocessing import balancing_multiple_classes, preprocess_text, spell_check_and_correct
from emotion_detective.models.model_saving import save_model
from emotion_detective.models.model_training import train_and_evaluate
```

Secondly, define the training pipeline:

```python
def training_pipeline(
    file_path: str,
    text_column: str,
    emotion_column: str,
    mapped_emotion_column: str,
    input_id_column: str,
    learning_rate: float,
    batch_size: int,
    num_epochs: int,
    patience: int,
    model_dir: str,
    model_name: str
):
    """
    Executes the complete training pipeline for an emotion classification model.

    This function performs the following steps:
    1. Loads the data from a specified file path.
    2. Balances the dataset to ensure equal representation of all emotion classes.
    3. Preprocesses the text data, including tokenization and encoding.
    4. Trains and evaluates a RoBERTa-based emotion classification model.
    5. Saves the trained model to a specified directory with a given name.

    Args:
        file_path (str): Path to the file containing the input data.
        text_column (str): Name of the column in the DataFrame containing text data.
        emotion_column (str): Name of the column in the DataFrame containing emotion labels.
        mapped_emotion_column (str): Name of the column in the DataFrame containing mapped emotion labels.
        input_id_column (str): Name of the column in the DataFrame containing input IDs.
        learning_rate (float): Learning rate for the optimizer.
        batch_size (int): Batch size for training and validation DataLoaders.
        num_epochs (int): Number of epochs to train the model.
        patience (int): Patience for early stopping.
        model_dir (str): Directory where the trained model will be saved.
        model_name (str): Name to use when saving the trained model.

    Returns:
        None

    Raises:
        Exception: If any error occurs during the pipeline execution, it will be logged and re-raised.

    Authors:
        Rebecca Borski, Kacper Janczyk, Martin Vladimirov, Amy Suneeth, Andrea Tosheva
    """
    logger = setup_logging()

    try:
        # Load data
        logger.info("Loading data...")
        df = load_data(file_path, text_column, emotion_column)

        # Balance classes
        logger.info("Balancing classes...")
        df = balancing_multiple_classes(df, emotion_column)

        logger.info("Correct Spelling Mistakes...")
        df = spell_check_and_correct(df, text_column)

        # Preprocess text
        logger.info("Preprocessing text...")
        df = preprocess_text(df, text_column, emotion_column)

        # Train and evaluate model
        logger.info("Training and evaluating model...")
        model = train_and_evaluate(df, mapped_emotion_column, input_id_column, learning_rate, batch_size, num_epochs, patience)

        # Save model
        logger.info("Saving model...")
        save_model(model, model_dir, model_name)

        logger.info("Training pipeline completed successfully.")

    except Exception as e:
        logger.error(f"Error in training pipeline: {e}")
        raise
```

Lastly, use the function to train your model:

```python
training_pipeline(
    file_path='path/to/your/file.csv',
    text_column='sentence',
    emotion_column='emotion',
    mapped_emotion_column='mapped_emotion',
    input_id_column='input_ids',
    learning_rate=0.01,
    batch_size=32,
    num_epochs=1,
    patience=3,
    model_dir='models',
    model_name='my_model'
)
```

### Example Inference Pipeline

First, import the needed functions:

```python
from emotion_detective.data.inference.data_ingestion import mov_to_mp3_audio
from emotion_detective.data.inference.data_preprocessing import transcribe_translate
from emotion_detective.models.model_definitions import load_model
from emotion_detective.models.model_predict import get_predictions
```

Secondly, define the inference pipeline:

```python
def main(input_path: str, model_path: str , output_audio_path: str = None, batch_size: int = 32):
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
