# backend/car_recommender/config.py

import yaml

def load_config(path="backend/config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)
