import os
import json
import shutil
from ocr__utils import extract_text
import re

# Setup
IMAGE_FOLDER = "test_images"
OUTPUT_FOLDER = "ocr_results"
JSON_FILE = os.path.join(OUTPUT_FOLDER, "results.json")
TEXT_FILE = os.path.join(OUTPUT_FOLDER, "results.txt")

# Create or clean output folder
if os.path.exists(OUTPUT_FOLDER):
    shutil.rmtree(OUTPUT_FOLDER)
os.makedirs(OUTPUT_FOLDER)

# Regex patterns
patterns = {
    "name": r"(?:Name|Nama|Student Name)[\s:]*([A-Za-z\s]+)",
    "roll_number": r"(?:Roll No|Student ID|ID)[\s:]*([\dA-Z]+)",
    "college": r"(College(?: of)? [A-Za-z\s]+)",
    "branch": r"(?:Branch|Dept)[\s:]*([A-Za-z\s]+)",
    "valid_upto": r"(?:Valid upto|Valid till|Upto)[\s:]*([0-9]{4})"
}

all_results = []
txt_lines = []

# Loop through images
for image_name in os.listdir(IMAGE_FOLDER):
    if image_name.lower().endswith(('.jpeg', '.jpg', '.png')):
        image_path = os.path.join(IMAGE_FOLDER, image_name)

        # Extract OCR text
        raw_text = extract_text(image_path)
        print(f"\n==== Raw Text for {image_name} ====\n{raw_text}\n=============================\n")

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

        result = {
            "user_id": image_name,
            "extracted_fields": extracted,
            "confidence_score": confidence_score,
            "missing_fields": missing_fields,
            "status": status
        }

        all_results.append(result)

        # Prepare TXT line
        txt_lines.append(f"User ID: {image_name}")
        for k, v in extracted.items():
            txt_lines.append(f"{k}: {v}")
        txt_lines.append(f"Confidence: {confidence_score}")
        txt_lines.append(f"Missing Fields: {', '.join(missing_fields)}")
        txt_lines.append(f"Status: {status}")
        txt_lines.append("-" * 30)

# Write to output files
with open(JSON_FILE, "w") as jf:
    json.dump(all_results, jf, indent=4)

with open(TEXT_FILE, "w") as tf:
    tf.write("\n".join(txt_lines))

print(f"\n✅ Done. Check output files in '{OUTPUT_FOLDER}/'")