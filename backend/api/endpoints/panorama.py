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
async def get_panorama(part: int = Query(None, description="Part of the panorama (1-8), omit for full image")):
    """Returns the panorama image, either in full or a specific part."""

    try:
        image = Image.open("./panorama.jpg")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Panorama image not found")

    if part is None:
        # Return the full image
        return FileResponse("./panorama.jpg")
    
    if part < 1 or part > TOTAL_PARTS:
        raise HTTPException(status_code=400, detail=f"Invalid part number. Choose between 1 and {TOTAL_PARTS}")

    # Calculate part dimensions
    w, h = image.size
    part_width = w // TOTAL_PARTS
    left = (part - 1) * part_width
    right = left + part_width

    # Crop the image
    cropped_image = image.crop((left, 0, right, h))

    # Serve the cropped image
    img_byte_array = io.BytesIO()
    cropped_image.save(img_byte_array, format='JPEG')
    img_byte_array.seek(0)

    return Response(content=img_byte_array.read(), media_type="image/jpeg")