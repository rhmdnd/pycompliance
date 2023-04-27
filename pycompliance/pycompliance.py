import typing
import re

class Node:

    def __init__(self, id: str) -> None:
        self.id = id
        self.children = []

    def find(self, id: str) -> 'Node|None':
        if self.id == id:
            return self
        for node in self.children:
            n = node.find(id)
            if n:
                return n

    def traverse(self, node: 'Node') -> 'list[Node]':
        r = []
        for child in node.children:
            res = self.traverse(child)
            r = r + res
        r.append(node)
        return r


class Benchmark(Node):

    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.id = name
        self.version = ''

    def add_section(self, section: 'Section'):
        # see if the section already exists
        s = self.find(section.id)
        if s:
            return s

        if '.' not in section.id:
            self.children.append(section)
            return
        parent_id = self._find_parent_id(section.id)
        parent = self.find(parent_id)
        if not parent:
            raise SectionNotFound(parent_id)
        parent.children.append(section)

    def add_control(self, control: 'Control'):
        parent_id = self._find_parent_id(control.id)
        parent = self.find(parent_id)
        if not parent:
            raise SectionNotFound(parent_id)
        parent.children.append(control)

    def _find_parent_id(self, id: str) -> str:
        pattern = re.compile(r"^(.+)\.(\d+)$")
        m = pattern.search(id)
        return m.group(1)


class Section(Node):

    def __init__(self, id: str):
        super().__init__(id)
        self.id = id
        self.title = None
        self.description = None

class Control(Node):

    def __init__(self, id: str):
        super().__init__(id)
        if not isinstance(id, str):
            raise InvalidControlException(control_id=id)
        self.id = id
        self.title = None
        self.description = None
        self.level = None
        self.remediation = None
        self.rationale = None
        self.audit = None
        self.assessment = None

    @classmethod
    def from_dict(cls, d: typing.Dict[str, typing.Any]) -> 'Control':
        control_id = d.get('id')
        if control_id is None:
            raise InvalidControlException()
        c = cls(id=control_id)
        c.title = d.pop("title", None)
        c.description = d.pop("description", None)
        c.level = d.pop("level", None)
        c.remediation = d.pop("remediation", None)
        c.rationale = d.pop("rationale", None)
        c.audit = d.pop("audit", None)
        c.assessment = d.pop("assessment", None)
        return c

class InvalidControlException(Exception):
    def __init__(self, control_id=None):
        message = "Control ID not set"
        if control_id:
            message = f"Invalid control ID {control_id}"
        super().__init__(message)


class SectionNotFound(Exception):
    def __init__(self, section_id=None):
        message = f"Failed to find section {section_id}"
        super().__init__(message)
