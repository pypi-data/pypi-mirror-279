import math
import re
import warnings
from kbrainsdk.validation.ingest import validate_ingest_onedrive, validate_ingest_sharepoint, validate_ingest_status, validate_ingest_rfp_responses, validate_ingest_pipeline_status
from kbrainsdk.apibase import APIBase
from docx import Document
import PyPDF2
import pandas as pd

class Ingest(APIBase):

    def __init__(self, *args, **kwds):
        self.FILE_HANDLER = {
            "pdf": self.pdf_handler,
            "txt": self.txt_handler,
            "docx": self.docx_handler
        }
        self.TXT_CHARACTERS_PER_PAGE = 2000  # Adjust this value based on your assumption
        self.HEADER_CUTOFF = 200
        self.DOCX_CHARACTERS_PER_PAGE = 500
        return super().__init__(*args, **kwds)

    def get_supported_file_types(self):
        return list(self.FILE_HANDLER.keys())

    def ingest_onedrive(self, email, token, client_id, oauth_secret, tenant_id, environment):

        payload = {
            "email": email,
            "token": token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_ingest_onedrive(payload)

        path = f"/ingest/onedrive/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def ingest_sharepoint(self, host, site, token, client_id, oauth_secret, tenant_id, environment):

        payload = {
            "host": host,
            "site": site,
            "token": token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_ingest_sharepoint(payload)

        path = f"/ingest/sharepoint/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def ingest_rfp_responses(self, proposal_id, email, assertion_token, client_id, oauth_secret, tenant_id, environment, datasets=[]):

        payload = {
            "proposal_id": proposal_id,
            "email": email,
            "token": assertion_token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id,
            "datasets": datasets
        }

        validate_ingest_rfp_responses(payload)

        path = f"/ingest/rfp/responses/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def get_status(self, datasource):

        payload = {
            "datasource": datasource 
        }

        validate_ingest_status(payload)

        path = f"/ingest/status/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
    
    def get_pipeline_status(self, run_id):

        payload = {
            "run_id": run_id 
        }

        validate_ingest_pipeline_status(payload)

        path = f"/ingest/pipeline/run/status/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def convert_site_to_datasource(self, site):
        # Remove special characters and replace spaces with hyphens
        site_name = re.sub(r'[^a-zA-Z0-9\s]', '', site)
        site_name = site_name.replace(' ', '-')
        return f"sharepoint-{site_name.lower().replace('.', '-')}"

    def convert_email_to_datasource(self, email):
        return f"drive-{email.lower().replace('@', '-at-').replace('.', '-')}"

    def pdf_handler(self, local_filepath, document_df, filename):
        with open(local_filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in range(len(pdf_reader.pages)):
                extracted_page = pdf_reader.pages[page]
                text = extracted_page.extract_text()
                sections = re.split(r'\t+|\n{2,}|\s{2,}', text)
                sections = list(filter(lambda x: x.strip() != '', sections))
                for text, section, section_type, paragraph in self.paragraph_generator(sections):
                    page_df = pd.DataFrame({
                        "text": [text],
                        "section": [section],
                        "file": [filename],
                        "page": [page + 1],
                        "type": [section_type],
                        "paragraph": [paragraph]
                    })
                    document_df = pd.concat([document_df, page_df], axis='rows')
        document_df.reset_index(drop=True, inplace=True)
        return document_df

    def estimate_pages(self, character_count, average_characters_per_page):
        return character_count // average_characters_per_page + 1


    def txt_handler(self, local_filepath, document_df, filename):
        with open(local_filepath, 'r') as file:
            text = file.read()
            character_count = len(text)
            estimated_pages = self.estimate_pages(character_count, self.TXT_CHARACTERS_PER_PAGE)
            paragraphs = re.split(r'\t+|\n{2,}|\s{2,}', text)
            paragraphs = list(filter(lambda x: x.strip() != '', paragraphs))
            total_sections = len(paragraphs)
            sections_per_page = math.ceil(total_sections / estimated_pages)
            for text, section, section_type, paragraph in self.paragraph_generator(paragraphs):
                page_df = pd.DataFrame({
                    "text": [text],
                    "section": [section],
                    "file": [filename],
                    "page": [int(math.ceil(section / sections_per_page))],
                    "type": [section_type],
                    "paragraph": [paragraph]
                })
                document_df = pd.concat([document_df, page_df], axis='rows')
        document_df.reset_index(drop=True, inplace=True)
        return document_df

    def docx_handler(self, local_filepath, document_df, filename):
        doc = Document(local_filepath)
        paragraphs = [p.text for p in doc.paragraphs]
        for text, section, section_type, paragraph in self.paragraph_generator(paragraphs):
            page_df = pd.DataFrame({
                "text": [text],
                "section": [section],
                "file": [filename],
                "page": [section // self.DOCX_CHARACTERS_PER_PAGE + 1],
                "type": [section_type],
                "paragraph": [paragraph]
            })
            document_df = pd.concat([document_df, page_df], axis='rows')
        document_df.reset_index(drop=True, inplace=True)
        return document_df
    
    def paragraph_generator(self, textblocks):
        previous_section = None
        paragraphs = 0
        sections = 0
        for text in textblocks:
            section_type = "header" if len(text) < self.HEADER_CUTOFF else "paragraph"
            if previous_section != "header":
                paragraphs += 1
            previous_section = section_type
            sections += 1
            yield text, sections, section_type, paragraphs
    ################################
    ##FLAWED AND DEPRECATED
    ################################
    def count_paragraphs(self, x, paragraph_count):
        warnings.warn(f"count_paragraphs contains bugs is deprecated. Use paragraph_generator instead to count paragraphs", DeprecationWarning, stacklevel=2)
        if x == "header":
            if paragraph_count["count"] == 0:
                return 1
            return paragraph_count["count"]
        
        paragraph_count["count"] += 1
        return int(paragraph_count["count"])

    def process_document(self, local_filepath, document_name, extension):
        try:
            document_df = pd.DataFrame({"file":[], "page":[], "section":[], "text":[], "type":[], "paragraph": []})
            filename = f"{document_name.strip()}.{extension}"
            document_df = self.FILE_HANDLER[extension.lower()](local_filepath, document_df, filename)
            metafile = f"{local_filepath.replace(f'.{extension}','')}_meta.csv"
            document_df.reset_index(inplace=True, drop=True)
            document_df.to_csv(metafile, escapechar="\\", index=False)                
            return metafile
        except Exception as ex:
            return str(ex)
            
