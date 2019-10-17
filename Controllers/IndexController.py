from flask_restplus import Resource


class IndexController(Resource):
     def get(self):
        return {"status": "Successful"}
    