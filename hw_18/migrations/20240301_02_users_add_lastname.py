"""
users: add lastname column
"""

from yoyo import step

__depends__ = {'20240301_01_users_create_table'}

steps = [
    step(
        """
        ALTER TABLE users ADD COLUMN lastname VARCHAR(100)
        """,
        """
        ALTER TABLE users DROP COLUMN lastname
        """
    )
]
