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

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeError(f"Undefined variable '{name}'.")