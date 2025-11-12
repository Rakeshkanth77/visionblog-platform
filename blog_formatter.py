import markdown

class BlogFormatter:
    @staticmethod
    def format(raw_output, image_bytes):
        """Format the raw blog output into markdown with embedded image."""
        # Embed the image in markdown
        from base64 import b64encode
        img_b64 = b64encode(image_bytes).decode()
        md_content = f"![Blog Image](data:image/png;base64,{img_b64})\n\n {raw_output}"

        html_content = markdown.markdown(md_content)
        return 
