import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from groundx import Document, GroundX
from dotenv import load_dotenv

load_dotenv()

class DocumentSearchToolInput(BaseModel):
    query: str = Field(..., description="Query to search the document.")

class DocumentSearchTool(BaseTool):
    name: str = "DocumentSearchTool"
    description: str = "Search the document for the given query."
    args_schema: Type[BaseModel] = DocumentSearchToolInput
    model_config = ConfigDict(extra="allow")
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.client = GroundX(api_key=os.getenv("GROUNDX_API_KEY"))
        self.bucket_id = self._create_bucket()
        self.process_id = self._upload_document()
    
    def _create_bucket(self):
        response = self.client.buckets.create(name="agentic_rag")
        return response.bucket.bucket_id

    def _upload_document(self):
        ingest = self.client.ingest(
            documents=[
                Document(
                    bucket_id=self.bucket_id,
                    file_name=os.path.basename(self.file_path),
                    file_path=self.file_path,
                    file_type="pdf",
                )
            ]
        )
        return ingest.ingest.process_id

    def _run(self, query: str) -> str:
        status_response = self.client.documents.get_processing_status_by_id(
            process_id=self.process_id
        )
        if status_response.ingest.status != "complete":
            return "Document is still being processed..."
        search_response = self.client.search.content(
            id=self.bucket_id,
            query=query,
            n=10,
            verbosity=2
        )
        formatted_results = ""
        for result in search_response.search.results:
            formatted_results += f"{result.text}\n____\n"
        return formatted_results.rstrip('____\n')
