import sys
import os

# Add the project subfolder to the path so app.py can be imported
# This assumes api/index.py is at the root and app.py is in Digital_Event_Organizer/
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Digital_Event_Organizer"))

from app import app as application

# This is the variable Vercel looks for
app = application
