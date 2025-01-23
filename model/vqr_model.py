# Import Libraries
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
from utils.config_loader import ConfigLoader
from custom_logger.custom_logging import CustomLogger

# Define GPU
device_gpu = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Virtual_Question_Answering:
    def __init__(self):
        # Load configuration from the config file
        self.config = ConfigLoader.config_loader(file_name="config.yaml")
        # Initialize generation parameters from the configuration
        self.gen_kwargs = {"max_length": self.config.get("max_length"), "num_beams": self.config.get("num_beams")}
        # Get the model name from the configuration
        self.model_name = self.config.get("model_name")
        # Placeholders for model, feature extraction, and tokenizer
        self.model = None
        self.feature_extraction = None
        self.tokenizer = None
        # Create a custom logger
        self.logger = CustomLogger.create_custom_logger(name="Virtual_Question_AnsweringModel")

    def load_model(self):
        try:
            # Load the VisionEncoderDecoder model from the pretrained model
            self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
            # Move the model to the GPU if available
            self.model = self.model.to(device_gpu)
            # Load the image processor for feature extraction
            self.feature_extraction = ViTImageProcessor.from_pretrained(self.model_name)
            # Load the tokenizer for decoding the generated output
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            # Log the successful loading of the model
            self.logger.info(f"Model {self.model_name} loaded successfully.")
        except Exception as e:
            # Log the error if the model fails to load
            self.logger.error(f"Failed to load model: {e}")
            self.tokenizer = None
            self.model = None
            # Raise an exception to ensure the failure is handled
            raise

    def predict_model(self, image_path):
        try:
            # Open the image from the provided path
            image = Image.open(image_path)
            # Convert the image to RGB if it is not already in that mode
            if image.mode != "RGB":
                image = image.convert(mode="RGB")
            
            # Perform feature extraction on the image to obtain pixel values
            pixel_value = self.feature_extraction(images=image, return_tensors="pt").pixel_values
            # Move the pixel values to the GPU if available
            pixel_value = pixel_value.to(device=device_gpu)

            # Generate the output (caption) for the image using the model
            output = self.model.generate(pixel_value, **self.gen_kwargs)
            # Log the successful generation of the caption
            self.logger.info("Caption Generated Successfully.")
            
            # Decode the output using the tokenizer
            predicted_caption = self.tokenizer.batch_decode(output, skip_special_tokens=True)
            # Strip any leading or trailing whitespace from the predicted caption
            predicted_caption = [pred.strip() for pred in predicted_caption]

            # Return the predicted caption
            return predicted_caption[0]
        
        except Exception as e:
            # Log the error if the prediction fails
            self.logger.error(f"Generation Caption Failed: {e}")
            # Return None to indicate failure
            return None