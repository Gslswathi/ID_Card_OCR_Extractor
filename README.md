
ID Card OCR Extractor (Offline AI Microservice)

This project is a Python-based offline microservice that extracts structured data from student college ID cards. It uses Tesseract OCR along with regex-based field extraction, built using FastAPI and designed to run locally or inside a Docker container.

Features:
- Offline OCR using Tesseract (no cloud dependency)
- Accepts base64-encoded ID card image input
- Extracts fields: name, college, roll_number, branch, valid_upto
- Field extraction using regex
- Returns confidence score and extraction status
- REST API powered by FastAPI (/extract, /docs, /health)
- Docker support for deployment

Project Structure:
idcard-ocr-extractor/
├── main.py               # FastAPI app with /extract endpoint
├── ocr_utils.py          # Image preprocessing + Tesseract OCR
├── requirements.txt      # Python dependencies
├── README.txt            # This file

API Usage:

POST /extract

Request:
{
  "user_id": "id_card_sample_1",
  "image_base64": "<base64_encoded_image>"
}

Response:
{
  "user_id": "id_card_sample_1",
  "extracted_fields": {
    "name": "Anjali Sharma",
    "roll_number": "23205Q0890",
    "college": "RGMCET Nandyal",
    "branch": "CSE",
    "valid_upto": "2028"
  },
  "confidence_score": 0.95,
  "missing_fields": [],
  "status": "success",
  "base64_preview": "<original base64 re-encoded image string>"
}

How to Run Locally:

1. Clone the Repo:
git clone https://github.com/Gslswathi/idcard-ocr-extractor.git
cd idcard-ocr-extractor

2. Set Up Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Run the Server:
uvicorn main:app --reload

Visit: http://localhost:8000/docs to test the API.

Testing Tips:
- Use valid and clearly scanned ID card images
- Convert image to base64 using:
    Python: base64.b64encode(open("file.jpg", "rb").read()).decode()
    Online: https://www.base64-image.de/
- If OCR results are incomplete, check image clarity or try preprocessing

Docker Support (Optional):

1. Build Image:
docker build -t idcard-extractor .

2. Run Container:
docker run -p 8000:8000 idcard-extractor

Visit http://localhost:8000/docs
