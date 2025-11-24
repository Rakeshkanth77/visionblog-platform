import markdown  # pip add if needed

class BlogFormatter:  # HLD: Content Aggregator
    @staticmethod
    def format(raw_output, image_bytes):
        """Format to Markdown/HTML with image embed (Core Feature: Download)."""
        # Embed image as Markdown
        from base64 import b64encode
        img_b64 = b64encode(image_bytes).decode()
        md_content = f"![Uploaded Image](data:image/png;base64,{img_b64})\n\n{raw_output}"
        
        # To HTML
        html_content = markdown.markdown(md_content)
        return md_content, html_content