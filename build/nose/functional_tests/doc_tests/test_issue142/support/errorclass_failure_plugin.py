from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin

class Todo(Exception):
    pass

class TodoPlugin(ErrorClassPlugin):

    name = "todo"

    todo = ErrorClass(Todo, label='TODO', isfailure=True)

class NonFailureTodoPlugin(ErrorClassPlugin):

    name = "non-failure-todo"

    todo = ErrorClass(Todo, label='TODO', isfailure=False)
