import json

"""
This class return a json with id_error and its message for the user
"""


class Notification:

    id_ = None
    error = None

    def __init__(self, id_, error):
        self.id_error = id_
        self.error = error

    def message(self):
        return json.dumps(self.__dict__)
