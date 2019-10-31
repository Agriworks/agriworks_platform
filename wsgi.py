import app

from flask_cors import CORS

#CORS for the backend server and frontend to communicate with each other
app.config['SECRET_KEY'] = 'secret'
CORS(app)

app = app.create_app()



if __name__ == "main":
    app.run()