import os
import sys

from urllib.parse import urlparse
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from Parser4LLM.pdf_converter import PDFConverter
from Parser4LLM.word_converter import DOCXConverter
from Parser4LLM.ppt_converter import PPTXConverter
from Parser4LLM.url_converter import URLConverter

class Parser4LLM:
    def check_file_type(self, path):
        parsed_url = urlparse(path)
        if parsed_url.scheme in ['http', 'https']:
            _, file_extension = os.path.splitext(parsed_url.path)
            file_extension = file_extension.lower()
            if file_extension == '.pdf':
                return 'PDF (URL)'
            else:
                return 'URL'
        
        _, file_extension = os.path.splitext(path)
        file_extension = file_extension.lower()

        if file_extension == '.docx':
            return 'Word'
        elif file_extension == '.pptx':
            return 'PowerPoint'
        elif file_extension == '.pdf':
            return 'PDF'
        else:
            return 'Unknown'
        
    def convert(self, file_path):
        file_type = self.check_file_type(file_path)
        if file_type == 'Word':
            converter = DOCXConverter()
            md_content = converter.convert(file_path)
            return md_content
        elif file_type == 'PDF':
            converter = PDFConverter(file_path)
            md_content = converter.convert()
            return md_content
        elif file_type == 'PowerPoint':
            converter = PPTXConverter()
            md_content = converter.convert(file_path)
            return md_content
        elif file_type == 'URL':
            converter = URLConverter()
            md_html, md_url = converter.convert(file_path)
            return md_html, md_url
        else:
            print("Please check the file...")
            return "Please Check the file type..."