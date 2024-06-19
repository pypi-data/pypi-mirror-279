from typing import Union, Dict

import requests

from vulavula.common.response_handler import APIResponseHandler
from vulavula.config import settings
from vulavula.models.types import CreateKnowledgeBaseRequest
import requests
from PyPDF2 import PdfReader

class VulavulaSearch:

    def __init__(self, client_token,  base_url=None, session=None):
        self.base_url = base_url if base_url else settings.BASE_URL
        self.headers = {
            "X-CLIENT-TOKEN": client_token,
            "Content-Type": "application/json"
        }
        self._handle_response = APIResponseHandler.handle_response
        self.session = session if session else requests.Session()
        self.session.headers.update(self.headers)
        self.collection = None

    def create_collection(self, data: Union[str, CreateKnowledgeBaseRequest]):
        """
        Sends a request to the API to create a knowledge base with the provided data.

        Parameters:
            data (Union[str, CreateKnowledgeBaseRequest]): An instance of CreateKnowledgeBaseRequest containing the data to create a knowledge base.
                                             This ensures that the 'collection' keys exist.

        Returns:
            dict: The response from the server after processing the knowledge base creation request.

        Example:
            data = CreateKnowledgeBaseRequest(collection="myCollection")
            try:
                kb_result = client.create_knowledge_base(data)
                print("Knowledge Base Creation Result:", kb_result)
            except Exception as e:
                print(f"Error during knowledge base creation: {e}")
        """
        if isinstance(data, CreateKnowledgeBaseRequest):
            data = data.__dict__
        url = f"{self.base_url}/search/create-knowledgebase"
        response = self.session.post(url, headers=self.headers, json=data)
        self.collection = data['collection']
        return self._handle_response(response)



    def upload_and_extract_text(self, file_path: str, language: str) -> dict:
        # Open the PDF file in binary mode
        with open(file_path, 'rb') as file:
            # Create a PDF file reader object
            pdf_reader = PdfReader(file)

            # Initialize an empty string to hold the extracted text
            extracted_text = ''

            # Loop through each page in the PDF file and extract the text
            for page in pdf_reader.pages:
                extracted_text += page.extract_text()

            # Split the extracted text into paragraphs (chunks)
            paragraphs = extracted_text.split('\n')

            url = f"{self.base_url}/search/create-documents"
            data = {
                "documents": paragraphs,
                "collection": self.collection,
                "language": language
            }

            # Send the POST request
            response = self.session.post(url,headers=self.headers ,json=data)

            # Handle the response as needed
            # For example, you might want to check if the request was successful
            if response.status_code == 200:
                print("Documents created successfully.")
            else:
                print(f"Failed to create documents. Status code: {response.status_code}")

        return self._handle_response(response)

    def search_query(self,query:str,language:str)->dict:
        url = f"{self.base_url}/search/search"
        data = {
            "query": query,
            "language": language,
            "collection": self.collection
        }
        response = self.session.post(url, headers=self.headers, json=data)
        return self._handle_response(response)
