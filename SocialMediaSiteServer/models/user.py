from app import db


class UserModel(db.DynamicDocument):
    email = db.EmailField(max_length=128, unique=True)
    password = db.StringField(max_length=128)
    username = db.StringField(max_length=128)
    avatar = db.StringField(max_length=128)
    follower = db.ListField(db.ObjectIdField())
    group = db.ListField(db.ObjectIdField())
    collection_album = db.ListField(db.ObjectIdField(), default=[])
    collection_media = db.ListField(db.ObjectIdField(), default=[])
    like_album = db.ListField(db.ObjectIdField(), default=[])
    like_media = db.ListField(db.ObjectIdField(), default=[])


class GroupModel(db.DynamicDocument):
    name = db.StringField(max_length=128)
    owner_user = db.ObjectIdField()
    users = db.ListField(db.ObjectIdField(), default=[])
