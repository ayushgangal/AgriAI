# Crop API Integration

This document describes the crop API integration feature that allows the AgriAI system to fetch crop data from multiple external sources, providing a comprehensive variety of crops for recommendations and management.

## Overview

The crop API integration system fetches crop data from multiple sources:
- **PlantNet API** - Real plant identification and information API
- **USDA Plants Database** - Free public API for plant information
- **Agricultural Research Database** - Mock implementation for additional crops
- **Local Database** - Existing crop data from JSON files

## Features

### 1. Multi-Source Data Fetching
- Fetches crop data from multiple APIs simultaneously
- Combines and deduplicates data from different sources
- Provides comprehensive crop information

### 2. Real PlantNet API Integration
- Uses actual PlantNet API with provided API key
- Fetches scientific names, common names, and taxonomic information
- Converts PlantNet data to our crop format

### 3. USDA API Integration
- Free and public API for plant information
- Provides additional crop data and scientific classifications
- No authentication required

### 4. Enhanced Crop Recommendations
- More detailed recommendations considering multiple factors
- Soil type and pH level considerations
- Comprehensive suitability scoring

## API Endpoints

### 1. Refresh Crop Database
```
GET /api/crops/refresh
```
Refreshes the crop database by fetching from all external APIs and syncing to the local database.

### 2. Fetch Crops from APIs
```
GET /api/crops/fetch?limit_per_source=20
```
Fetches crops from external APIs without saving to the database (preview mode).

### 3. Get Data Sources
```
GET /api/crops/sources
```
Returns information about available crop data sources.

### 4. Get Crop Categories
```
GET /api/crops/categories
```
Returns all crop categories available in the database with counts.

### 5. Search Crops
```
GET /api/crops/search?name=tomato&category=vegetable&season=kharif
```
Search crops by various criteria including name, category, season, and temperature requirements.

### 6. Enhanced Recommendations
```
GET /api/crops/recommendations/enhanced?temperature=25&rainfall=800&soil_type=loamy&ph_level=6.5
```
Get enhanced crop recommendations based on multiple environmental factors.

## PlantNet API Configuration

The PlantNet API integration uses the following configuration:

```python
api_key = "2b10nNH1NQjSRx5ToTvNSEAV"
base_url = "https://my.plantnet.org/api/v2"
```

### Supported Crops for PlantNet API
The system searches for the following agricultural crops:
- Vegetables: tomato, potato, onion, carrot, cabbage, cauliflower, pepper, cucumber, pumpkin
- Cereals: corn, wheat, rice, barley, oats, sorghum
- Oilseeds: soybean, sunflower, canola, peanut, groundnut
- Pulses: chickpea, lentil
- Fiber: cotton
- Cash crops: sugarcane, mustard, alfalfa

## Data Structure

Each crop from the APIs includes:

```json
{
  "crop_name": "tomato",
  "crop_variety": "Cherry",
  "scientific_name": "Solanum lycopersicum",
  "crop_category": "vegetable",
  "optimal_temperature_min": 18.0,
  "optimal_temperature_max": 30.0,
  "optimal_rainfall_min": 600.0,
  "optimal_rainfall_max": 1200.0,
  "soil_type_preference": ["loamy", "sandy_loam"],
  "ph_range": {"min": 6.0, "max": 7.0},
  "growing_season": "year_round",
  "irrigation_schedule": "drip_irrigation",
  "fertilizer_recommendations": "80:40:40 kg/ha NPK",
  "common_diseases": ["early_blight", "late_blight"],
  "common_pests": ["aphids", "whiteflies"],
  "data_source": "plantnet_api",
  "plantnet_info": {
    "family": "Solanaceae",
    "genus": "Solanum",
    "common_names": ["Tomato", "Love Apple"],
    "plantnet_id": "12345",
    "images_count": 5
  }
}
```

## Usage Examples

### 1. Refresh Crop Database
```bash
curl -X GET "http://localhost:8000/api/crops/refresh"
```

### 2. Get Enhanced Recommendations
```bash
curl -X GET "http://localhost:8000/api/crops/recommendations/enhanced?temperature=25&rainfall=800&soil_type=loamy&ph_level=6.5"
```

### 3. Search for Specific Crops
```bash
curl -X GET "http://localhost:8000/api/crops/search?name=tomato&category=vegetable"
```

## Testing

Run the test script to verify API integration:

```bash
cd backend
python scripts/test_plantnet_api.py
```

This will test both PlantNet and USDA API integrations and show sample results.

## Error Handling

The system includes comprehensive error handling:
- API rate limiting with delays between requests
- Graceful fallback when APIs are unavailable
- Detailed logging of errors and warnings
- Duplicate removal based on crop name and scientific name

## Rate Limiting

- PlantNet API: 0.5 second delay between requests
- USDA API: No specific rate limiting implemented
- All APIs: 10-15 second timeout for requests

## Future Enhancements

1. **Additional APIs**: Integration with more agricultural databases
2. **Image Recognition**: Using PlantNet's image identification features
3. **Real-time Updates**: Scheduled database refreshes
4. **Regional Data**: Location-specific crop recommendations
5. **Market Data**: Integration with crop pricing APIs

## Troubleshooting

### Common Issues

1. **PlantNet API Errors**
   - Check API key validity
   - Verify network connectivity
   - Check rate limiting

2. **USDA API Errors**
   - Verify API endpoint availability
   - Check request parameters

3. **Database Sync Issues**
   - Verify database connection
   - Check CRUD function availability
   - Review error logs

### Debug Mode

Enable debug logging by setting the log level:

```python
import logging
logging.getLogger('app.services.crop_api_service').setLevel(logging.DEBUG)
```

## Security Considerations

- API keys are stored in code (consider environment variables for production)
- Rate limiting implemented to respect API limits
- Error handling prevents sensitive information leakage
- Input validation on all API endpoints

## Performance Considerations

- Asynchronous API calls for better performance
- Caching of API responses (future enhancement)
- Batch processing for database operations
- Efficient duplicate removal algorithms 