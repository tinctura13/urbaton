from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
import io
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def process(image: Image.Image) -> Image.Image:
    # Prepare to draw text
    draw = ImageDraw.Draw(image)
    text = "PROCESSED"
    
    # Calculate proportional font size (80% of image width)
    width, height = image.size
    proportional_font_size = int((width * 0.8) / len(text))

    # Load font (adjust the path to your font file if necessary)
    mf = ImageFont.truetype('font.ttf', proportional_font_size)

    # Calculate position for the text (centered)
    
    x = width / 2 - proportional_font_size * 4
    y = height / 2 - proportional_font_size * 2

    # Add text to the original image
    draw.text((x, y), text, font=mf, fill=(255, 255, 255))

    return image


@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Process image
    processed_image = process(image)

    # Convert processed image to byte stream
    img_byte_arr = io.BytesIO()
    processed_image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    return StreamingResponse(io.BytesIO(img_byte_arr), media_type="image/jpeg")


origins = [
    "http://localhost:3000",  # Allow your frontend running on localhost:3000
    "http://localhost:8000",  # If you also have frontend components on this port
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)