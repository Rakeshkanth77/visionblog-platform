
from euriai import EuriaiClient
import os
import base64
from io import BytesIO
from PIL import Image


api_key = os.getenv('euri-c243bba3cbdc9b7bb96b5c1f8ebbd74fe717da1138b22baf62ad0c9e2dd604d6')
class AIGenerator:
    def __init__(self, api_key):
        # self.llm = ChatOpenAI(model_name="gpt-4o",  openai_api_key=os.getenv('euri-c243bba3cbdc9b7bb96b5c1f8ebbd74fe717da1138b22baf62ad0c9e2dd604d6'))
        self.llm = EuriaiClient(
            api_key=api_key,  # Pass the api_key parameter
            model="gpt-4.1-nano"  # or any model from the supported list
        )
    def generate_blog(self, image_bytes, user_prompt, style, tone, length):
        """Generate a blog post based on the image and user preferences."""
        image = Image.open(BytesIO(image_bytes))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        prompt = self.llm.generate_completion(
            "Analyze this image: [Image: data:image/png;base64,{img_b64}] "
            "Generate a {length}-word blog post on {user_prompt}. Style: {style}, Tone: {tone}. "
            "Integrate image description and visuals."
        )         
        chain = prompt | self.llm
        response = chain.invoke({
            "img_b64": img_str,
            "user_prompt": user_prompt,
            "style": style,
            "tone": tone,
            "length": length
        })
        return response.content
    


