from aram import app
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_URI = os.environ.get("POSTGRES_DB_URI")


if __name__ == "__main__":
    app.run(debug=True)
