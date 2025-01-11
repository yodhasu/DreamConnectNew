from groq import Groq
import base64
import os
from dotenv import load_dotenv
import json
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def see_screenshot(prompt):
    filepath = 'streamScreen/screen.jpg'
    target_img = f"data:image/jpeg;base64,{encode_image(filepath)}"
    # print(target_img)

    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"The image is the screenshot of user screen. Try to describe what's on the screen, what application or window that currently opened (Discord, Notepad, Web Browser, Youtube, etc.), and any other important information. Additional prompt: {prompt} Your token is limited to 1000"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": target_img
                        }
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=2042,
        top_p=1,
        stream=False,
        stop=None,
    )
    img_results = completion.choices[0].message.content
    result_json = json.dumps({"result": img_results})
    print("Results: ", img_results)
    print("Results JSON: ", result_json)
    return result_json

see_screenshot("focus on the text and describe what is it")