from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
