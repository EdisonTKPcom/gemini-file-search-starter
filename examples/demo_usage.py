"""
Example Usage Script for Gemini File Search Starter

This script demonstrates how to use the API programmatically.
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

def upload_file(file_path, create_new_store=True, store_name=None):
    """Upload a file to the File Search Store"""
    url = f"{API_BASE_URL}/upload"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'create_new_store': str(create_new_store).lower(),
        }
        if store_name:
            data['store_name'] = store_name
        
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()


def query_files(query, store_name, temperature=0.1):
    """Query files in a File Search Store"""
    url = f"{API_BASE_URL}/query"
    
    payload = {
        "query": query,
        "store_name": store_name,
        "temperature": temperature
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def list_stores():
    """List all File Search Stores"""
    url = f"{API_BASE_URL}/stores/list"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def main():
    print("=== Gemini File Search Demo ===\n")
    
    # Example 1: Upload a file
    print("1. Uploading sample files...")
    try:
        # Upload first file and create a store
        result1 = upload_file("ai_introduction.txt", create_new_store=True)
        print(f"   ✓ Uploaded: {result1['file_info']['name']}")
        print(f"   ✓ Store: {result1['store_name']}")
        store_name = result1['store_name']
        
        # Upload more files to the same store
        result2 = upload_file("company_data.json", create_new_store=False, store_name=store_name)
        print(f"   ✓ Uploaded: {result2['file_info']['name']}")
        
        result3 = upload_file("sample_code.py", create_new_store=False, store_name=store_name)
        print(f"   ✓ Uploaded: {result3['file_info']['name']}")
        
        print("\n   Waiting for indexing to complete...")
        time.sleep(2)
        
    except Exception as e:
        print(f"   ✗ Upload failed: {e}")
        return
    
    # Example 2: Query the files
    print("\n2. Querying files...\n")
    
    queries = [
        "What is the difference between narrow AI and general AI?",
        "How many employees work in the Engineering department?",
        "Explain the fibonacci function in the code",
    ]
    
    for i, q in enumerate(queries, 1):
        print(f"   Question {i}: {q}")
        try:
            result = query_files(q, store_name)
            print(f"   Answer: {result['answer'][:200]}...")
            if result['citations']:
                print(f"   Citations: {len(result['citations'])} source(s)")
                for citation in result['citations']:
                    print(f"      - {citation['source']}")
            print()
        except Exception as e:
            print(f"   ✗ Query failed: {e}\n")
    
    # Example 3: List stores
    print("\n3. Listing all stores...")
    try:
        stores = list_stores()
        print(f"   Found {len(stores)} store(s):")
        for store in stores:
            print(f"      - {store['display_name']} ({store['name']})")
    except Exception as e:
        print(f"   ✗ Failed to list stores: {e}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
