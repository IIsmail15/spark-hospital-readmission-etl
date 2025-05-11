from dotenv import load_dotenv
import os 

load_dotenv()

DATA_PATH = os.getenv("DATA_PATH", "data/diabetic_data.csv")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "output/")