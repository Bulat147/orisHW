#!/usr/bin/env python3

import cgi

from util import Util

form = cgi.FieldStorage()
action = form.getfirst("action")

poster = form.getfirst("poster")

login = form.getfirst("login")
password = form.getfirst("password")


util = Util()

online = util.get_data(util.ONLINE)
user = online[0] if len(online) else None

error = False
message = ''

if action == "login":
    if util.login(login, password):
        user = login
    else:
        error = True
        message = '<p>Такой пользователь не зарегистрирован</p>'
elif action == "register":
    util.register(login, password)
    message = '<p>Вы зарегистрированы и уже авторизованы</p>'
elif action == "logout":
    util.logout(user)
    message = "<p>Вы вышли из системы</p>"
elif not action:
    if not util.is_online(user):
        action = "logout"

if action == "logout" or error:
    form = '''
        <h1>Авторизуйтесь</h1>
        <form method="post" action="wall.py">
            Логин: <input type="text" name="login">
            Пароль: <input type="password" name="password">
            <input type="hidden" name="action" value="login">
            <input type="submit">
        </form>
        <h1>Еще не зарегистрированы?</h1>
        <form method="post" action="wall.py">
            Логин: <input type="text" name="login">
            Пароль: <input type="password" name="password">
            <input type="hidden" name="action" value="register">
            <input type="submit">
        </form>
    '''
else:
    form = '''
        <form action="wall.py">
            <input type="hidden" name="action" value="logout">
            <input type="submit" value="Выйти">
        </form>
        <br>
        <br>
        Напишите новый пост:
        <br>
        <br>
        <form action="wall.py">
        <textarea name="poster"></textarea>
        <p><input type="submit" value="Отправить"></p>
        </form>
        
    '''

if poster != None:
    util.set_post(poster, user)

user_posts = util.get_user_posts(user)
if user_posts is not None and action != "logout":
    for post in user_posts:
        form += f"<div style=\"border:2px solid #000;width:30%;text-align:center;\">{post}</div><br>"

pattern = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Wall</title>
</head>
<body>
    {form}

    {message}
</body>
</html>
'''

print('Content-type: text/html\n')
print(pattern.format(form=form, message=message))
