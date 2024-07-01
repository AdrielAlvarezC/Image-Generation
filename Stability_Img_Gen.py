import base64
import requests
import os
import cv2
import numpy as np

# Function to check if the image is blurred
def is_blurred(image_path, threshold=100.0):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    return fm < threshold

# Function to generate and save image
def generate_and_save_image(prompt, image_count, non_blurred_count):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    
    # Update the prompt in the request body
    body = {
      "steps": 40,
      "width": 1024,
      "height": 1024,
      "cfg_scale": 5,
      "samples": 1,
      "text_prompts": [
        {
          "text": prompt,
          "weight": 1
        },
        {
          "text": "bad",
          "weight": -1
        }
      ],
    }

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": "WRITE USER KEY HERE",
    }
    
    response = requests.post(
      url,
      headers=headers,
      json=body,
    )
    
    if response.status_code != 200:
        raise Exception("Non-200 response: " + response.text)
    
    data = response.json()
    
    # Make sure the output directory exists
    if not os.path.exists("./out"):
        os.makedirs("./out")
    
    # Save image data
    for i, image in enumerate(data["artifacts"]):
        image_path = f'./out/txt2img_{prompt.replace(" ", "_")}_{image_count}_{image["seed"]}.png'
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
        
        # Check if the image is blurred
        if not is_blurred(image_path):
            non_blurred_count += 1
            if non_blurred_count > 5:
                os.remove(image_path)
                break
        else:
            os.remove(image_path)
    return non_blurred_count

# Main program
user_prompt = input("Enter your image prompt: ")
non_blurred_count = 0
i = 0
while non_blurred_count < 5:
    try:
        non_blurred_count = generate_and_save_image(user_prompt, i, non_blurred_count)
        print(f"Image {i+1} processed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    i += 1
    # Add a delay if needed to comply with API rate limits
    # time.sleep(1)

print("5 non-blurred images saved.")

