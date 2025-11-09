import os

CONFIG_FILE = "config.txt"

def load_config():
    """
    Lit le fichier config.txt et renvoie un dictionnaire :
    {
        "machine": "Machine01",
        "host": "127.0.0.1",
        "port": 8888,
        "lang": "fr"
    }
    """
    config = {
        "machine": "UNKNOWN",
        "host": "127.0.0.1",
        "port": 8888,
        "lang": "fr"
    }

    if not os.path.exists(CONFIG_FILE):
        return config

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key == "port":
                    value = int(value)
                config[key] = value
    return config

def save_config(config: dict):
    """
    Sauvegarde le dictionnaire config dans config.txt
    """
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
