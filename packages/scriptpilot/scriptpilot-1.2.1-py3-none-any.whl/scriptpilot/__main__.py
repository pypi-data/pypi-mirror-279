from .main import app

def main():
    import uvicorn
    import json
    import os

    CONFIG_FILE = "sp_config.json"

    # Load configuration
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' not found.")

    with open(CONFIG_FILE, "r") as config_file:
        config = json.load(config_file)

    uvicorn.run(app, host="0.0.0.0", port=config["port"])

if __name__ == "__main__":
    main()
