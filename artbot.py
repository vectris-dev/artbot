import os
import csv
from io import BytesIO
import requests
from PIL import Image
from openai import OpenAI
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# The number of times to process the entire CSV file
run_count = 1

# The guidance text is prepended to the prompt to prevent openAI from modifying the prompt
guidance = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: "
use_guidance = True

# The delay between image generations to avoid rate limits
delay = 2
# The delay before retrying after an error
retry_delay = 10

# The output directory
output_dir = "output"

# Add this with the other configuration variables at the top
image_size = "1792x1024"  # Can be "1024x1024", "1792x1024", or "1024x1792"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def generate_image(prompt):

    if(use_guidance):
        prompt=f"{guidance}{prompt}"

    response = client.images.generate(
        model="dall-e-3",
        prompt= prompt,
        n=1,
        size=image_size
    )
    image_url = response.data[0].url
    revised_prompt = response.data[0].revised_prompt
    return image_url, revised_prompt

def download_image(image_url, filename):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save(filename)

def save_prompt_to_txt(revised_prompt, txt_filename):
    with open(txt_filename, 'w') as txt_file:
        txt_file.write(revised_prompt)

def process_prompts():
    with open("example.csv", mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            prompt = row[0].strip()
            num_images = int(row[1].strip()) if row[1].strip().isdigit() else 1

            if not prompt:
                continue

            print(f"Generating {num_images} image(s) for prompt: '{prompt}'")

            for i in range(num_images):
                success = False
                while not success:
                    try:
                        image_url, revised_prompt = generate_image(prompt)

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        image_filename = os.path.join(output_dir, f"{timestamp}.png")
                        txt_filename = os.path.join(output_dir, f"{timestamp}.txt")
                        
                        print(f"Saving image {i+1} of {num_images} as: {image_filename}")
                        download_image(image_url, image_filename)

                        print(f"Saving revised prompt for image {i+1} of {num_images} as: {txt_filename}")
                        save_prompt_to_txt(revised_prompt, txt_filename)

                        success = True

                        print(f"Waiting for {delay} seconds before the next image...")
                        time.sleep(delay)

                    except Exception as e:
                        print(f"Error occurred: {e}. Retrying after {retry_delay} seconds...")
                        time.sleep(retry_delay)

for run in range(run_count):
    print(f"Starting run {run+1} of {run_count}")
    process_prompts()
    print(f"Completed run {run+1} of {run_count}")
