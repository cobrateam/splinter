from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin

class Todo(Exception):
    pass

class TodoPlugin(ErrorClassPlugin):
    todo = ErrorClass(Todo, label='TODO', isfailure=True)
