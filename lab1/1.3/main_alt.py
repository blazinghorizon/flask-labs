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

    return output

@app.route("/boxes", methods=['GET', 'POST'])
def create_box():
    if request.method == 'POST':
        # parse args
        name = request.args.get('name', None)
        colour = request.args.get('color', None)

        # validate args
        if colour is None or len(colour) == 0:
            return "<p>Ошибка: Вы не указали цвет коробки (нужно указать через параметр <color>)</p>"
        
        if name is None or len(name) == 0:
            return "<p>Ошибка: Вы не указали имя коробки (нужно указать через параметр <name>)</p>"
        
        if colour not in available_colours:
            return f"<p>Ошибка: Вы указали некорректный цвет коробки.</p>\<p>Доступные цвета: {available_colours}</p>"
        
        # create box
        new_box = Box(name=name, colour=colour)
        try:
            # try to add box to boxes
            boxes.append(new_box)
        except ValueError:
            # raise error if box is not unique
            return f"<p>Ошибка: Такая коробка уже существует!</p>"
        except:
            return '<p>Ошибка: Неизвестная ошибка!</p>'

        return f"<p>Коробка успешно создана!</p>"
        
    elif request.method == 'GET':
        return str(boxes)

    return f'<p>{request.method} не поддерживается!</p>'

@app.route("/boxes/<box_name>", methods=['GET', 'POST'])
def put_object_in_box(box_name):
    if request.method == 'POST':
        ...
    elif request.method == 'GET':
        ...

    return f'<p>{request.method} не поддерживается!</p>'