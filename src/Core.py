from Events import Event


class DirectionError(Exception):
    """
    This exception is raised when a wrong direction is given to the compass.
    """


class Interactive:
    def __init__(self, name, description="", activate=None, look=None, hidden=False):
        if description == "":
            description = "Nothing out of the ordinary."
        self.name = name
        self.description = Event(event=description)
        self.hidden = hidden
        self.events = {
            "lookAt": Event(event=look),
            "activate": Event(event=activate)
        }

    def set(self, name, value):
        self.events[name] = Event(event=value)


class Room:
    class Compass:
        def __init__(self):
            directions = (
                "north",
                "south",
                "east",
                "west",
                "up",
                "down",
                "in",
                "out"
            )
            self.data = {}
            for direction in directions:
                self.data[direction] = None

        def __len__(self):
            return len(self.get_all(prompt=True))

        def set(self, direction, destination, event=None, hidden=False):
            direction = direction.lower().strip()
            for item in self.data:
                if item == direction:
                    self.data[item] = Event(destination, event, hidden=hidden)
                    return
            raise DirectionError("Undefined direction: " + direction)

        def get(self, direction):
            if len(direction) == 1:
                for item in self.data:
                    if item.startswith(direction):
                        return self.data[item]
            else:
                for item in self.data:
                    if item == direction:
                        return self.data[direction]
            return False

        def get_all(self, prompt=False):
            result = []
            for (name, value) in self.data.items():
                if value is not None and (not prompt or not value.config["hidden"]):
                    result.append(name)
            return result

        def remove(self, direction):
            self.set(direction, None)

    class Map:
        def __init__(self):
            self.data = {}

        def __len__(self):
            return len(self.get_all(prompt=True))

        def set(self, location, destination, event=None, hidden=False):
            if destination is None:
                del self.data[location]
            else:
                self.data[location] = Event(destination, event, hidden=hidden)

        def get(self, location):
            if location in self.data:
                return self.data[location]

        def get_all(self, prompt=False):
            result = []
            for (name, value) in self.data.items():
                if not prompt or not value.config["hidden"]:
                    result.append(name)
            return result

        def remove(self, direction):
            self.set(direction, None)

    class Interactives:
        def __init__(self):
            self.data = []

        def __len__(self):
            return len(self.get_all(prompt=True))

        def add(self, interactive):
            added = False
            for i in range(len(self.data)):
                if self.data[i].name == interactive.name:
                    self.data[i] = interactive
                    added = True
            if not added:
                self.data.append(interactive)

        def get(self, name):
            for interactive in self.data:
                if interactive.name == name:
                    return interactive

        def get_all(self, prompt=False):
            result = []
            for interactive in self.data:
                if not prompt or not interactive.hidden:
                    result.append(interactive.name)
            return result

        def remove(self, name):
            for i in range(len(self.data)):
                if self.data[i].name == name:
                    del self.data[i]

    class Items:
        def __init__(self):
            self.data = []

        def __len__(self):
            return len(self.get_all())

        def add(self, item):
            if not isinstance(item, Event):
                self.data.append(Event(item))
            else:
                self.data.append(item)

        def get_all(self):
            result = []
            for item in self.data:
                result.append(item.next.name)
            return result

    def __init__(self, description, enter=None, leave=None, show_map=False):
        self.description = Event(event=description)
        self.compass = Room.Compass()
        self.map = Room.Map()
        self.interactives = Room.Interactives()
        self.items = Room.Items()
        self.show_map = show_map
        self.events = {
            "roomEnter": Event(event=enter),
            "roomLeave": Event(event=leave),
        }
