def success(x=None):
    d = {'code': 0, 'data': {}}
    if x:
        for t in x:
            if t == 'code' or t == 'msg':
                d[t] = x[t]
            else:
                d['data'][t] = x[t]
    d['data']['msg'] = 'SUCCESS'
    return d


Email_already_use = {'code': 4101, 'data': {'msg': '邮箱已经存在'}}
User_wrong_param = {'code': 4102, 'data': {'msg': '用户名或密码错误'}}
User_not_exist = {'code': 4103, 'data': {'msg': '用户不存在'}}
Group_not_exist = {'code': 4104, 'data': {'msg': '分组不存在'}}
Album_not_exist = {'code': 4105, 'data': {'msg': '专辑不存在'}}
Media_not_exist = {'code': 4106, 'data': {'msg': '媒体不存在'}}

