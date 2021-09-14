from app import app
import os
from dotenv import load_dotenv

load_dotenv('.env')

app.run(host=os.environ.get("HOST"), port=os.environ.get("PORT"), debug=os.environ.get("DEBUG"), use_reloader=False)
