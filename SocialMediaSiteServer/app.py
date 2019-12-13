from flask import Flask
from flask_mongoengine import MongoEngine
from app_config import DevelopmentConfig
import logging
import os

db = MongoEngine()

if __name__ == '__main__':
    app = Flask(__name__, static_url_path='/static')  # 要映射静态文件到根目录下用static_url_path=''
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    from views.user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/user')
    from views.file import file_blueprint
    app.register_blueprint(file_blueprint, url_prefix='/api/file')
    from views.album import album_blueprint
    app.register_blueprint(album_blueprint, url_prefix='/api/album')
    from views.media import media_blueprint
    app.register_blueprint(media_blueprint, url_prefix='/api/media')

    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.run()



