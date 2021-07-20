"""Seed for Blogly"""

from models import User, db
from app import app

# Create tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
alan_alda = User(first_name="Alan", last_name="Alda")
joel_burton = User(first_name="Joel", last_name="Burton")
jane_smith = User(first_name="Jane", last_name="Smith")

# Add objects to the session
db.session.add(alan_alda)
db.session.add(joel_burton)
db.session.add(jane_smith)

# Commit!
db.session.commit()