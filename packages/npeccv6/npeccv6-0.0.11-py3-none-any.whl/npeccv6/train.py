#!/bin/python3
import argparse

try:
    # Attempt relative imports (if run as a package module)
    from .data import load_and_preprocess_data
    from .model_func import train_model
    from .utils import read_config, setup_logger

except ImportError:
    # Fallback to absolute imports (if run as a standalone script)
    from model_func import train_model
    from utils import read_config, setup_logger

    from data import load_and_preprocess_data

# Set up the logger
logger = setup_logger()


def main():
    parser = argparse.ArgumentParser(
        description="Train a U-net model from images and masks."
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
        "-e",
        "--epochs",
        type=int,
        default=20,
        help="Number of epochs. Default: 20",
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

    # Parse the arguments
    args = parser.parse_args()
    model_name = args.model_name
    
    if args.config_path == None:
        args.config_path = args.models_path
    
    config = read_config(model_name, args.config_path)
    logger.info(f'Loaded config {config}, type:{type(config)}')
    if isinstance(config, list):
        config = config[0]
    train_generator, test_generator, steps_per_epoch, validation_steps, = load_and_preprocess_data(
        classes=args.classes,
        model_name=model_name,
        patch_dir=args.patch_dir,
        patch_size=config['input_shape'][0],
        seed=args.seed,
        batch_size=args.batch_size,
    )

    logger.info(f"Training model\n{steps_per_epoch = }\n{validation_steps = }")
    logger.info(f"Moden input shape: {config['input_shape']}")

    history = train_model(
        model_name=model_name,
        train_generator=train_generator,
        val_generator=test_generator,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        epochs=args.epochs,
        models_path=args.models_path,
        config_folder=args.config_path,
    )


if __name__ == "__main__":
    main()
