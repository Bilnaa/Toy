class Environment:
    """Holds variable bindings for a lexical scope."""

    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value=None):
        if name in self.values:
            raise RuntimeError(f"Variable '{name}' is already defined.")
        self.values[name] = value
        return value