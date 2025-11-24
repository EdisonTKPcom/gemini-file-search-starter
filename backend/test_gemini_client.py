"""
Unit tests for Gemini File Search Client
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from gemini_client import GeminiFileSearchClient


class TestGeminiFileSearchClient:
    """Test suite for GeminiFileSearchClient"""
    
    @patch('gemini_client.genai.Client')
    def test_init_with_api_key(self, mock_client):
        """Test client initialization with API key"""
        client = GeminiFileSearchClient(api_key="test-key")
        assert client.api_key == "test-key"
        mock_client.assert_called_once_with(api_key="test-key")
    
    @patch('gemini_client.genai.Client')
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'env-key'})
    def test_init_with_env_var(self, mock_client):
        """Test client initialization with environment variable"""
        client = GeminiFileSearchClient()
        assert client.api_key == "env-key"
    
    def test_init_without_api_key(self):
        """Test client initialization fails without API key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="GOOGLE_API_KEY must be set"):
                GeminiFileSearchClient()
    
    @patch('gemini_client.genai.Client')
    def test_detect_mime_type(self, mock_client):
        """Test MIME type detection"""
        client = GeminiFileSearchClient(api_key="test-key")
        
        assert client.detect_mime_type("test.pdf") == "application/pdf"
        assert client.detect_mime_type("test.txt") == "text/plain"
        assert client.detect_mime_type("test.py") == "text/x-python"
        assert client.detect_mime_type("test.json") == "application/json"
        assert client.detect_mime_type("test.unknown") == "application/octet-stream"
    
    @patch('gemini_client.genai.Client')
    def test_get_supported_mime_types(self, mock_client):
        """Test getting supported MIME types"""
        client = GeminiFileSearchClient(api_key="test-key")
        
        mime_types = client.get_supported_mime_types()
        assert isinstance(mime_types, dict)
        assert ".pdf" in mime_types
        assert ".txt" in mime_types
        assert ".py" in mime_types
    
    @patch('gemini_client.genai.Client')
    def test_create_file_search_store(self, mock_client):
        """Test creating a File Search Store"""
        mock_store = Mock()
        mock_store.name = "file_search_stores/test123"
        
        mock_client_instance = mock_client.return_value
        mock_client_instance.file_search_stores.create.return_value = mock_store
        
        client = GeminiFileSearchClient(api_key="test-key")
        store = client.create_file_search_store("Test Store")
        
        assert store.name == "file_search_stores/test123"
        mock_client_instance.file_search_stores.create.assert_called_once_with(
            display_name="Test Store"
        )
    
    @patch('gemini_client.genai.Client')
    def test_list_stores(self, mock_client):
        """Test listing File Search Stores"""
        mock_store1 = Mock()
        mock_store1.name = "file_search_stores/test1"
        mock_store2 = Mock()
        mock_store2.name = "file_search_stores/test2"
        
        mock_client_instance = mock_client.return_value
        mock_client_instance.file_search_stores.list.return_value = [mock_store1, mock_store2]
        
        client = GeminiFileSearchClient(api_key="test-key")
        stores = client.list_stores()
        
        assert len(stores) == 2
        assert stores[0].name == "file_search_stores/test1"
        assert stores[1].name == "file_search_stores/test2"
    
    @patch('gemini_client.genai.Client')
    def test_delete_store(self, mock_client):
        """Test deleting a File Search Store"""
        mock_client_instance = mock_client.return_value
        
        client = GeminiFileSearchClient(api_key="test-key")
        client.delete_store("file_search_stores/test123")
        
        mock_client_instance.file_search_stores.delete.assert_called_once_with(
            name="file_search_stores/test123"
        )
    
    @patch('gemini_client.genai.Client')
    def test_query_with_file_search(self, mock_client):
        """Test querying with File Search"""
        # Mock response structure
        mock_part = Mock()
        mock_part.text = "This is the answer"
        
        mock_content = Mock()
        mock_content.parts = [mock_part]
        
        mock_candidate = Mock()
        mock_candidate.content = mock_content
        mock_candidate.grounding_metadata = None
        
        mock_response = Mock()
        mock_response.candidates = [mock_candidate]
        
        mock_client_instance = mock_client.return_value
        mock_client_instance.models.generate_content.return_value = mock_response
        
        client = GeminiFileSearchClient(api_key="test-key")
        result = client.query_with_file_search(
            query="What is the capital of France?",
            store_name="file_search_stores/test123"
        )
        
        assert result["answer"] == "This is the answer"
        assert isinstance(result["citations"], list)
    
    @patch('gemini_client.genai.Client')
    def test_query_with_citations(self, mock_client):
        """Test querying with citations"""
        # Mock response with grounding metadata
        mock_part = Mock()
        mock_part.text = "Paris is the capital"
        
        mock_content = Mock()
        mock_content.parts = [mock_part]
        
        mock_context = Mock()
        mock_context.text = "Paris is the capital of France"
        mock_context.title = "geography.pdf"
        mock_context.uri = "file://geography.pdf"
        
        mock_chunk = Mock()
        mock_chunk.retrieved_context = mock_context
        
        mock_grounding = Mock()
        mock_grounding.grounding_chunks = [mock_chunk]
        
        mock_candidate = Mock()
        mock_candidate.content = mock_content
        mock_candidate.grounding_metadata = mock_grounding
        
        mock_response = Mock()
        mock_response.candidates = [mock_candidate]
        
        mock_client_instance = mock_client.return_value
        mock_client_instance.models.generate_content.return_value = mock_response
        
        client = GeminiFileSearchClient(api_key="test-key")
        result = client.query_with_file_search(
            query="What is the capital of France?",
            store_name="file_search_stores/test123"
        )
        
        assert result["answer"] == "Paris is the capital"
        assert len(result["citations"]) == 1
        assert result["citations"][0]["source"] == "geography.pdf"
        assert "Paris" in result["citations"][0]["text"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
