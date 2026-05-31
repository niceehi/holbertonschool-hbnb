
"""
Base model for all HBnB entities.
"""

from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    Base class inherited by all models.
    """

    def __init__(self):
        self.id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """
        Update modification timestamp.
        """
        self.updated_at = datetime.utcnow()