import sqlite3 as sl
from dataclasses import dataclass, field
from ast import literal_eval

available_colours = ('red', 'green', 'blue', 'yellow', 'magenta')

@dataclass
class Box:
    owner: str = field(default=None)

    name: str = field(default=None)
    colour: str = field(default=None)
    objects: dict[str, int] = field(default_factory=dict)

    # post init check for colour to be correct
    def __post_init__(self) -> None:
        if self.colour not in available_colours:
            raise NameError
    
    # render html page with Box objects
    def get_objects_page(self) -> str:
        parts = ''
        for key in self.objects.keys():
            parts += f'<div>Объект: {key}, количество: {self.objects[key]}</div>'

        print(self.owner)

        return (
            f'<html><body style="background-color:{self.colour}">'
            f'<h1>{self.name.capitalize()}</h1>'
            + '<form method="post">'
            + '<p>Object name</p><input type=text name=name>'
            + '<p><input type=submit value="Add item">'
            + '</form>'
            + parts
            + '</body></html>'
        )
        
    # == overloading
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Box):
            return False
        
        return self.name == __value.name or self.colour == __value.colour
        
    def insert_to_db(self) -> None:
        with sl.connect('my-test.db') as con:
            owner_id = con.execute(f'SELECT id FROM USERS WHERE username = "admin"').fetchone()[0]

            con.execute(
                "INSERT INTO BOXES (name, color, objects, boxowner) "
                +f"VALUES ('{self.name}', '{self.colour}', '{str(self.objects)}', {owner_id})"
            )

    def update_in_db(self) -> None:
        with sl.connect('my-test.db') as con:
            con.execute(f'UPDATE BOXES SET objects = "{str(self.objects)}" WHERE name = "{self.name}" AND color = "{self.colour}"')
    #def draw(self) -> str:
        #return f'<div style="width: 100px; height: 100px; border: 1px solid black; color: {self.colour}>'

@dataclass
class ListOfBoxes:
    boxes: list[Box] = field(default_factory=list)

    def load_from_db(self):
        with sl.connect('my-test.db') as con:
            output = con.execute("""
                SELECT * FROM BOXES
                """).fetchall()
            
            users = con.execute("""
                SELECT * FROM USERS
                """).fetchall()
            
            users_info = {}
            for id, username, _ in users:
                users_info.update({id: username})
            
            for id, name, color, objects, boxowner in output:
                self.boxes.append(
                    Box(
                        owner=users_info[boxowner],
                        name=name,
                        colour=color,
                        objects=literal_eval(objects)
                    )
                )

    # kinda overload
    def append(self, box: Box) -> None:
        if box not in self.boxes:
            box.insert_to_db()
            self.boxes.append(box)
        else:
            raise ValueError

    # reset list of boxes
    def reset(self) -> None:
        self.boxes = []

    # add object_name to box with .name == box_name
    def add_object_to_box(self, box_name: str, object_name: str) -> str:
        for i in range(len(self.boxes)):
            if self.boxes[i].name == box_name:
                if object_name in self.boxes[i].objects.keys():
                    self.boxes[i].objects[object_name] += 1
                else:
                    self.boxes[i].objects.update({object_name: 1})

                self.boxes[i].update_in_db()
                return self.boxes[i].get_objects_page()
        
        raise NameError

    def get_box_by_name(self, box_name: str) -> Box:
        for i in range(len(self.boxes)):
            if self.boxes[i].name == box_name:
                return self.boxes[i]

    def render_box(self, box_name: str) -> str:
        for i in range(len(self.boxes)):
            if self.boxes[i].name == box_name:
                return self.boxes[i].get_objects_page()
            
        raise NameError

    # overload of str()
    def __repr__(self) -> str:
        start = (
            '<form method="post">'
            + '<p>Box name</p><input type=text name=name>'
            + '<p>Box color</p><input type=text name=color>'
            + '<p><input type=submit value="Create">'
            + '</form>'
        )

        if len(self.boxes) == 0:
            return start + "коробок еще не создано :("
        
        parts = [start]

        for box in self.boxes:
            parts.append(f'<p style="background: {box.colour}; width: max-content;"><a href="/boxes/{box.name}">Name = {box.name}, color = {box.colour}</a></p>')

        output = ''.join(parts)

        return output
    
    # overload of len()
    def __len__(self) -> int:
        return len(self.boxes)