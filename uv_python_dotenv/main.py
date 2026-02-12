import os
from dotenv import load_dotenv

load_dotenv()

test_key = os.getenv("test_key")
print (f"test_key={test_key}")
