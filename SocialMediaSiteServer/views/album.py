from flask import Blueprint
from flask import request, jsonify
from util.service_config import get_boolean
from util.response_config import *
from util.service_util import *

album_blueprint = Blueprint('album', __name__)


@album_blueprint.route("/test", methods=["GET"])
def test():
    user_list = UserModel.objects(email__contains="1576294283.7824", avatar=None)
    return jsonify(success({"data": {"user_list": list(map(lambda x: format_user_info(x), user_list))}}))


@album_blueprint.route("/create", methods=['POST'])
def create():
    email = request.form.get('email')
    password = request.form.get('password')
    name, tags, cover, description, public = get_album_param()

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    album = AlbumModel()
    set_album(album, name, tags, cover, description, public, user.id)
    album.save()

    return jsonify(success({"data": {"album": format_album_info(album, user)}}))


@album_blueprint.route("/modify", methods=['POST'])
def modify():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("id")
    name, tags, cover, description, public = get_album_param()

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)

    set_album(album, name, tags, cover, description, public, user.id)
    album.save()

    return jsonify(success({"data": {"album": format_album_info(album, user)}}))


@album_blueprint.route("/delete", methods=['POST'])
def delete_album():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("id")

    found = UserModel.objects(email=email, password=password).first()
    if not found:
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

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    album_list = AlbumModel.objects(user=user.id)
    if not album_list or len(album_list) == 0:
        return jsonify(Album_not_exist)
    album_list = list(map(lambda x: format_album_info(x, user), album_list))
    return jsonify(success({"data": {"album_list": album_list}}))


@album_blueprint.route("/list-hot", methods=['GET'])
def list_hot():
    email = request.args.get('email')
    password = request.args.get('password')
    only_friends = get_boolean(request.args.get('onlyFriends'))

    user = UserModel.objects(email=email, password=password).first()
    if not user:
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
    res = list(map(lambda x: format_album_info(x, user), res))
    return jsonify(success({"data": {"album_list": res}}))


@album_blueprint.route("/list-collection", methods=['GET'])
def list_collection():
    email = request.args.get('email')
    password = request.args.get('password')

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    album_id_list = user.collection_album
    album_list = AlbumModel.objects(id__in=album_id_list)
    res = list(map(lambda a: format_album_info(a, user), album_list))
    return jsonify(success({"data": {"album_list": res}}))


@album_blueprint.route("/info", methods=['GET'])
def info():
    album_id = request.args.get("id")
    email = request.args.get('email')
    password = request.args.get('password')
    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)
    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)
    user.viewed_album.insert(0, album.id)
    user.save()
    return jsonify(success({"data": {"album": format_album_info(album, user)}}))


@album_blueprint.route("/collect", methods=['POST'])
def collect():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("albumId")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
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
    album_id = request.form.get("albumId")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
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
    album_id = request.form.get("albumId")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
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
    album_id = request.form.get("albumId")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
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
    if not user:
        return jsonify(User_not_exist)
    res_set = set()
    for k in keyword_list:
        res_set.update(AlbumModel.objects(description__contains=k))
        res_set.update(AlbumModel.objects(name__contains=k))
        res_set.update(AlbumModel.objects(tags__contains=k))
    res_list = list(map(lambda album: format_album_info(album, user),
                        sorted(list(res_set), key=lambda album: album.create_time, reverse=True)))
    return jsonify(success({"data": {"album_list": res_list}}))


@album_blueprint.route("/comment", methods=['POST'])
def comment():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("albumId")
    comment_str = request.form.get("comment")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)
    album = AlbumModel.objects(id=album_id).first()
    if not album:
        return jsonify(Album_not_exist)

    album.comments.append({
        "user": {"username": user.username, "avatar": user.avatar, "email": user.email},
        "comment": comment_str,
        "time": datetime.datetime.utcnow()
    })
    album.save()
    return jsonify(success({"data": {"album": format_album_info(album, user)}}))


@album_blueprint.route("/history", methods=['GET'])
def history():
    email = request.args.get('email')
    password = request.args.get('password')

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    return jsonify(success({"data": {"album_list": list(map(lambda x: format_album_info(x, user),
                                                            AlbumModel.objects(id__in=user.viewed_album)))}}))


def get_album_param():
    name = request.form.get('name')
    tags = request.form.getlist('tags')
    cover = request.form.get('cover')
    description = request.form.get('description')
    public = get_boolean(request.form.get('public'))
    return name, tags, cover, description, public
