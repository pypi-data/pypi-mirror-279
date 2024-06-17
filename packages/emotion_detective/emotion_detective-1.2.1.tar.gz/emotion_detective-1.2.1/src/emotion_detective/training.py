import typer
from colorama import Fore, Style
from .logger.logger import setup_logging
from .data.training.data_ingestion import load_data
from .data.training.data_preprocessing import balancing_multiple_classes, preprocess_text, spell_check_and_correct
from .models.model_saving import save_model
from .models.model_training import train_and_evaluate_rnn, train_and_evaluate_roberta
from .models.model_definitions import roberta_model, rnn_model

app = typer.Typer()

def show_instructions():
    instructions = f"""
{Fore.YELLOW}🎭 Welcome to the Emotion Classifier Training CLI! 🎭{Style.RESET_ALL}

{Fore.CYAN}This tool trains a classification model to detect emotions from text data.{Style.RESET_ALL}

{Fore.GREEN}🚀 Instructions: {Style.RESET_ALL}
1. {Fore.BLUE}train_data_path: {Style.RESET_ALL} Path to the file containing the training data. {Fore.RED}[required]{Style.RESET_ALL}
2. {Fore.BLUE}test_data_path: {Style.RESET_ALL} Path to the file containing the testing data. {Fore.RED}[required]{Style.RESET_ALL}
3. {Fore.BLUE}text_column: {Style.RESET_ALL} Name of the column in the DataFrame containing text data. {Fore.RED}[required]{Style.RESET_ALL}
4. {Fore.BLUE}emotion_column: {Style.RESET_ALL} Name of the column in the DataFrame containing emotion labels. {Fore.RED}[required]{Style.RESET_ALL}
5. {Fore.BLUE}learning_rate: {Style.RESET_ALL} Learning rate for the optimizer. {Fore.RED}[required]{Style.RESET_ALL}
6. {Fore.BLUE}num_epochs: {Style.RESET_ALL} Number of epochs to train the model. {Fore.RED}[required]{Style.RESET_ALL}
7. {Fore.BLUE}model_type: {Style.RESET_ALL} Type of model that is going to be used (roberta, rnn) {Fore.RED}[required]{Style.RESET_ALL}
8. {Fore.BLUE}model_dir: {Style.RESET_ALL} Directory where the trained model will be saved. {Fore.RED}[required]{Style.RESET_ALL}
9. {Fore.BLUE}model_name: {Style.RESET_ALL} Name to use when saving the trained model. {Fore.RED}[required]{Style.RESET_ALL}
10. {Fore.BLUE}cloud_logging: {Style.RESET_ALL} Set to 'True', if you are using AzureML cloud services. {Fore.RED}[defaults to: True]{Style.RESET_ALL}

{Fore.MAGENTA}🔔 Please provide the necessary inputs when prompted. 🔔{Style.RESET_ALL}
"""
    print(instructions)


def training_pipeline(
    train_data_path: str,
    test_data_path: str,
    text_column: str,
    emotion_column: str,
    num_epochs: int,
    model_type: str,
    model_dir: str,
    model_name: str,
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
        train_data = balancing_multiple_classes(train_data, 'label' )

        logger.info("Correcting spelling mistakes...")
        train_data = spell_check_and_correct(train_data, text_column)

        NUM_LABELS =  train_data['label'].nunique()
        
        if model_type == 'roberta':
            model = roberta_model(NUM_LABELS)
            # Train and evaluate model
            logger.info("Training and evaluating model...")
            trained_model, eval = train_and_evaluate_roberta(model, train_data, test_data, num_train_epochs=num_epochs, cloud_logging=cloud_logging)
        if model_type == 'rnn': 
            model = rnn_model(NUM_LABELS)
            # Train and evaluate model
            logger.info("Training and evaluating model...")
            trained_model = train_and_evaluate_rnn(model, train_data, test_data, num_epochs=num_epochs, cloud_logging=cloud_logging)
        # Save model
        logger.info("Saving model...")
        save_model(trained_model, model_dir, model_name)

        logger.info("Training pipeline completed successfully.")

    except Exception as e:
        logger.error(f"Error in training pipeline: {e}")
        raise

@app.command()
def train(
    train_data_path: str = typer.Option(None, help="Path to the file containing the training data"),
    test_data_path: str = typer.Option(None, help="Path to the file containing the testing data"),
    text_column: str = typer.Option(None, help="Name of the column in the DataFrame containing text data"),
    emotion_column: str = typer.Option(None, help="Name of the column in the DataFrame containing emotion labels"),
    num_epochs: int = typer.Option(None, help="Number of epochs to train the model"),
    model_type: str = typer.Option(None, help="Type of model that is going to be used (roberta, rnn)"),
    model_dir: str = typer.Option(None, help="Directory where the trained model will be saved"),
    model_name: str = typer.Option(None, help="Name to use when saving the trained model"),
    cloud_logging: bool = typer.Option(None, help="Set to 'True', if you are using AzureML cloud services")

):
    show_instructions()
    train_data_path = input(f"Enter training file path: ")
    test_data_path = input(f"Enter testing file path: ")
    text_column = input(f"Enter text column name: ")
    emotion_column = input(f"Enter emotion column name: ")
    num_epochs = int(input(f"Enter number of epochs: "))
    model_type = str(input(f"Enter model type: "))
    model_dir = input(f"Enter model directory: ")
    model_name = input(f"Enter model name: ")
    cloud_logging = input(f"Enable cloud logging (True): ")

    training_pipeline(
    train_data_path,
    test_data_path,
    text_column,
    emotion_column,
    num_epochs,
    model_type,
    model_dir,
    model_name,
    cloud_logging
    )

if __name__ == "__main__":
    app()

