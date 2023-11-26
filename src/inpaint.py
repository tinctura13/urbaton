from models.model_manager import ModelManager
from models.owlvit import detect_classes
from PIL import Image
import time
from loguru import logger
import numpy as np
from schema import Config, HDStrategy
import cv2


lama_model = ModelManager(name="lama", device="cpu")


def inpaint(image: Image, class_name: str, prompt: str, threshold: float):
    np_image, np_mask = detect_classes(image, prompt, threshold)
        
    # Check if the mask is empty (all black)
    if not np.any(np_mask):
        logger.info(f"No objects detected for '{class_name}', skipping inpainting.")
        return Image.fromarray(cv2.cvtColor(np_image.astype(np.uint8), cv2.COLOR_BGR2RGB))

    config = Config(
        hd_strategy=HDStrategy.ORIGINAL,
        hd_strategy_crop_margin=10,
        hd_strategy_crop_trigger_size=1000,
        hd_strategy_resize_limit=2048,
    )

    # Perform inpainting with LaMa model
    start = time.time()
    res_np_img = lama_model(np_image, np_mask, config=config)
    logger.info(f"Processing time for '{class_name}': {(time.time() - start) * 1000}ms")

    # Update the image with the result for the next iteration
    return Image.fromarray(cv2.cvtColor(res_np_img.astype(np.uint8), cv2.COLOR_BGR2RGB))