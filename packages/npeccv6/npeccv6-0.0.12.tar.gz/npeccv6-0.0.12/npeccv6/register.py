import argparse
import os

from azure.ai.ml import MLClient
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Model
from azure.identity import ClientSecretCredential


def register_model_if_accuracy_above_threshold(
    model_path: str, accuracy_folder: str, threshold: float=0.5
):
    print(f"Registering model if accuracy is above {threshold}.")
    print(f"Model path: {model_path}")
    print(f"Accuracy file: {accuracy_folder}")
    # Get the accuracy file
    accuracy_file = os.path.join(accuracy_folder, "accuracy.txt")
    # Load accuracy from file
    with open(accuracy_file, "r") as f:
        print(f"Reading accuracy from {accuracy_file}")
        accuracy = float(f.read().strip())

    print(f"Model accuracy: {accuracy}")

    # Only register model if accuracy is above threshold
    if accuracy['accuracy'] > threshold:
        print("Model accuracy is above threshold, registering model.")

        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        resource_group = "buas-y2"
        workspace_name = "CV6"

        #cridentail = CloientSecretCridential(tenat_id, client_id, client_secret)
        tenant_id = os.getenv("AZURE_TENANT_ID")
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET")
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)

        ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)
        
        model = Model(
            #path=f"{model_path}/{model_name}.keras",
            path=model_path,
            type=AssetTypes.CUSTOM_MODEL,
            name=model_name,
            description="Model created from pipeline",
        )

        # Register the model
        model = ml_client.models.create_or_update(model)
        # print(f"Model {model.name} registered.")
        print("Model registered.")
    else:
        print("Model accuracy is not above threshold, not registering model.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Register a TensorFlow model if accuracy is above threshold."
    )
    parser.add_argument("--model_path", type=str, help="Path to the file saved model.")
    #parser.add_argument("--model_name", type=str, help="Name of the model.")
    parser.add_argument(
        "--accuracy", type=str, help="Path to the file containing model accuracy."
    )
    parser.add_argument("--threshold", type=int, help="Threshold of the model accuracy.", default=0.9)
    args = parser.parse_args()

    #register_model_if_accuracy_above_threshold(args.model_path, args.model_name, args.accuracy, args.threshold)
    register_model_if_accuracy_above_threshold(args.model_path, args.accuracy, args.threshold)