"""
Gemini File Search Client Wrapper

This module provides a wrapper around Google's Gemini API with File Search capabilities.
It handles file uploads, store management, and query operations with built-in retry logic.
"""

import os
import time
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging

from google import genai
from google.genai import types
from google.api_core import retry
from google.api_core.exceptions import GoogleAPIError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiFileSearchClient:
    """
    Wrapper for Gemini API with File Search Store capabilities.
    
    This client manages:
    - File uploads to File Search Stores
    - Store creation and management
    - Query operations with File Search tool integration
    - Automatic retry logic for transient failures
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Google AI API key. If not provided, reads from GOOGLE_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY must be set in environment or passed to constructor")
        
        # Initialize the client with the API key
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.0-flash-exp"
        
    @retry.Retry(predicate=retry.if_exception_type(GoogleAPIError))
    def create_file_search_store(self, display_name: str) -> types.FileSearchStore:
        """
        Create a new File Search Store.
        
        Args:
            display_name: Human-readable name for the store
            
        Returns:
            FileSearchStore object with name and metadata
        """
        try:
            logger.info(f"Creating File Search Store: {display_name}")
            store = self.client.file_search_stores.create(
                display_name=display_name
            )
            logger.info(f"Created store: {store.name}")
            return store
        except Exception as e:
            logger.error(f"Error creating store: {e}")
            raise
    
    @retry.Retry(predicate=retry.if_exception_type(GoogleAPIError))
    def upload_file_to_store(
        self, 
        file_path: str, 
        store_name: str,
        mime_type: Optional[str] = None
    ) -> types.File:
        """
        Upload a file to a specific File Search Store.
        
        Args:
            file_path: Path to the file to upload
            store_name: Name of the File Search Store (e.g., "file_search_stores/{id}")
            mime_type: MIME type of the file (auto-detected if not provided)
            
        Returns:
            File object with upload details
        """
        try:
            logger.info(f"Uploading file {file_path} to store {store_name}")
            
            # Upload file to the store
            file = self.client.file_search_stores.upload_to_file_search_store(
                path=file_path,
                store_name=store_name,
                display_name=Path(file_path).name,
                mime_type=mime_type
            )
            
            logger.info(f"File uploaded successfully: {file.name}")
            return file
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            raise
    
    @retry.Retry(predicate=retry.if_exception_type(GoogleAPIError))
    def list_stores(self) -> List[types.FileSearchStore]:
        """
        List all File Search Stores.
        
        Returns:
            List of FileSearchStore objects
        """
        try:
            logger.info("Listing File Search Stores")
            stores = list(self.client.file_search_stores.list())
            logger.info(f"Found {len(stores)} stores")
            return stores
        except Exception as e:
            logger.error(f"Error listing stores: {e}")
            raise
    
    @retry.Retry(predicate=retry.if_exception_type(GoogleAPIError))
    def get_store(self, store_name: str) -> types.FileSearchStore:
        """
        Get details of a specific File Search Store.
        
        Args:
            store_name: Name of the store
            
        Returns:
            FileSearchStore object
        """
        try:
            logger.info(f"Getting store: {store_name}")
            store = self.client.file_search_stores.get(name=store_name)
            return store
        except Exception as e:
            logger.error(f"Error getting store: {e}")
            raise
    
    @retry.Retry(predicate=retry.if_exception_type(GoogleAPIError))
    def delete_store(self, store_name: str) -> None:
        """
        Delete a File Search Store.
        
        Args:
            store_name: Name of the store to delete
        """
        try:
            logger.info(f"Deleting store: {store_name}")
            self.client.file_search_stores.delete(name=store_name)
            logger.info(f"Store deleted: {store_name}")
        except Exception as e:
            logger.error(f"Error deleting store: {e}")
            raise
    
    @retry.Retry(predicate=retry.if_exception_type(GoogleAPIError))
    def query_with_file_search(
        self, 
        query: str, 
        store_name: str,
        temperature: float = 0.1
    ) -> Dict[str, Any]:
        """
        Query the model with File Search tool enabled.
        
        This uses the Gemini model with the File Search tool to answer questions
        based on the files in the specified store.
        
        Args:
            query: The question to ask
            store_name: Name of the File Search Store to search in
            temperature: Model temperature (0.0-1.0, lower is more deterministic)
            
        Returns:
            Dict containing:
                - answer: The model's response text
                - citations: List of citations with snippets and metadata
        """
        try:
            logger.info(f"Querying with File Search: {query[:100]}...")
            
            # Configure the File Search tool with the specific store
            tool = types.Tool(
                file_search=types.FileSearchTool(
                    store=types.FileSearchStore(
                        name=store_name
                    )
                )
            )
            
            # Generate content with File Search enabled
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=query,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    tools=[tool]
                )
            )
            
            # Extract answer text
            answer = ""
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'text'):
                            answer += part.text
            
            # Extract citations with grounding metadata
            citations = []
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                
                # Check for grounding metadata
                if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                    grounding = candidate.grounding_metadata
                    
                    # Extract grounding chunks
                    if hasattr(grounding, 'grounding_chunks') and grounding.grounding_chunks:
                        for chunk in grounding.grounding_chunks:
                            citation_data = {
                                "text": "",
                                "source": "Unknown"
                            }
                            
                            # Get the chunk content
                            if hasattr(chunk, 'retrieved_context') and chunk.retrieved_context:
                                context = chunk.retrieved_context
                                if hasattr(context, 'text'):
                                    citation_data["text"] = context.text
                                if hasattr(context, 'title'):
                                    citation_data["source"] = context.title
                                if hasattr(context, 'uri'):
                                    citation_data["uri"] = context.uri
                            
                            citations.append(citation_data)
            
            result = {
                "answer": answer,
                "citations": citations
            }
            
            logger.info(f"Query completed. Found {len(citations)} citations")
            return result
            
        except Exception as e:
            logger.error(f"Error querying with File Search: {e}")
            raise
    
    def get_supported_mime_types(self) -> Dict[str, str]:
        """
        Get mapping of file extensions to MIME types.
        
        Returns:
            Dict mapping file extension to MIME type
        """
        return {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".txt": "text/plain",
            ".json": "application/json",
            ".py": "text/x-python",
            ".js": "text/javascript",
            ".ts": "text/typescript",
            ".java": "text/x-java",
            ".cpp": "text/x-c++",
            ".c": "text/x-c",
            ".go": "text/x-go",
            ".rs": "text/x-rust",
            ".md": "text/markdown",
            ".html": "text/html",
            ".css": "text/css",
            ".xml": "application/xml",
            ".yaml": "text/yaml",
            ".yml": "text/yaml",
        }
    
    def detect_mime_type(self, file_path: str) -> str:
        """
        Detect MIME type from file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            MIME type string
        """
        ext = Path(file_path).suffix.lower()
        mime_types = self.get_supported_mime_types()
        return mime_types.get(ext, "application/octet-stream")
