from flask_restplus import Resource


class IndexController(Resource):
     def get(self):
        return {"status": "Congradulations, Agriworks is now running on your machine."}
