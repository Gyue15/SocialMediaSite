class DevelopmentConfig:
    WTF_CSRF_ENABLED = False  # 是否开启flask-wtf的csrf保护,默认是True,用postman提交表单测试需要设为False
    MONGODB_SETTINGS = {
        'db': 'social_media',
        'host': '127.0.0.1',
        'port': 27017,
        'connect': False  # False: connect when first connect instead of instantiated
    }
