#!/usr/bin/env python3
"""
Simple test script for PlantNet API endpoint verification
"""

import requests
import json

def test_plantnet_api():
    """Test PlantNet API endpoint directly"""
    print("Testing PlantNet API endpoint...")
    
    # PlantNet API configuration
    api_key = "2b10nNH1NQjSRx5ToTvNSEAV"
    
    # Test different endpoints
    endpoints = [
        "https://my.plantnet.org/api/v2/species",
        "https://my.plantnet.org/api/v2/species/search",
        "https://my.plantnet.org/api/v2/identify",
        "https://my.plantnet.org/api/v2/projects"
    ]
    
    for endpoint in endpoints:
        print(f"\nTesting endpoint: {endpoint}")
        try:
            params = {
                "api-key": api_key,
                "limit": 5
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                print(f"Response type: {type(data)}")
                if isinstance(data, dict) and 'data' in data:
                    print(f"Data length: {len(data['data']) if isinstance(data['data'], list) else 'Not a list'}")
            else:
                print(f"Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"Exception: {e}")
    
    # Test with a specific search
    print(f"\nTesting species search with 'tomato'...")
    try:
        search_url = "https://my.plantnet.org/api/v2/species"
        params = {
            "q": "tomato",
            "api-key": api_key,
            "limit": 5
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response structure: {json.dumps(data, indent=2)[:500]}...")
        else:
            print(f"Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_plantnet_api() 