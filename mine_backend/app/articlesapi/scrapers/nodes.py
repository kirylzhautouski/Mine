class Nodes:

    @staticmethod
    def create_image_node(image_src, caption):
        return {
            '@type': 'ImageNode',
            'src': image_src,
            'caption': caption,
        }

    @staticmethod
    def create_video_node(video_src):
        return {
            '@type': 'VideoNode',
            'src': video_src,
        }

    @staticmethod
    def create_text_node(text):
        if not text:
            return None

        return {
            '@type': 'TextNode',
            'text': text,
        }
