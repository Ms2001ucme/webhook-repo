from flask import Blueprint

# Import routes so they get registered
from app.webhook.routes import webhook

# Re-export the blueprint for app factory
webhook_bp = webhook

