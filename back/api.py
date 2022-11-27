from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

from wikiphilo import resolve_page_for_search

app = Flask(__name__)

api = Api(app)

class Crawler(Resource):
    def get(self, name):
        return resolve_page_for_search(name)


api.add_resource(Crawler, "/<string:name>/")
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)