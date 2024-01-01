#!/usr/bin/env python3

import io
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

def generate_image(prompt):
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

        # Check if the request was successful
        if image_response.status_code == 200:
            # Get the content of the response
            image_data = image_response.content

            # Read the image data into a byte array
            image_bytes = io.BytesIO(image_data)

            return image_bytes

        else:
            logger.error(f"Failed to download image: {image_response.status_code}")
            return None

    except Exception as e:
        # Log any exceptions that occur
        logger.error(e)
        return None