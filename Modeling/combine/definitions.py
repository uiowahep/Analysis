class Command(object):
    """
    A class that reprensents a single command unit.
    A list of such can be splitted!
    """
    def __init__(self, name, what):
        object.__init__(self)
        self.what = what
        self.name = name

    def __add__(self, other):
        return Command(self.name + "__" + other.name, self.what + other.what)

    def __str__(self):
        return \
        """
        Command: {name}
        what: {what}
        """.format(name=self.name, what=",".join(self.what))

    def __repr__(self):
        return self.__str__()

    def toString(self):
        return "#\n# Command: {name}\n#\n".format(name=self.name) + "\n\n".join(self.what)

class Job(object):
    def __init__(self, name, cmds):
        self.name = name
        self.cmds = cmds

    def toString(self):
        return "\n\n\n\n\n\n\n\n\n".join([x.toString() for x in self.cmds])
