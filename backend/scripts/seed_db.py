import json
import sys
import os
import logging

# --- Path Setup ---
# This allows the script to import modules from your 'app' directory
# by adding the project's root directory ('backend/') to the Python path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Imports from your application ---
from app.core.database import SessionLocal, engine
from app.models import crop_data as crop_model # Import the model class
from app.schemas import crop_data as crop_schema # Import the Pydantic schema
from app.crud.crud_crop_data import crop_data # Import the CRUD instance

# --- Logger Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def seed_database():
    """
    Populates the database with initial data from a JSON file.
    This function is idempotent, meaning it's safe to run multiple times.
    """
    db = SessionLocal()
    try:
        # Construct the full path to the data file
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'crops.json')
        
        logger.info(f"Loading data from {data_path}...")
        with open(data_path, 'r') as f:
            crops_data_from_json = json.load(f)

        logger.info("Starting to seed the database with crop data...")

        for crop_item in crops_data_from_json:
            # Check if a crop with the same name already exists
            existing_crop = crop_data.get_crop_by_name(db, name=crop_item["crop_name"])
            
            if existing_crop:
                logger.info(f"Crop '{crop_item['crop_name']}' already exists. Skipping.")
                continue

            # Validate the data from the JSON file using your Pydantic schema
            crop_to_create = crop_schema.CropDataCreate(**crop_item)
            
            # Use your CRUD function to create the new record in the database
            crop_data.create_crop(db, crop_in=crop_to_create)
            logger.info(f"Successfully added crop: {crop_item['crop_name']}")

        logger.info("Database seeding complete.")

    except FileNotFoundError:
        logger.error(f"Error: Data file not found. Please ensure 'data/crops.json' exists.")
    except Exception as e:
        logger.error(f"An error occurred during database seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("--- Database Setup and Seeding Script Initializing ---")
    
    # This command creates all tables defined in your models (via Base.metadata)
    # It is safe to run multiple times; it won't re-create tables that already exist.
    logger.info("Creating database tables if they don't exist...")
    crop_model.Base.metadata.create_all(bind=engine)
    
    # Run the main seeding function
    seed_database()
    
    logger.info("--- Script Finished ---")
