# img_dlder
`img_dlder` is a Python package designed for downloading and saving images from various sources.

## Installation
You can install `img_dlder` via pip:
```bash
pip install img_dlder
```

```bash
pip install requests Pillow tqdm
```

### Example Usage:
```python
from img_dlder.img_dler import ImgDownloader
# Initialize ImgDownloader
downloader = ImgDownloader()
# Specify the search query and the number of images to fetch and download
query = "cat"
num_images = 10
destination_directory = "./downloaded_images"
# Download images based on the query
try:
    downloader.dl_imgs(query, num_images, destination_directory)
        print(f"Successfully downloaded and saved images to {destination_directory}")
except ValueError as e:
    print(f"Error: {e}")
```
%ls
