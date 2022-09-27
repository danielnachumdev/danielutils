from ..Classes.DataStructures import Stack
from ..Text import is_matching
import re


class DomObject:
    def __init__(self, raw_html: str) -> None:
        self.raw_html: str = raw_html.strip()
        self.children: list[DomObject] = []
        self.name: str = ""
        self.attributes: dict = dict()
        self.__analize()

    def __analize(self) -> None:
        lines = self.raw_html.split("\n")
        stack = []
        i = 0
        scope = 0
        exclude = ["link", "meta"]
        OPEN, CLOSE = True, False
        while i < len(lines):
            line = lines[i].strip()
            # if not empty line
            if re.search(r"[\w<>]+", line):
                # if line has open tag as first char afterspaces
                if re.search(r"^[\t ]*<.*", line):
                    if re.search(r"^</", line):
                        # get first word after </
                        name = re.findall(r"</([\w]+){1}", line)[0]
                        if name not in exclude:
                            scope -= 1
                        stack.append((scope, name, CLOSE, i))
                    elif re.search(r"</\w*>$", line):
                        name = re.findall(r"</([\w]+)>$", line)[0]
                        stack.append((scope, name, OPEN, i))
                        stack.append((scope, name, CLOSE, i))
                    else:
                        # get first word after <
                        res = re.findall(r"<([\w]+){1}", line)
                        if res:
                            name = res[0]
                        # if tag closes in the same line
                            if re.search(r">$", line):
                                stack.append((scope, name, OPEN, i))
                                if name not in exclude:
                                    scope += 1
                                else:
                                    stack.append((scope, name, CLOSE, i))
                            else:
                                # multiline tag statment
                                stack.append((scope, name, OPEN, i))
                                if name not in exclude:
                                    scope += 1
                        else:
                            # nonesense e.g: '<!-- Google tag (gtag.js) -->' '<!DOCTYPE html>'
                            pass
                else:
                    if re.search(r"</\w*>$", line):
                        # get first word after </
                        name = re.findall(r"</([\w]+){1}", line)[0]
                        if name not in exclude:
                            scope -= 1
                        stack.append((scope, name, CLOSE, i))
                    elif re.search(r">$", line):
                        # end multilne tag statment
                        pass
                    else:
                        # just inner text with no tags
                        pass
            i += 1
        curr = None
        SCOPE, NAME, STATE, LINE = 0, 1, 2, 3
        for i, tag_statment in enumerate(stack[1:-1]):
            if curr == None:
                curr = tag_statment
            else:
                if curr[SCOPE] == tag_statment[SCOPE] and curr[NAME] == tag_statment[NAME] and curr[STATE] == OPEN and tag_statment[STATE] == CLOSE:
                    self.children.append(
                        DomObject("\n".join(lines[curr[LINE]: tag_statment[LINE]+1])))
                    curr = None

        self.name = stack[0][NAME]
        if name not in ["style", "script"]:
            for line in lines[stack[0][LINE]:stack[1][LINE]+1]:
                line = line.strip()
                attributes = re.findall(r"\b\w+\b(?==\")", line)
                for att in attributes:
                    res = re.findall(rf"[^\b{att}\b]\"([^\"]+)\"", line)
                    if res:
                        self.attributes[att] = res[0][2:-1]
                self.inner_html = re.findall(r">(.*)<")
        # do thigs for self

    def __str__(self) -> str:
        # s = " ".join([k for k in self.attributes.keys()])
        return f"<{self.name}>"

    def __repr__(self) -> str:
        return str(self)
# (?<=^([^"]|"[^"]*")*)text
# \b\w*\b
