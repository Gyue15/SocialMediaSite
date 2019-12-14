from flask import Blueprint
from flask import request, jsonify
from util.service_config import get_boolean
from util.response_config import *
from util.service_util import *

media_blueprint = Blueprint('media', __name__)


@media_blueprint.route("/upload", methods=["POST"])
def upload():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("albumId")
    name, tags, media_type, description, public, url = get_media_param()

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    media = MediaModel()
    set_media(media, name, tags, media_type, description, public, url, user.id)
    media.save()

    album = AlbumModel.objects(id=album_id).first() if album_id else None
    if album:
        media.album = album.id
        if media.id not in album.media_list:
            album.media_list.append(media.id)
    album.save()
    media.save()

    return jsonify(success({"data": {"media": format_media_info(media, user)}}))


@media_blueprint.route("/delete", methods=["POST"])
def delete():
    email = request.form.get('email')
    password = request.form.get('password')
    media_id = request.form.get("mediaId")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)
    media = MediaModel.objects(id=media_id).first()
    if not media:
        return jsonify(Media_not_exist)

    media.delete()
    return jsonify(success())


@media_blueprint.route("/list-self", methods=["GET"])
def list_self():
    email = request.args.get('email')
    password = request.args.get('password')
    album_id = request.args.get("albumId")
    media_type = request.args.get("type")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    if album_id:
        media_list = MediaModel.objects(album=album_id, user=user.id) if media_type == "BOOTH" else MediaModel.objects(
            album=album_id, media_type=media_type, user=user.id)
    else:
        media_list = MediaModel.objects(user=user.id) if media_type == "BOOTH" else MediaModel.objects(
            media_type=media_type, user=user.id)
    return jsonify(success({"data": {"media_list": list(map(lambda x: format_media_info(x, user), media_list))}}))


@media_blueprint.route("/list-hot", methods=["GET"])
def list_hot():
    email = request.args.get('email')
    password = request.args.get('password')
    media_type = request.args.get("type")
    only_friends = get_boolean(request.args.get("onlyFriends"))

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    media_list = MediaModel.objects().order_by('-liked', '-create_time') if media_type == "BOOTH" else \
        MediaModel.objects(media_type=media_type).order_by('-liked', '-create_time')
    res = []
    if only_friends:
        friends = user.group
        for media in media_list:
            if media.user in friends:
                res.append(media)
    else:
        res = media_list
    return jsonify(success({"data": {"media_list": list(map(lambda x: format_media_info(x, user), res))}}))


@media_blueprint.route("/list-collection", methods=["GET"])
def list_collection():
    email = request.args.get('email')
    password = request.args.get('password')
    media_type = request.args.get("type")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    media_id_list = user.collection_media
    media_list = MediaModel.objects(id__in=media_id_list) if media_type == "BOOTH" else MediaModel.objects(
        id__in=media_id_list, media_type=media_type)
    res = list(map(lambda a: format_media_info(a, user), media_list))
    return jsonify(success({"data": {"media_list": res}}))


@media_blueprint.route("/info", methods=["GET"])
def info():
    email = request.args.get('email')
    password = request.args.get('password')
    media_id = request.args.get("mediaId")
    media = MediaModel.objects(id=media_id).first()
    if not media:
        return jsonify(Media_not_exist)
    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)
    user.viewed_media.insert(0, media.id)
    user.save()
    return jsonify(success({"data": {"media": format_media_info(media, user)}}))


@media_blueprint.route("/modify", methods=["POST"])
def modify():
    email = request.form.get('email')
    password = request.form.get('password')
    album_id = request.form.get("albumId")
    media_id = request.form.get("mediaId")
    name, tags, media_type, description, public, url = get_media_param()

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)
    media = MediaModel.objects(id=media_id).first()
    if not media:
        return jsonify(Media_not_exist)
    set_media(media, name, tags, media_type, description, public, url, user.id)

    album = AlbumModel.objects(id=album_id).first()
    if album:
        media.album = album.id
        if media.id not in album.media_list:
            album.media_list.append(media.id)
    album.save()
    media.save()

    return jsonify(success({"data": {"media": format_media_info(media, user)}}))


@media_blueprint.route("/collect", methods=["POST"])
def collect():
    email = request.form.get('email')
    password = request.form.get('password')
    media_id = request.form.get("mediaId")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    media = MediaModel.objects(id=media_id).first()
    if not media:
        return jsonify(Media_not_exist)
    if media.id not in user.collection_media:
        user.collection_media.append(media.id)
    user.save()
    return jsonify(success())


@media_blueprint.route("/dis-collect", methods=["POST"])
def dis_collect():
    email = request.form.get('email')
    password = request.form.get('password')
    media_id = request.form.get("mediaId")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    media = MediaModel.objects(id=media_id).first()
    if not media:
        return jsonify(Media_not_exist)
    if media.id in user.collection_media:
        user.collection_media.remove(media.id)
    user.save()
    return jsonify(success())


@media_blueprint.route("/like", methods=["POST"])
def like():
    email = request.form.get('email')
    password = request.form.get('password')
    media_id = request.form.get("mediaId")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    media = MediaModel.objects(id=media_id).first()
    if not media:
        return jsonify(Media_not_exist)
    if media.id not in user.like_media:
        user.like_media.append(media.id)
    user.save()
    return jsonify(success())


@media_blueprint.route("/dis-like", methods=["POST"])
def dis_like():
    email = request.form.get('email')
    password = request.form.get('password')
    media_id = request.form.get("mediaId")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    media = MediaModel.objects(id=media_id).first()
    if not media:
        return jsonify(Media_not_exist)
    if media.id in user.like_media:
        user.like_media.remove(media.id)
    user.save()
    return jsonify(success())


@media_blueprint.route("/search", methods=["GET"])
def search():
    email = request.args.get('email')
    password = request.args.get('password')
    keywords = request.args.get('keywords')
    media_type = request.args.get("type")
    keyword_list = keywords.strip().split(" ")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)
    res_set = set()
    if media_type == "BOOTH":
        for k in keyword_list:
            res_set.update(MediaModel.objects(description__contains=k))
            res_set.update(MediaModel.objects(name__contains=k))
            res_set.update(MediaModel.objects(tags__contains=k))
    else:
        for k in keyword_list:
            res_set.update(MediaModel.objects(media_type=media_type, description__contains=k))
            res_set.update(MediaModel.objects(media_type=media_type, name__contains=k))
            res_set.update(MediaModel.objects(media_type=media_type, tags__contains=k))
    res_list = list(map(lambda x: format_media_info(x, user),
                        sorted(list(res_set), key=lambda x: x.create_time, reverse=True)))
    return jsonify(success({"data": {"media_list": res_list}}))


@media_blueprint.route("/comment", methods=["POST"])
def comment():
    email = request.form.get('email')
    password = request.form.get('password')
    media_id = request.form.get("mediaId")
    comment_str = request.form.get("comment")

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)
    media = MediaModel.objects(id=media_id).first()
    if not media:
        return jsonify(Media_not_exist)

    media.comments.append({
        "user": {"username": user.username, "avatar": user.avatar, "email": user.email},
        "comment": comment_str,
        "time": datetime.datetime.utcnow()
    })
    media.save()
    return jsonify(success({"data": {"media": format_media_info(media, user)}}))


@media_blueprint.route("/history", methods=["GET"])
def history():
    email = request.args.get('email')
    password = request.args.get('password')

    user = UserModel.objects(email=email, password=password).first()
    if not user:
        return jsonify(User_not_exist)

    return jsonify(success({"data": {"media_list": list(map(lambda x: format_media_info(x, user),
                                                            MediaModel.objects(id__in=user.viewed_media)))}}))


def get_media_param():
    name = request.form.get('name')
    tags = request.form.getlist('tags')
    media_type = request.form.get('type')
    description = request.form.get('description')
    public = get_boolean(request.form.get('public'))
    url = request.form.get('url')
    return name, tags, media_type, description, public, url
