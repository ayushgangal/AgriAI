#!/usr/bin/env python3
"""
Test script for PlantNet API integration
"""

import asyncio
import sys
import os
import json

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.crop_api_service import CropAPIService
from app.core.database import get_db

async def test_plantnet_api():
    """Test the PlantNet API integration"""
    print("Testing PlantNet API integration...")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Create CropAPIService instance
        crop_api_service = CropAPIService(db)
        
        # Test fetching crops from PlantNet API
        print("Fetching crops from PlantNet API...")
        plantnet_crops = await crop_api_service.fetch_crops_from_plantnet_api(limit=5)
        
        print(f"Successfully fetched {len(plantnet_crops)} crops from PlantNet API")
        
        if plantnet_crops:
            print("\nSample crops from PlantNet API:")
            for i, crop in enumerate(plantnet_crops[:3], 1):
                print(f"\n{i}. {crop['crop_name'].title()} ({crop['scientific_name']})")
                print(f"   Category: {crop['crop_category']}")
                print(f"   Variety: {crop['crop_variety']}")
                print(f"   Temperature: {crop['optimal_temperature_min']}°C - {crop['optimal_temperature_max']}°C")
                print(f"   Rainfall: {crop['optimal_rainfall_min']}mm - {crop['optimal_rainfall_max']}mm")
                print(f"   Growing Season: {crop['growing_season']}")
                if 'plantnet_info' in crop:
                    print(f"   PlantNet ID: {crop['plantnet_info'].get('plantnet_id', 'N/A')}")
                    print(f"   Family: {crop['plantnet_info'].get('family', 'N/A')}")
                    print(f"   Common Names: {', '.join(crop['plantnet_info'].get('common_names', []))}")
        
        # Test fetching from all APIs
        print("\n" + "="*50)
        print("Testing fetch from all APIs...")
        all_crops = await crop_api_service.get_all_crops_from_apis(limit_per_source=3)
        
        print(f"Total unique crops fetched: {len(all_crops)}")
        
        # Group by source
        sources = {}
        for crop in all_crops:
            source = crop.get('data_source', 'unknown')
            if source not in sources:
                sources[source] = []
            sources[source].append(crop['crop_name'])
        
        print("\nCrops by source:")
        for source, crops in sources.items():
            print(f"  {source}: {len(crops)} crops - {', '.join(crops)}")
        
        # Test database sync (optional - uncomment to test)
        # print("\n" + "="*50)
        # print("Testing database sync...")
        # sync_result = await crop_api_service.sync_crops_to_database(all_crops)
        # print(f"Sync result: {sync_result}")
        
        return True
        
    except Exception as e:
        print(f"Error testing PlantNet API: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()

async def test_usda_api():
    """Test the USDA API integration"""
    print("\n" + "="*50)
    print("Testing USDA API integration...")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Create CropAPIService instance
        crop_api_service = CropAPIService(db)
        
        # Test fetching crops from USDA API
        print("Fetching crops from USDA API...")
        usda_crops = await crop_api_service.fetch_crops_from_usda_api(limit=5)
        
        print(f"Successfully fetched {len(usda_crops)} crops from USDA API")
        
        if usda_crops:
            print("\nSample crops from USDA API:")
            for i, crop in enumerate(usda_crops[:3], 1):
                print(f"\n{i}. {crop['crop_name'].title()} ({crop['scientific_name']})")
                print(f"   Category: {crop['crop_category']}")
                print(f"   Variety: {crop['crop_variety']}")
                print(f"   Temperature: {crop['optimal_temperature_min']}°C - {crop['optimal_temperature_max']}°C")
                print(f"   Rainfall: {crop['optimal_rainfall_min']}mm - {crop['optimal_rainfall_max']}mm")
        
        return True
        
    except Exception as e:
        print(f"Error testing USDA API: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()

async def main():
    """Main test function"""
    print("Starting API integration tests...")
    print("="*50)
    
    # Test PlantNet API
    plantnet_success = await test_plantnet_api()
    
    # Test USDA API
    usda_success = await test_usda_api()
    
    print("\n" + "="*50)
    print("Test Results:")
    print(f"PlantNet API: {'✓ PASS' if plantnet_success else '✗ FAIL'}")
    print(f"USDA API: {'✓ PASS' if usda_success else '✗ FAIL'}")
    
    if plantnet_success and usda_success:
        print("\n🎉 All tests passed! The crop API integration is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main()) 