from fastapi import FastAPI, File, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import io

from inpaint import inpaint

app = FastAPI()

@app.post("/process-image/")
async def process_image(file: bytes = File(...), texts: list[tuple] = None):
    if not texts:
        raise HTTPException(status_code=400, detail="Texts not provided")

    try:
        # Read image from bytes
        image = Image.open(io.BytesIO(file))

        # Process each text item
        for text_item in texts:
            image = inpaint(image, *text_item)

        # Convert the PIL Image to bytes for the response
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        return StreamingResponse(io.BytesIO(img_byte_arr), media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
