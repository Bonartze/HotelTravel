import requests
from bs4 import BeautifulSoup

# The webpage URL
url = 'https://www.booking.com/city/eg/cairo.html'  # Replace with the actual URL

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')  # or 'html.parser'

    # Find all <img> tags
    images = soup.find_all('img')

    # List to store image URLs
    image_urls = []

    # Extract the 'src' attribute and resolve relative URLs
    for img in images:
        img_src = img.get('src')
        if img_src:
            img_url = requests.compat.urljoin(url, img_src)
            image_urls.append(img_url)

    # Print the image URLs
    for img_url in image_urls:
        print(img_url)
else:
    print(f"Failed to retrieve the webpage: {response.status_code}")