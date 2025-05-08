"""
    The run.py is used to run the app.routes and render the html templates
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
