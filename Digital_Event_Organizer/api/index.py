import sys
import os

# Add the project root to the path so app.py can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as application

# This is the variable Vercel looks for
app = application
