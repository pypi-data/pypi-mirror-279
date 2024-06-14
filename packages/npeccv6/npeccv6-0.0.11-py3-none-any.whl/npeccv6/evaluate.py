import argparse
import os
import json
from typing import Tuple

try:
    # Attempt relative imports (if run as a package module)
    from .data import DataGenerator, load_and_preprocess_data
    from .model_func import load_pretrained_model
    from .utils import f1, iou, setup_logger, read_config

except ImportError:
    # Fallback to absolute imports (if run as a standalone script)
    from data import DataGenerator, load_and_preprocess_data
    from model_func import load_pretrained_model
    from utils import f1, iou, setup_logger, read_config

# Set up logger
logger = setup_logger()

def model_eval(
    model, 
    test_generator: DataGenerator,
    batch_size: int = 16,
    output_path: str = "./models",
    steps: int = None,
) -> Tuple[float, float, float, float]:
    """
    Evaluates a pre-trained model on a test dataset of images and their corresponding masks.

    Parameters:
        - model: Loaded model to evaluate.
        - test_generator (DataGenerator): Validation data.
        - batch_size (int): Batch size.
        - output_path (str): Path to models directory. Default is "./models".
        - steps (int): Steps to take during evaluation.

    Returns:
        Tuple[float, float]:
            A tuple containing the F1 score and IoU (Intersection over Union) score for the model's predictions on the test dataset.

    Notes:
        The function performs the following steps:
        1. Sets up a logger for debugging and logging purposes.
        2. Initializes empty lists to store predictions (preds) and ground truth masks (y_true).
        3. Loads the specified pre-trained model.
        4. Iterates through each file in the test data directory:
            - Checks if the file is a PNG image.
            - Constructs the file path for the image and its corresponding mask.
            - Reads the mask image using OpenCV.
            - Uses the model to predict the mask for the image.
            - Appends the predicted mask and the ground truth mask to their respective lists.
        5. Calculates the F1 score and IoU score using the ground truth masks and the model's predictions.
        6. Logs and returns the F1 score and IoU score as a tuple.
    """

    # Define empty list for preds
    preds = []

    # Define empty list for y true
    y_true = []

    # Define empty list for confidence score
    conf_scores = []

    results = model.evaluate(test_generator, batch_size=batch_size, steps=steps)
    metrics = dict(zip(model.metrics_names, results))
    logger.info(f'Evaluation metrics: {metrics}')
    
    loss = metrics.get('loss', None)
    accuracy = metrics.get('accuracy', None)
    f1 = metrics.get('f1', None)
    iou = metrics.get('iou', None)

    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    model_details = {
    "loss": loss,
    "accuracy": accuracy,
    "f1": f1,
    "iou": iou,
    #"avg_conf": avg_conf_over_all_preds,
    #"timestamp": "2024-06-12T12:00:00"  # replace with actual timestamp
    }
    
    logger.info(f"Saving metrics to {output_path}/accuracy.json")

    with open(output_path + "/accuracy.json", "w") as f:
        json.dump(model_details, f)
    
    logger.info("Metrics saved")
    
    return loss, f1, accuracy, iou


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a model"
    )
    parser.add_argument(
        "--model_name", type=str, help="Name of model selected by the user."
    )
    parser.add_argument(
        "-c",
        "--classes",
        type=list,
        default=["root"],
        help="Classes to use to train the model the model. For single class(recomended): ['class'], for multiclass(not advised):['class1', 'class2', ...]",
    )
    parser.add_argument(
        "-d",
        "--patch_dir",
        type=str,
        default="./data_patched/",
        help="Path to data root directory, should end with '/'. Default: './data_patched/'",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=42,
        help="Seed for reading data and model training. Default: 42",
    )
    parser.add_argument(
        "-b",
        "--batch_size",
        type=int,
        default=16,
        help="Batch size to use during training. Default: 16",
    )
    parser.add_argument(
        "--models_path",
        type=str,
        default="./models",
        help="Path to models direcotry. Defautl is './models'",
    )
    parser.add_argument(
        "--config_path",
        type=str,
        default=None,
        help="Path to folder with models config file. Defaults to models_paht if not specified"
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default=None,
        help="Path where to save model accuracies"
    )

    # Parse the arguments
    args = parser.parse_args()
    model_name = args.model_name
    
    if args.config_path == None:
        args.config_path = args.models_path
    
    config = read_config(model_name, args.config_path)
    model = load_pretrained_model(model_name, args.models_path)

    (
        _,
        val_generator,
        _,
        validation_steps,
    ) = load_and_preprocess_data(
        classes=args.classes,
        model_name=args.model_name,
        patch_size=config["input_shape"][0],
        patch_dir=args.patch_dir,
        seed=args.seed,
        batch_size=args.batch_size,
    )

    logger.info(f"Moden input shape: {config['input_shape']}")

    loss, f1, accuracy, iou = model_eval(
        model = model, 
        test_generator = val_generator,
        batch_size = args.batch_size,
        output_path = args.output_path,
        steps = validation_steps,
    )


if __name__ == "__main__":
    main()