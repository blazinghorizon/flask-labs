from dataclasses import dataclass, field

available_colours = ('red', 'green', 'blue', 'yellow', 'magenta')

@dataclass
class Box:
    name: str = field(default=None)
    colour: str = field(default=None)

    # post init check for colour to be correct
    def __post_init__(self):
        if self.colour not in available_colours:
            raise NameError
        
    # == overloading
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Box):
            return False
        
        return (
            self.name == __value.name
            and
            self.colour == __value.colour
        )
        
    #def draw(self) -> str:
        #return f'<div style="width: 100px; height: 100px; border: 1px solid black; color: {self.colour}>'

@dataclass
class ListOfBoxes:
    boxes: list[Box] = field(default_factory=list)

    # kinda overload
    def append(self, box: Box) -> None:
        if box not in self.boxes:
            self.boxes.append(box)
        else:
            raise ValueError

    # overload of str()
    def __repr__(self) -> str:
        if len(self.boxes) == 0:
            return "коробок еще не создано :("
        
        parts = []

        for box in self.boxes:
            parts.append(f'<p style="background: {box.colour}; width: max-content;">Name = {box.name}, color = {box.colour}</p>')

        output = ''.join(parts)

        return output
    
    # overload of len()
    def __len__(self) -> int:
        return len(self.boxes)