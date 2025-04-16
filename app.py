from flask import Flask, render_template
from models import db
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
from routes import register_routes

load_dotenv()


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    

register_routes(app)

@app.route('/')
def home():
    return render_template('app.html')

if __name__ == '__main__':
    app.run(debug=True)
