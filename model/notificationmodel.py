import json


class Notification:

    id_ = None
    error = None

    def __init__(self, id_, error):
        self.id_error = id_
        self.error = error

    def Message(self):
        return json.dumps(self.__dict__)
