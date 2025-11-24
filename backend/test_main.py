"""
Unit tests for FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import io

from main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def mock_gemini_client():
    """Mock Gemini client fixture"""
    with patch('main.gemini_client') as mock:
        yield mock


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data


class TestUploadEndpoint:
    """Test file upload endpoint"""
    
    def test_upload_file_success(self, client, mock_gemini_client):
        """Test successful file upload"""
        # Mock store creation
        mock_store = Mock()
        mock_store.name = "file_search_stores/test123"
        mock_gemini_client.create_file_search_store.return_value = mock_store
        
        # Mock file upload
        mock_file = Mock()
        mock_file.name = "files/test_file"
        mock_gemini_client.upload_file_to_store.return_value = mock_file
        mock_gemini_client.detect_mime_type.return_value = "text/plain"
        
        # Create test file
        file_content = b"Test file content"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        data = {"create_new_store": True}
        
        response = client.post("/upload", files=files, data=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True
        assert "test.txt" in result["message"]
    
    def test_upload_without_gemini_client(self, client):
        """Test upload fails without Gemini client"""
        with patch('main.gemini_client', None):
            file_content = b"Test file content"
            files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
            
            response = client.post("/upload", files=files)
            
            assert response.status_code == 503


class TestQueryEndpoint:
    """Test query endpoint"""
    
    def test_query_success(self, client, mock_gemini_client):
        """Test successful query"""
        # Mock query response
        mock_result = {
            "answer": "Paris is the capital of France",
            "citations": [
                {
                    "text": "Paris is the capital",
                    "source": "geography.pdf",
                    "uri": None
                }
            ]
        }
        mock_gemini_client.query_with_file_search.return_value = mock_result
        
        request_data = {
            "query": "What is the capital of France?",
            "store_name": "file_search_stores/test123",
            "temperature": 0.1
        }
        
        response = client.post("/query", json=request_data)
        
        assert response.status_code == 200
        result = response.json()
        assert "Paris" in result["answer"]
        assert len(result["citations"]) == 1
        assert result["citations"][0]["source"] == "geography.pdf"
    
    def test_query_without_gemini_client(self, client):
        """Test query fails without Gemini client"""
        with patch('main.gemini_client', None):
            request_data = {
                "query": "Test query",
                "store_name": "file_search_stores/test123"
            }
            
            response = client.post("/query", json=request_data)
            
            assert response.status_code == 503


class TestStoreEndpoints:
    """Test store management endpoints"""
    
    def test_list_stores(self, client, mock_gemini_client):
        """Test listing stores"""
        # Mock stores
        mock_store1 = Mock()
        mock_store1.name = "file_search_stores/test1"
        mock_store1.display_name = "Test Store 1"
        
        mock_store2 = Mock()
        mock_store2.name = "file_search_stores/test2"
        mock_store2.display_name = "Test Store 2"
        
        mock_gemini_client.list_stores.return_value = [mock_store1, mock_store2]
        
        response = client.get("/stores/list")
        
        assert response.status_code == 200
        stores = response.json()
        assert len(stores) == 2
        assert stores[0]["name"] == "file_search_stores/test1"
        assert stores[1]["display_name"] == "Test Store 2"
    
    def test_delete_store(self, client, mock_gemini_client):
        """Test deleting a store"""
        mock_gemini_client.delete_store.return_value = None
        
        response = client.delete("/stores/test123")
        
        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True
    
    def test_delete_store_with_full_name(self, client, mock_gemini_client):
        """Test deleting a store with full name"""
        mock_gemini_client.delete_store.return_value = None
        
        response = client.delete("/stores/file_search_stores/test123")
        
        assert response.status_code == 200


class TestSupportedTypesEndpoint:
    """Test supported types endpoint"""
    
    def test_get_supported_types(self, client, mock_gemini_client):
        """Test getting supported file types"""
        mock_gemini_client.get_supported_mime_types.return_value = {
            ".pdf": "application/pdf",
            ".txt": "text/plain",
            ".py": "text/x-python"
        }
        
        response = client.get("/supported-types")
        
        assert response.status_code == 200
        result = response.json()
        assert "supported_extensions" in result
        assert "mime_types" in result
        assert ".pdf" in result["supported_extensions"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
