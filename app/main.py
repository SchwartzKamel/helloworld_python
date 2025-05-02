"""
main.py
==========================================
Core python file that runs the application
"""

import os
import bleach
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_talisman import Talisman
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address

import app.modules.api as api

# Load environment variables from .env file
load_dotenv()

# --- Configuration & Initialization ---

app = Flask(__name__)

# Security Headers
csp = {
    'default-src': '\'self\'',
    'img-src': '*',
    'script-src': '\'self\'',
    'style-src': '\'self\''
}
talisman = Talisman(app, content_security_policy=csp)

# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # Use memory storage for simplicity, consider Redis for production
)

# --- Secret Validation ---

def validate_secrets():
    """Validates that required environment variables are set."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("Error: API_KEY environment variable not set.")
        # In a real app, you might raise an exception or exit
        # For now, we'll just print an error.
        # raise ValueError("API_KEY environment variable not set.")
        exit(1) # Exit if critical secrets are missing
    print("Secrets validated successfully.")

# --- Routes ---

@app.route("/")
def flask_hello():
    """Basic Hello World endpoint."""
    return {"message": "Hello World"}

@app.route("/random-name")
def random_name_route():
    """Fetches and returns a sanitized random name from an external API."""
    api_key = os.getenv("API_KEY")
    # No need to validate here again if validate_secrets() is called at startup
    # if not api_key:
    #     return jsonify({"error": "API key configuration missing"}), 500

    allowed_domains = ["randommer.io"]
    target_url = "https://randommer.io/api/Name"
    
    if not any(target_url.startswith(f"https://{d}") for d in allowed_domains):
        raise ValueError(f"Access to {target_url} is not permitted")
    
    try:
        raw_name = api.GET_page(target_url, api_key=api_key)
        # Sanitize the input received from the external API
        sanitized_name = bleach.clean(raw_name, strip=True) if raw_name else "Error fetching name"
        return {"name": sanitized_name}
    except Exception as e:
        # Log the error in a real application
        print(f"Error fetching random name: {e}")
        return jsonify({"error": "Failed to fetch random name"}), 500


@app.route("/health", methods=["GET"])
@limiter.limit("5 per minute")  # Apply specific rate limit to this endpoint
def health_check():
    """Health check endpoint with rate limiting."""
    return {"status": "healthy"}

# --- Error Handlers ---

@app.errorhandler(RateLimitExceeded)
def ratelimit_handler(e):
    """Custom handler for rate limit exceeded errors."""
    return jsonify(error=f"Rate limit exceeded: {e.description}"), 429

# --- Main Execution ---

if __name__ == "__main__":
    validate_secrets() # Validate secrets before starting the app
    # Use a production-ready server like Gunicorn/Waitress in production
    # For development:
    app.run(debug=False, host='0.0.0.0', port=5000) # Set debug=False for security
