
"""
HBnB Application Launcher

This module serves as the entry point for the HBnB application.
It creates the Flask application instance using the application
factory and starts the development server.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)