from openai import OpenAI
import base64
import cv2
from PIL import Image
import os
import tempfile
from accounts.azam_module.unique_frames import extract_unique_frames
from dotenv import load_dotenv
load_dotenv()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def vqa_data(video_path,output_dir_for_frames,output_dir_for_text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    MODEL="gpt-4o"
    frames = extract_unique_frames(video_path, output_dir_for_frames)
    if frames:
        for image_path in frames:
            base64_image = encode_image(image_path)
            response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates detailed descriptions based on provided images."},
                {"role": "user", "content": [
                    {"type": "text", "text": "I would like you to generate a detailed description about the provided image so that I can answer any questions related to it based on the description you generate."},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"}
                    }
                ]}
            ],
            temperature=0.0,)
            print(f"ip = {image_path}")
            file_path = image_path.split('\\')[-1].split('.jpeg')[0]
            file_path = os.path.join(output_dir_for_text, f"{file_path}.txt")
            with open(file_path, 'w') as file:
                file.write(response.choices[0].message.content)






