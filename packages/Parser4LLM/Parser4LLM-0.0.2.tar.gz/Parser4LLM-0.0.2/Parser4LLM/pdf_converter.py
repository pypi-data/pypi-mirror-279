import os
import pymupdf4llm
import PyPDF2
import json
import requests
import uuid

class PDFConverter:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def is_ocr_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            page = reader.pages[0]
            text = page.extract_text()
            if text.strip():
                return True  # OCR PDF (text can be extracted)
            else:
                return False  # Non-OCR PDF (no extractable text)
    
    def upload_to_cloudflare(self, file_path):
        os.environ["CLOUDFLARE_API_URL"] = "https://workspace.askjunior2023.workers.dev/upload/"
        os.environ["CLOUDFLARE_CDN_URL"] = "https://pub-cc8438e664ef4d32a54c800c7c408282.r2.dev/"
        unique_id = str(uuid.uuid4())
        upload_url = os.environ["CLOUDFLARE_API_URL"] + unique_id + ".pdf"
        with open(file_path, 'rb') as f:
            headers = {'Content-Type': 'application/pdf'}
            upload_response = requests.put(upload_url, data=f.read(), headers=headers)
            upload_response.raise_for_status()
        new_url = f"{os.environ['CLOUDFLARE_CDN_URL']}{unique_id}.pdf"
        return new_url, unique_id
    
    def marker_converter_Non_ocr(self, pdf_url, file_id):
        url = "https://askjunior--split-pdf-split-pdf.modal.run"
        payload = json.dumps({
        "pdf_url": pdf_url,
        "file_id": file_id,
        "workspace_id": "rec_cpf9vp6225mchnjkhaq0",
        "collection_name": "Non-Ocr-Markdown"
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    def convert(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        is_ocr = self.is_ocr_pdf(self.file_path)
        if is_ocr:
            md_content = pymupdf4llm.to_markdown(self.file_path)
            return md_content
        else:
            pdf_url, file_id = self.upload_to_cloudflare(self.file_path)
            md_content = self.marker_converter_Non_ocr(pdf_url, file_id)
            md_url = f"https://pub-cc8438e664ef4d32a54c800c7c408282.r2.dev/{file_id}.md"
            return md_url