from flask import Blueprint
from flask import request, jsonify
from models.post import MediaModel, AlbumModel
from models.user import UserModel
from util.service_config import get_boolean
from util.response_config import *

album_blueprint = Blueprint('album', __name__)


# TODO 判断是否点赞过

@album_blueprint.route("/test", methods=["GET"])
def test():
    album_list = AlbumModel.objects().order_by('-liked', '-create_time')
    return jsonify(album_list)


@album_blueprint.route("/create", methods=['POST'])
def create():
    email = request.form.get('email')
    password = request.form.get('password')
    name, tags, cover, description, public = get_album_param()

    found = UserModel.objects(email=email, password=password).first()
    if found:
        return jsonify(User_not_exist)

    album = AlbumModel()
    set_album(album, name, tags, cover, description, public, found.id)

    album.save()

    return jsonify(success({"data": {"album": album}}))


@album_blueprint.route("/modify", methods=['POST'])
def modify():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("id")
    name, tags, cover, description, public = get_album_param()

    found = UserModel.objects(email=email, password=password).first()
    if found:
        return jsonify(User_not_exist)

    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)

    set_album(album, name, tags, cover, description, public, found.id)
    album.save()

    return jsonify(success({"data": {"album": album}}))


@album_blueprint.route("/delete", methods=['POST'])
def delete_album():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("id")

    found = UserModel.objects(email=email, password=password).first()
    if found:
        return jsonify(User_not_exist)

    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)

    album.delete()
    return jsonify(success())


@album_blueprint.route("/list-self", methods=['GET'])
def list_self():
    email = request.args.get('email')
    password = request.args.get('password')

    found = UserModel.objects(email=email, password=password).first()
    if found:
        return jsonify(User_not_exist)

    album_list = AlbumModel.objects(user=found.id)
    if not album_list or len(album_list) == 0:
        return jsonify(Album_not_exist)
    return jsonify(success({"data": {"album_list": album_list}}))


@album_blueprint.route("/list-hot", methods=['GET'])
def list_hot():
    email = request.args.get('email')
    password = request.args.get('password')
    only_friends = get_boolean(request.args.get('onlyFriends'))

    user = UserModel.objects(email=email, password=password).first()
    if user:
        return jsonify(User_not_exist)

    album_list = AlbumModel.objects().order_by('-liked', '-create_time')
    res = []
    if only_friends:
        friends = user.group
        for a in album_list:
            if a.user in friends:
                res.append(a)
    else:
        res = album_list

    return jsonify(success({"data": {"album_list": res}}))


@album_blueprint.route("/list-collection", methods=['GET'])
def list_collection():
    email = request.args.get('email')
    password = request.args.get('password')

    user = UserModel.objects(email=email, password=password).first()
    if user:
        return jsonify(User_not_exist)

    album_list = user.collection_album
    res = []
    for album_id in album_list:
        album = AlbumModel.objects(id=album_id).first()
        if album:
            res.append(album)
    return jsonify(success({"data": {"album_list": res}}))


@album_blueprint.route("/info", methods=['GET'])
def info():
    # TODO 记录下访问信息
    album_id = request.args.get("id")
    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)
    return jsonify(success({"data": {"album": album}}))


@album_blueprint.route("/collect", methods=['POST'])
def collect():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("id")

    user = UserModel.objects(email=email, password=password).first()
    if user:
        return jsonify(User_not_exist)

    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)
    if album.id not in user.collection_album:
        user.collection_album.append(album.id)
    user.save()
    return jsonify(success())


@album_blueprint.route("/dis-collect", methods=['POST'])
def dis_collect():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("id")

    user = UserModel.objects(email=email, password=password).first()
    if user:
        return jsonify(User_not_exist)
    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)

    if album.id in user.collection_album:
        user.collection_album.remove(album.id)
    user.save()
    return jsonify(success())


@album_blueprint.route("/like", methods=['POST'])
def like():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("id")

    user = UserModel.objects(email=email, password=password).first()
    if user:
        return jsonify(User_not_exist)
    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)

    if album.id not in user.like_album:
        user.like_album.append(album.id)
    user.save()
    return jsonify(success())


@album_blueprint.route("/dis-like", methods=['POST'])
def dis_like():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("id")

    user = UserModel.objects(email=email, password=password).first()
    if user:
        return jsonify(User_not_exist)
    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)

    if album.id in user.like_album:
        user.like_album.remove(album.id)
    user.save()
    return jsonify(success())


@album_blueprint.route("/search", methods=['GET'])
def search():
    email = request.args.get('email')
    password = request.args.get('password')
    keywords = request.args.get('keywords')
    keyword_list = keywords.strip().split(" ")

    user = UserModel.objects(email=email, password=password).first()
    if user:
        return jsonify(User_not_exist)
    res_set = set()
    for k in keyword_list:
        res_set.update(AlbumModel.objects.filter(description__contains=k))
        res_set.update(AlbumModel.objects.filter(name__contains=k))
        res_set.update(AlbumModel.objects.filter(tags__contains=k))
    res_list = sorted(list(res_set), key=lambda album: album.create_time, reverse=True)
    return jsonify(success({"data": {"album_list": res_list}}))


@album_blueprint.route("/repeat", methods=['POST'])
def repeat():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("id")

    user = UserModel.objects(email=email, password=password).first()
    if user:
        return jsonify(User_not_exist)
    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)

    repeat_album = AlbumModel()
    copy_album(album, repeat_album)

    return 0


@album_blueprint.route("/comment", methods=['POST'])
def comment():
    return 0


@album_blueprint.route("/history", methods=['POST'])
def history():
    return 0


def get_album_param():
    name = request.form.get('name')
    tags = request.form.getlist('tags')
    cover = request.form.get('cover')
    description = request.form.get('description')
    public = get_boolean(request.form.get('public'))
    return name, tags, cover, description, public


def copy_album(origin, target):
    pass


def add_like_info(album, user):
    return {}


def set_album(album, name, tags, cover, description, public, user_id):
    album.name = name
    album.tags = tags
    album.cover = cover
    album.description = description
    album.public = public
    album.user = user_id
