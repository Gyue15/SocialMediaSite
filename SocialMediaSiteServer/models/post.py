import datetime
from app import db


class AlbumModel(db.DynamicDocument):
    name = db.StringField(max_length=128)
    tags = db.ListField(db.StringField(max_length=128))
    description = db.StringField(max_length=256)
    public = db.BooleanField(default=False)
    cover = db.StringField(max_length=128)
    like_num = db.IntField(min_value=0, default=0)
    create_time = db.DateTimeField(default=lambda: datetime.datetime.utcnow())
    modify_time = db.DateTimeField(default=lambda: datetime.datetime.utcnow())
    media_list = db.ListField(db.ObjectIdField(), default=[])
    comments = db.ListField(db.DictField(default={}), default=[])
    user = db.ObjectIdField()
    like_user = db.ListField(db.DictField(default={}), default=[])


class MediaModel(db.DynamicDocument):
    name = db.StringField(max_length=128)
    url = db.StringField(max_length=256)
    description = db.StringField(max_length=256)
    like_num = db.IntField(min_value=0, default=0)
    create_time = db.DateTimeField(default=lambda: datetime.datetime.utcnow())
    modify_time = db.DateTimeField(default=lambda: datetime.datetime.utcnow())
    public = db.BooleanField(default=False)
    tags = db.ListField(db.StringField(max_length=128))
    media_type = db.StringField(max_length=128)
    comments = db.ListField(db.DictField(default={}), default=[])
    album = db.ObjectIdField()
    user = db.ObjectIdField()
    like_user = db.ListField(db.DictField(default={}))




