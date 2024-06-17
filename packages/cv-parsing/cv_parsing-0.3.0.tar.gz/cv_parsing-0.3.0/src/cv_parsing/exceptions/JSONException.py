class JSONException(Exception):
    def __init__(self, message):
        super(JSONException, self).__init__(message)
