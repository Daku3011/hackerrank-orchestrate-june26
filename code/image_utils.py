import base64
from pathlib import Path
from PIL import Image
import io


def encode_image(image_path, max_size=2048):
    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size
    if max(w, h) > max_size:
        scale = max_size / max(w, h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def validate_image(image_path):
    path = Path(image_path)
    if not path.exists():
        return False
    try:
        img = Image.open(path)
        img.verify()
        return True
    except Exception:
        return False
