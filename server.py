from flask_app import app
from flask_app.controllers import users
# imports the users file content from the controllers folder

if __name__ == "__main__":
    app.run(debug=True)