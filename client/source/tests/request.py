import requests

with open("png.png", "rb") as image:
    request = requests.post(
        "http://localhost:8000/identify",
        files={"file": ("image.png", image, "image/png")},
    )
