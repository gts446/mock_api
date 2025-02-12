from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
from api import APIRequest, APIHandler, APIResponse
import db_config

db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_config.username}:{db_config.password}@localhost/{db_config.database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"echo": True}

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/fake', methods=['POST'])
def fk():
    from fake_data import generate_sample_data
    generate_sample_data(db)
    return ''


@app.route('/', methods=['POST'])
def hello_world():
    api_request, error_msg = APIRequest.form_request(request)
    pprint(request.form)
    if error_msg:
        pprint(error_msg)
        return error_msg, 400
    
    api_handler = APIHandler(api_request)

    success, data, msg = api_handler.result(db)

    if not success:
        pprint(f"{api_request.function} - {api_request.data} - {msg}")
        return msg, 400
    

    response = APIResponse(success, data,msg)

    # pprint(data)
    return response.to_json()

if __name__ == '__main__':
    app.run(port = 8000, debug=True)