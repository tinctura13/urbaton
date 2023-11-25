import requests
from PIL import Image
from io import BytesIO

def download_image(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an HTTPError for unsuccessful status codes
        return BytesIO(response.content)
    except requests.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"An error occurred: {err}")

def send_image_to_api(image_stream, api_url):
    response = requests.post(api_url, files={"file": image_stream})
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception(f"API request failed with status code {response.status_code}")

def display_image(image_stream):
    image = Image.open(image_stream)
    image.show()

def main():
    image_url = input("Enter the image URL: ")
    api_endpoint = "http://localhost:8000/process-image/"

    try:
        # Download the image from the URL
        image_stream = download_image(image_url)

        # Send the image to the FastAPI endpoint
        processed_image_stream = send_image_to_api(image_stream, api_endpoint)

        # Display the processed image
        display_image(processed_image_stream)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

