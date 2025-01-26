import cv2
from groq import Groq
import base64
import os
from dotenv import load_dotenv
import json
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

output_filename='streamScreen/captured_photo.png'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def capture_photo(camera_index=0):
    """
    Captures a photo from the specified camera index and saves it to a file.

    Args:
        camera_index (int): The index of the camera to use (default is 0).
        output_filename (str): The file name to save the captured photo.

    Returns:
        bool: True if the photo was successfully captured and saved, False otherwise.
    """
    # Open the camera
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera with index {camera_index}.")
        return False

    # Capture a single frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture photo.")
        cap.release()
        return False

    # Save the captured frame to a file
    cv2.imwrite(output_filename, frame)
    print(f"Photo saved as {output_filename}")

    # Release the camera resource
    cap.release()
    cv2.destroyAllWindows()
    # return True


def see_photo(prompt):
    filepath = 'streamScreen/captured_photo.png'
    capture_photo(camera_index=2)
    target_img = f"data:image/jpeg;base64,{encode_image(filepath)}"
    # print(target_img)

    completion = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Prompt: {prompt} ; Ignore the IVCam logo and if you didn't want or can't answer just say I don't know \n\nYour token is limited to 1000"
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
    return img_results
# # Example usage
# if __name__ == '__main__':
#     success = capture_photo(camera_index=2, output_filename='ivcam_photo.png')
#     if success:
#         print("Photo capture successful!")
#     else:
#         print("Photo capture failed.")

see_photo("describe the image. read any text found. determine the programming language. solve or answer the question")
