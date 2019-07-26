# AWDFF

AWD-FOR-FUN  
开源AWD平台

beta 0.1 版本功能说明

- [ ]  个人用户注册、登录
- [ ] 队伍注册
- [ ] 个人用户带token加入团队
- [ ] 裁判手动开启比赛
    - [ ] 题目容器开始运行，保存ssh、web端口，ssh 账号密码
    - [ ] 自动分发本队ssh端口,账户密码
    - [ ] 自动分发本队web端口
    - [ ] 平台发放所有赛题端口(略过需要扫描内网环境这一步)
- [ ] 比赛过程中
    - [ ] 提交flag，获取分数，平台可显示攻陷情况
    - [ ] 可发布提示公告
    - [ ] 可重置赛题容器 
- [ ] 裁判手动结束比赛


# 第一次开始

执行

```bash

python manage.py makemigrations
python manage.py collectstatic
python manage.py migrate

```

创建一个管理员账户
```bash
python manage.py createsuperuser
```