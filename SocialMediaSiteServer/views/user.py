from flask import Blueprint
from flask import request, jsonify
from util.response_config import *
from util.service_config import UserConfig
from util.service_util import *

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')

    found = UserModel.objects(email=email).first()
    if found:
        return jsonify(Email_already_use)

    user_model = UserModel()
    user_model.name = username
    user_model.email = email
    user_model.password = password
    user_model.save()

    group_model = GroupModel()
    group_model.name = UserConfig.default_group_name
    group_model.owner_user = user_model.id
    group_model.save()

    user_model.group = [group_model.id]
    user_model.save()

    return jsonify(success({"data": {'user': format_user_info(user_model)}}))


@user_blueprint.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    found = UserModel.objects(email=email, password=password).first()
    if not found:
        return jsonify(User_wrong_param)
    return jsonify(success({"data": {"user": format_user_info(found)}}))


@user_blueprint.route('/modify', methods=['POST'])
def modify():
    email = request.form.get('email')
    password_before = request.form.get('passwordBefore')
    password_after = request.form.get('passwordAfter')
    avatar = request.form.get('avatar')

    user = UserModel.objects(email=email, password=password_before).first()
    if not user:
        return jsonify(User_wrong_param)

    user.password = password_after
    user.avatar = avatar
    user.save()

    return jsonify(success({"data": {"user": format_user_info(user)}}))


@user_blueprint.route('/follow', methods=['POST'])
def follow():
    follower_email = request.form.get('followerEmail')
    target_email = request.form.get('targetEmail')
    follower_password = request.form.get('followerPassword')
    group_id = request.form.get('groupId')

    follower = UserModel.objects(email=follower_email, password=follower_password).first()
    if not follower:
        return jsonify(User_wrong_param)
    target = UserModel.objects(email=target_email).first()
    if not target:
        return jsonify(User_not_exist)
    group = GroupModel.objects(id=group_id).first()
    if not group:
        return jsonify(Group_not_exist)

    if target.id not in group.users:
        group.users.append(target.id)
    group.save()

    return jsonify(success())


@user_blueprint.route('/group/create', methods=['POST'])
def group_create():
    email = request.form.get('email')
    password = request.form.get('password')
    group_name = request.form.get('groupName')

    user_model = UserModel.objects(email=email, password=password).first()
    if not user_model:
        return jsonify(User_wrong_param)

    group_model = GroupModel()
    group_model.name = group_name
    group_model.owner_user = user_model.id
    group_model.save()

    if group_model.id not in user_model:
        user_model.group.append(group_model.id)
    user_model.save()

    return jsonify(success({"data": {"group": format_group_info(group_model)}}))


@user_blueprint.route('/group/delete', methods=['POST'])
def group_delete():
    email = request.form.get('email')
    password = request.form.get('password')
    group_id = request.form.get('groupId')

    user_model = UserModel.objects(email=email, password=password).first()
    if not user_model:
        return jsonify(User_wrong_param)
    group = GroupModel.objects(id=group_id).first()
    if not group:
        return jsonify(Group_not_exist)
    default_group = GroupModel.objects(id=user_model.group[0])

    user_list = group.users
    for user_id in user_list:
        if user_id not in default_group.users:
            default_group.users.append(user_id)

    user_model.group.remove(group.id)
    user_model.save()
    default_group.save()
    group.delete()

    return jsonify(success())


@user_blueprint.route('/group/list', methods=['GET'])
def group_list():
    email = request.args.get("email")
    password = request.args.get("password")
    user_model = UserModel.objects(email=email, password=password).first()
    if not user_model:
        return jsonify(User_wrong_param)

    groups = user_model.group
    res = []
    for group_id in groups:
        group = GroupModel.objects(id=group_id).first()
        user_ids = group.users
        g = {"name": group.name, "id": group_id, "users": []}
        users = UserModel.objects(id__in=user_ids)
        for user in users:
            g['users'] = {"email": user.email, "username": user.username, "avatar": user.avatar}
        res.append(g)
    return jsonify(success({"data": {"group_list": res}}))


@user_blueprint.route('/group/followed-user', methods=['GET'])
def group_followed_user():
    email = request.args.get("email")
    password = request.args.get("password")
    group_id = request.form.get('groupId')

    user_model = UserModel.objects(email=email, password=password).first()
    if not user_model:
        return jsonify(User_wrong_param)

    group = GroupModel.objects(id=group_id).first()
    if not group:
        return jsonify(Group_not_exist)

    users = group.users
    res = []
    for user_id in users:
        user = UserModel.objects(id=user_id)
        res.append({"email": user.email, "username": user.username, "avatar": user.avatar})

    return jsonify(success({"data": {"users": res}}))

