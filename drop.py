import os
from app import db,create_app
app=create_app('developmentcode ')
db.init_app(app)
with app.app_context():
    db.drop_all()