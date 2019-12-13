import os
from flask import Blueprint
from flask import request, jsonify
from werkzeug.utils import secure_filename
from util.service_config import FileConfig
import time
from util.response_config import *

file_blueprint = Blueprint('file', __name__)


@file_blueprint.route('upload', methods=['POST'])
def upload():
    file = request.files['file']
    t = time.time()
    filename = str(round(t * 1000)) + secure_filename(file.filename)
    path = os.path.join(FileConfig.UPLOAD_FOLDER, filename)
    url = os.path.join(FileConfig.FILE_URL, filename)
    file.save(path)
    return jsonify(success({"data": {"file_url": url}}))
