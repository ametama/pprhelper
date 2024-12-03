from __future__ import annotations
from re import match

class Node:
    directive: str
    points: float
    parent: Node
    children: list[Node]

def parseSchema(filename):
    with open(filename) as f:
        root = Node()
        root.directive = None
        root.parent = root
        root.children = []
        lines = f.readlines()
        maxpts = float(lines[0])
        for line in f.readlines()[1:]:
            m = match(r"^(-*)(.*)#([^#]+)$", line)
            lineRank, directive, points = m[1], m[2], m[3]
            lineRank = len(lineRank)
            parent = root
            # Traverse tree to last node.
            for i in range(lineRank): parent = parent.children[-1]
            node = Node()
            node.directive = directive
            node.points = float(points)
            node.parent = parent
            node.children = []
            parent.children.append(node)
        return maxpts, root

def main():
    maxpts, root = parseSchema("schema.txt")
    outLines = []
    outPts = []
    stack = [root]
    while node := stack.pop(0):
        while True:
            print(node.directive)
            ans = input("> ")
            match ans:
                case "y" | "Y":
                    outLines.append(f"{node.directive} ({str(round(node.points, 1))}p)")
                    outPts.append(node.points)
                    stack = node.children + stack
                case "n" | "N":
                    pass
                case _:
                    continue
            break
    for line in outLines: print(line)
    print(f"Points achieved: {maxpts + sum(outPts)} / {maxpts}")

if __name__ == "__main__":
    main()
