import os
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from tqdm.notebook import tqdm
from fetch_images.fetch_images import fetch_images as fetch

def download_images(urls, dest, image_name):
    """
    Downloads images from a list of URLs to a specified destination directory.

    Args:
    - urls (list): List of URLs of images to download.
    - dest (str): Destination directory where images will be saved.
    - image_name (str): Prefix to use for naming downloaded images.
    """
    os.makedirs(dest, exist_ok=True)  # Ensure the destination directory exists
    
    with tqdm(total=len(urls), desc="Downloading images", unit="image", dynamic_ncols=True) as pbar:
        for index, url in enumerate(urls, start=1):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Check for bad status codes
                
                img_data = response.content
                img_file = BytesIO(img_data)
                
                img = Image.open(img_file)
                
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
                file_name = f'{image_name}_{timestamp}.jpg'
                save_path = os.path.join(dest, file_name)
                
                # Handle filename conflicts
                while os.path.exists(save_path):
                    print(f'File {file_name} already exists.')
                    action = input("""What do you want to do now:
                    s: Skip
                    m: Modify filename
                    u: Use timestamp for uniqueness
                    Choice: """)
                    
                    if action == 's':
                        print(f'Skipping {file_name}')
                        break
                    elif action == 'm':
                        file_name = input('Enter new filename (without extension): ') + '.jpg'
                        save_path = os.path.join(dest, file_name)
                    elif action == 'u':
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
                        file_name = f'{image_name}_{timestamp}.jpg'
                        save_path = os.path.join(dest, file_name)
                    else:
                        print('Invalid choice, please choose again.')
                
                if os.path.exists(save_path):
                    pbar.update(1)
                    continue

                img.save(save_path)
                pbar.update(1)
                
            except requests.exceptions.RequestException as e:
                print(f'Failed to download {url}: {e}')
                pbar.update(1)
            
            except IOError as e:
                print(f'Failed to process {url}: {e}')
                pbar.update(1)

    print(f"Successfully downloaded and saved images to {dest}")


class ImgDownloader:
    """
    A class to facilitate downloading images based on a query.
    Methods:
    - dl_imgs(qry, num, dest): Downloads images based on the specified query and saves them to the destination directory.
    """
    def __init__(self):
        self._urls = None
    def dl_imgs(self, qry, num, dest):
        """
        Downloads images based on a query and saves them to the destination directory.
        Args:
        - qry (str): Query string used to fetch images.
        - num (int): Number of images to download.
        - dest (str): Destination directory where images will be saved.
        """
        if not dest:
            raise ValueError('Destination directory must be provided!')
        res = fetch(qry, num)
        count = res['total_count']
        if count == 0:
            raise ValueError(f"No images found for query '{qry}'")
        if num > count:
            raise ValueError(f"Only {count} images found for query '{qry}', but {num} requested")
        self._urls = res['img_urls']
        download_images(self._urls, dest, qry)
