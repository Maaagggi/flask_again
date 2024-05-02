from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "S_HiSyP1WL3e7k8GrsSj6dm0UfUXI3pnMHdgMExsiMM"
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True)

from .routes import *
