from flask import Flask, request, session, redirect
from data import Box, ListOfBoxes, available_colours
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

boxes: ListOfBoxes = ListOfBoxes()

users_data = {
    'admin': '1337',
    'user': '666'
}

@app.route("/", methods=['GET'])
def root():
    additional = f"<p><a href='/login'>Войти в аккаунт...</a></p>"
    if 'username' in session:
        additional = f"<p><a href='/logout'>Выйти из аккаунта: {session['username']}</a></p>"

    output = (
        "<p>На этом веб-сайте вы можете создавать коробки!</p>"
        + f"<p>Всего коробок создано: {len(boxes)}.</p>"
        + f"<p><a href='/boxes'>Создать свою коробку!</a></p>"
        + additional
    )

    return output, 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (request.form['username'] in users_data.keys() 
            and request.form['password'] == users_data[request.form['username']]):
            session['username'] = request.form['username']

            return redirect('/')
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''
@app.route('/secret-login/<username>', methods=['POST'])
def secret_login(username):
    if username is None or len(username) == 0:
        return '<p>Ошибка: введите корректное имя пользователя!</p>', 400
    
    if request.method == 'POST':
        session['username'] = username
        return f"<p>Вы зашли как {username}</p>", 200

    return f'<p>{request.method} не поддерживается!</p>', 403

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')

@app.route("/boxes", methods=['GET', 'POST'])
def create_box():
    if request.method == 'POST':
        # parse args
        name = request.args.get('name', None)
        colour = request.args.get('color', None)

        # validate args
        if colour is None or len(colour) == 0:
            return "<p>Ошибка: Вы не указали цвет коробки (нужно указать через параметр <color>)</p>", 400
        
        if name is None or len(name) == 0:
            return "<p>Ошибка: Вы не указали имя коробки (нужно указать через параметр <name>)</p>", 400
        
        if colour not in available_colours:
            return f"<p>Ошибка: Вы указали некорректный цвет коробки.</p>\<p>Доступные цвета: {available_colours}</p>", 400
        
        if 'username' not in session:
            return '<p>Только авторизованные пользователи могут создавать коробки!</p>', 400

        # create box
        new_box = Box(owner=session['username'], name=name, colour=colour)
        try:
            # try to add box to boxes
            boxes.append(new_box)
        except ValueError:
            # raise error if box is not unique
            return f"<p>Ошибка: Такая коробка уже существует!</p>", 400
        except:
            return '<p>Ошибка: Неизвестная ошибка!</p>', 400

        return f"<p>Коробка успешно создана!</p>", 200
        
    elif request.method == 'GET':
        return str(boxes), 200

    return f'<p>{request.method} не поддерживается!</p>', 403

@app.route("/boxes/<box_name>", methods=['GET', 'POST'])
def put_object_in_box(box_name):
    if box_name is None or len(box_name) == 0:
        return '<p>Ошибка: введите корректное название коробки!</p>', 400
    
    if request.method == 'POST':   
        object_name = request.args.get('name', None)
        if object_name is None or len(object_name) == 0:
            return "<p>Ошибка: Вы не указали название предмета (нужно указать через параметр <name>)</p>", 400

        if 'username' not in session:
            return "<p>Ошибка: Вы не авторизованы!</p>", 400

        if session['username'] != boxes.get_box_by_name(box_name=box_name):
            return '<p>Только владелец может изменять содержимое коробки!</p>', 400

        try:
            page = boxes.add_object_to_box(box_name=box_name, object_name=object_name)
        except NameError:
            return '<p>Ошибка: Коробки с таким именем не существует!', 404
        except:
            return '<p>Ошибка: Неизвестная ошибка!</p>', 400
        
        return page, 200

        
    elif request.method == 'GET':
        try:
            page = boxes.render_box(box_name=box_name)
        except NameError:
            return '<p>Ошибка: Коробки с таким именем не существует!', 404
        except:
            return '<p>Ошибка: Неизвестная ошибка!</p>', 400
        
        return page, 200

    return f'<p>{request.method} не поддерживается!</p>', 403
