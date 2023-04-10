from flask import Flask, request
from data import Box, ListOfBoxes, available_colours
app = Flask(__name__)

boxes = ListOfBoxes()

@app.route("/", methods=['GET'])
def root():
    output = (
        "<p>На этом веб-сайте вы можете создавать коробки!</p>"
        + f"<p>Всего коробок создано: {len(boxes)}.</p>"
        + f"<p><a href='/boxes'>Создать свою коробку!</a></p>"
    )

    return output, 200

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
        
        # create box
        new_box = Box(name=name, colour=colour)
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