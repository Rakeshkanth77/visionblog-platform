from PIL import Image
import io

from matplotlib import image

class ImageProcessor:
    @staticmethod
    def validate(image_file):
        """Validate the uploaded image file format."""
        if not image_file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            return False, "Unsupported file format. Please upload a JPG or PNG image."
        if image_file.size > 5 * 1024 * 1024:  # 5MB limit
            return False
        return True, "Image is valid."
    
    @staticmethod
    def preprocess(image_file):
        """Preprocess the image for model input."""
        image = Image.open(image_file)
        image = image.resize((512, 512))  # Resize to model expected size
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        return img_buffer.getvalue()
    
