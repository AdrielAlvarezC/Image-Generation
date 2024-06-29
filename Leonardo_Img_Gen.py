import requests
import json
import time

# Function to create a generation of images
def create_image_generation(api_key, model_id, prompt, width, height, num_images):
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "prompt": prompt,
        "modelId": model_id,
        "width": width,
        "height": height,
        "num_images": num_images  # Set the number of images to generate
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        print("Response Body:", response.text)  # Print the response body for more details
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")

# Function to retrieve generated images
def get_generated_images(api_key, generation_id):
    url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        print("Response Body:", response.text)  # Print the response body for more details
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")

# Replace these variables with your own values
YOUR_API_KEY = "users key goes here" #   Replace with your User Dev Key
MODEL_ID = "users model id goes here"  # Replace with your model ID
PROMPT = "user prompt goes here"
WIDTH = 512
HEIGHT = 512
NUM_IMAGES = 5  # Number of images to generate

# Create image generation
generation_response = create_image_generation(YOUR_API_KEY, MODEL_ID, PROMPT, WIDTH, HEIGHT, NUM_IMAGES)

if generation_response:
    print(json.dumps(generation_response, indent=4))
    generation_id = generation_response.get("generationId")
    print(f"Generation ID: {generation_id}")
else:
    print("Failed to get a valid response from the image generation request.")

# Wait a bit for the generation to complete
time.sleep(10)  # Adjust the sleep time as needed

# Retrieve the generated images
if generation_id:
    images_response = get_generated_images(YOUR_API_KEY, generation_id)
    if images_response:
        print(json.dumps(images_response, indent=4))
    else:
        print("Failed to get a valid response from the image retrieval request.")
else:
    print("No generation ID received, cannot retrieve images.")


