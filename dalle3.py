#!/usr/bin/env python3

import logging
from openai import OpenAI
import requests
import sys
from datetime import datetime
import select

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

client = OpenAI()

# Check if there's any input from stdin
if select.select([sys.stdin,],[],[],0.0)[0]:
    # Get the prompt from stdin
    prompt = sys.stdin.read().strip()
else:
    print("No Prompt. Exiting.")
    sys.exit()

try:
    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      n=1,
      size="1024x1024"
    )

    # Log the entire response
    logger.info(response)

    # Get the URL of the first image from the response
    image_url = response.data[0].url

    # Download the image
    image_response = requests.get(image_url)

    # Create a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Write the image data to a file with a unique name
    with open(f'dark_{timestamp}.jpg', 'wb') as f:
        f.write(image_response.content)

except Exception as e:
    # Log any exceptions that occur
    logger.error(e)