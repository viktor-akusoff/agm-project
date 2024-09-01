from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import FileResponse
from PIL import Image
import io

router = APIRouter(
    prefix='/panorama',
    tags=["Panorama management"]
)

# Define the total number of parts
TOTAL_PARTS = 8

@router.get('')
async def get_panorama(part: int = Query(description="Part of the panorama (0-8), omit for full image",)):
    """Returns the panorama image, either in full or a specific part."""

    try:
        image = Image.open("./panorama.jpg")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Panorama image not found")

    result_image = image.copy()

    if  part < 0 or part > TOTAL_PARTS:
        raise HTTPException(status_code=400, detail=f"Invalid part number. Choose between 1 and {TOTAL_PARTS}")

    if part:
        w, h = image.size
        part_width = w // TOTAL_PARTS
        left = (part - 1) * part_width
        right = left + part_width
        result_image = image.crop((left, 0, right, h))

    img_byte_array = io.BytesIO()
    result_image.save(img_byte_array, format='JPEG')
    img_byte_array.seek(0)

    return Response(content=img_byte_array.read(), media_type="image/jpeg")