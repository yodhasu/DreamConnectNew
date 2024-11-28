import token
import pyuac
import tokenize
import nltk
import re
from nltk.tokenize import word_tokenize
from urlextract import URLExtract
from transformers import pipeline

from groq import Groq
import base64
from dotenv import load_dotenv
import os
import stat

summarizer = pipeline("summarization", model="t5-small", device="cuda")
load_dotenv()

def encode_image(image_path):
    # os.chmod(image_path, 0o777)
    if not os.access(image_path, os.R_OK):
        raise PermissionError(f"Cannot read file: {image_path}")
    
    with open(image_path, "rb") as image_file:  # Open in binary mode
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = input("String: ")



def vision(img):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe what's in the image in short. Your token is limited to 100"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img
                        }
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=500,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content


usrinput = "img link https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png"
path_pattern = r'["\']?([a-zA-Z]:[\\\/](?!https?:\/\/)[^<>:"|?*]+(?:[\\\/][^<>:"|?*]+)*)["\']?'

# input = input.replace("\\", "/")
# tokenized = word_tokenize(input)
# tokenized

match = re.findall(path_pattern, usrinput)
print(match)
extractor = URLExtract()
if match:
    file_path = match[0]
    print(file_path)
    
    # Replace backslashes with forward slashes in the file path
    processed_path = file_path.replace("\\", "/")
    
    # Remove the file path from the original text
    remaining_text = usrinput.replace(file_path, "").strip()
    
    # Tokenize the remaining text
    tokenized_text = word_tokenize(remaining_text)
    base64_image = encode_image(processed_path)

    local_image = f"data:image/jpeg;base64,{base64_image}"
    # Print the results
    print("File Path:", processed_path)
    print("Remaining Text:", tokenized_text)
else:
    urls = extractor.find_urls(image_path)
    if len(urls) < 1:
        print("No file path found in the input text.")
    else:
        print(''.join(urls))

def summ():
    visionres = vision(local_image)

    return visionres

print(image_path)
print(match)
res = summ()
print(res)