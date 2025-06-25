from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ocr__utils import extract_text
import base64
import re
import tempfile

app = FastAPI()

# Input schema
class OCRRequest(BaseModel):
    user_id: str
    image_base64: str

# Patterns to match fields 
patterns = {
    "name": r"(?:Name|Nama|Student Name)[\s:]*([A-Za-z\s]+)",
    "roll_number": r"(?:Roll No|Student ID|ID)[\s:]*([\dA-Z]+)",
    "college": r"(College(?: of)? [A-Za-z\s]+)",
    "branch": r"(?:Branch|Dept)[\s:]*([A-Za-z\s]+)",
    "valid_upto": r"(?:Valid upto|Valid till|Upto)[\s:]*([0-9]{4})"
}

@app.post("/extract")
def extract_fields(data: OCRRequest):
    try:
        # Decode and write image to a temporary file
        image_bytes = base64.b64decode(data.image_base64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpeg") as tmp_file:
            tmp_file.write(image_bytes)
            tmp_path = tmp_file.name

        # Extract OCR text
        raw_text = extract_text(tmp_path)
        print(f"\n==== Raw OCR Text for {data.user_id} ====\n{raw_text}\n")

        extracted = {}
        missing_fields = []

        for key, pattern in patterns.items():
            match = re.search(pattern, raw_text, re.IGNORECASE)
            if match:
                extracted[key] = match.group(1).strip()
            else:
                missing_fields.append(key)

        status = "success" if not missing_fields else "partial_success"
        confidence_score = 0.95 if status == "success" else 0.2

        # ✅ Add full base64 preview from saved image
        with open(tmp_path, "rb") as f:
            base64_preview = base64.b64encode(f.read()).decode("utf-8")
        # ✅ Console log the length for debugging
        print(f"Base64 Preview Length for {data.user_id}: {len(base64_preview)} characters")

        return {
            "user_id": data.user_id,
            "extracted_fields": extracted,
            "confidence_score": confidence_score,
            "missing_fields": missing_fields,
            "status": status,
            "base64_preview": base64_preview
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
