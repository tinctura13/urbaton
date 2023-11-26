import requests
from PIL import Image
from inpaint import inpaint



url = input("Enter image URL: ")
image = Image.open(requests.get(url, stream=True).raw)

# List of texts to iterate over
texts = [
    ("Рекламный баннер", "photo of an advertising sign on a building", 0.09),
    ("Вывеска", "photo of an Signboard on a building", 0.08),
    ("Штендер", "photo of a Pavement sign", 0.06),
    ("Световой короб", "photo of an advertising lightbox sign on building", 0.06),
    ("Кондиционер", "Split-type AC units", 0.05),
    # ("class_name", "prompt", threshold: float),
]

for text_item in texts:
    image = inpaint(image, text_item[0], text_item[1], text_item[2])


image.show()
