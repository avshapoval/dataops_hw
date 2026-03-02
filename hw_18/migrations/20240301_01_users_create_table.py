"""
users: create table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        DROP TABLE users
        """
    )
]
