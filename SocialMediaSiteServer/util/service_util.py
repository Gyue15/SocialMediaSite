from models.user import *
from models.post import *


def format_album_info(album, user):
    return {
        "id": album.id.__str__(),
        "name": album.name,
        "tags": album.tags,
        "public": album.public,
        "cover": album.cover,
        "like_num": album.like_num,
        "liked": user.id in album.like_user,
        "description": album.description,
        "create_time": album.create_time,
        "modify_time": album.modify_time,
        "media_list": list(map(lambda x: format_media_info(x, user), MediaModel.objects(id__in=album.media_list))),
        "comments": album.comments,
    }


def format_media_info(media, user):
    return {
        "name": media.name,
        "id": media.id.__str__(),
        "url": media.url,
        "like_num": media.like_num,
        "liked": user.id in media.like_user,
        "description": media.description,
        "create_time": media.create_time,
        "modify_time": media.modify_time,
        "public": media.public,
        "type": media.media_type,
        "comments": media.comments,
    }


def format_user_info(user):
    return {
        "email": user.email,
        "username": user.username,
        "password": user.password,
        "avatar": user.avatar
    }


def set_album(album, name, tags, cover, description, public, user_id):
    album.name = name
    album.tags = tags
    album.cover = cover
    album.description = description
    album.public = public
    album.user = user_id


def set_media(media, name, tags, media_type, description, public, url, user_id):
    media.name = name
    media.tags = tags
    media.media_type = media_type
    media.description = description
    media.public = public
    media.user = user_id
    media.url = url


def format_group_info(group):
    return {
        "name": group.name,
        "id": group.id.__str__(),
        "users": list(map(lambda x: format_user_info(x), UserModel.objects(id__in=group.users)))
    }
