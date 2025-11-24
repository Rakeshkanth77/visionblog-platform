import requests
import base64
from io import BytesIO
from PIL import Image

class AIGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.euron.one/api/v1/euri/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def generate_blog(self, image_bytes, user_prompt, style, tone, length):
        """Generate a blog post based on the image and user preferences."""
        # Convert image to base64
        image = Image.open(BytesIO(image_bytes))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Create the prompt
        prompt_text = (
            f"Analyze this image and generate a {length}-word blog post.\n"
            f"Topic: {user_prompt}\n"
            f"Style: {style}\n"
            f"Tone: {tone}\n"
            f"Image: data:image/png;base64,{img_b64}"
        )
        
        # Make API request
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            "model": "gemini-2.5-pro",
            "max_tokens": 5000,
            "temperature": 0.7
        }
        

        
        response = requests.post(self.url, headers=self.headers, json=payload)
        data = response.json()
        
        # Debug: Print response to see actual structure
        print("API Response:", data)
        
        # Extract the generated text
        # Extract the generated text
        try:
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                message = choice.get("message", {})
                
                # Check if content exists
                if "content" in message and message["content"]:
                    return message["content"]
                else:
                    finish_reason = choice.get("finish_reason", "unknown")
                    return f"API returned empty response. Finish reason: {finish_reason}. Tokens used: {data.get('usage', {})}"
            else:
                return f"Error: {data.get('error', 'No choices in response')}"
        except Exception as e:
            return f"Error parsing response: {str(e)}"