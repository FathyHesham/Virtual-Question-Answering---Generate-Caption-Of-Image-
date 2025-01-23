# Import libraries
import streamlit as st
from PIL import Image
from utils.config_loader import ConfigLoader
from model.vqr_model import Virtual_Question_Answering
from custom_logger.custom_logging import CustomLogger

# Create a custom logger for the Streamlit app
logger = CustomLogger.create_custom_logger("StreamlitAPP")

st.set_page_config(
    page_title="Virtual Question Answering - Image Caption",
    layout="centered",  # This ensures the content is centered on the page
    page_icon="🖼️"
)

# Function to initialize the VQA model
def initialize_vqa(config_path="config.yaml"):
    progress_bar = st.progress(0)  # Taskbar added here for initialization progress
    st.write("Initializing the Virtual Question Answering Model...", )
    
    try:
        # Load configuration from the specified config file
        config = ConfigLoader.config_loader(config_path)
        progress_bar.progress(33)
        
        if not config:
            st.error("Failed to load configuration. Please check config.yaml.")
            logger.error("Failed to load configuration.")
            return None
        
        # Initialize and load the VQA model
        VQA = Virtual_Question_Answering()
        progress_bar.progress(66)
        VQA.load_model()
        progress_bar.progress(100)
        
        st.title("Virtual Question Answering - Image Captioning")
        st.write("Upload an image to generate a caption")
        return VQA
    except Exception as e:
        st.error(f"Failed to load the VQA model: {e}")
        logger.error(f"Error loading VQA model: {e}")
        return None

# Function to process the uploaded image
def process_uploaded_image(uploaded_file, vqa_model):
    if uploaded_file is None:
        return

    try:
        # Open the uploaded image and resize it
        image = Image.open(uploaded_file)
        image = image.resize((600, 600))  # Resize the image to make it smaller (adjust size as needed)

        # Container layout with image and caption below it
        with st.container():
            # Image section with responsive layout
            st.markdown("""
            <div style="text-align: center; max-width: 100%; margin: 0 auto; padding: 10px;">
                <img src="data:image/png;base64,{}" width="100%" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); max-width: 600px;">
            </div>
            """.format(image_to_base64(image)), unsafe_allow_html=True)

            # Caption section
            with st.spinner("Generating caption..."):
                caption = vqa_model.predict_model(uploaded_file)
                if caption:
                    # Display generated caption under the image
                    st.markdown(f"""
                    <div style="max-width: 600px; margin: 20px auto; padding: 15px; border: 2px solid #4CAF50; border-radius: 12px; background-color: #f9f9f9; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); font-size: 18px; color: #333;">
                        <strong>Generated Caption :</strong><br>{caption}
                    </div>
                    """, unsafe_allow_html=True)
                    logger.info("Caption generated successfully.")
                else:
                    st.error("Failed to generate caption.")
                    logger.error("Failed to generate caption.")
    except Exception as e:
        # Detailed error message for image processing
        st.error(f"An error occurred while processing the image: {e}")
        logger.error(f"Error processing image: {e}")

# Function to run the Streamlit app
def run_streamlit_app():
    # Initialize the VQA model
    vqa_model = initialize_vqa()
    if not vqa_model:
        return
    
    # File uploader to upload an image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        process_uploaded_image(uploaded_file, vqa_model)

# Function to convert the image to base64 format for embedding it in the HTML
import io
import base64

def image_to_base64(image):
    img_buffer = io.BytesIO()
    image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return base64.b64encode(img_buffer.read()).decode('utf-8')