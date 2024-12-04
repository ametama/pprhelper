from __future__ import annotations
from re import match

class Task:
    descriptor: str
    points: float
    root: Node
    results: list[Node]

class Node:
    directive: str
    points: float
    parent: Node
    children: list[Node]

def parseTask(lines):
    root = Node()
    root.directive = None
    root.parent = root
    root.children = []
    for line in lines:
        m = match(r"^(-*)(.*)#([^#]+)$", line)
        linerank, directive, points = m[1], m[2], m[3]
        linerank = len(linerank)
        parent = root
        # Traverse tree to last node.
        for i in range(linerank): parent = parent.children[-1]
        node = Node()
        node.directive = directive
        node.points = float(points)
        node.parent = parent
        node.children = []
        parent.children.append(node)
    return root

def parseSchema(filename):
    tasks: list[Task] = []
    with open(filename) as f:
        currtask = None
        tasklines = None
        for line in f.readlines():
            if line[0] == "/":
                if currtask != None:
                    currtask.root = parseTask(tasklines)
                    tasks.append(currtask)
                currtask = Task()
                tasklines = []
                m = match(r"^/(.*)#([^#]+)$", line)
                currtask.descriptor = m[1]
                currtask.points = float(m[2])
                currtask.results = []
            else:
                tasklines.append(line)
        currtask.root = parseTask(tasklines)
        tasks.append(currtask)
    return tasks

def main():
    out = []
    tasks = parseSchema("schema2.txt")
    for task in tasks:
        stack = task.root.children
        while len(stack) > 0:
            node = stack.pop(0)
            while True:
                print(node.directive)
                ans = input("> ")
                match ans:
                    case "y" | "Y":
                        task.results.append(node)
                        break
                    case "n" | "N":
                        stack = node.children + stack
                        break
                    case _:
                        try:
                            ans = float(ans)
                            node.points = ans
                            task.results.append(node)
                            break
                        except:
                            pass
        taskachieved = round(max(0, task.points + sum(map(lambda node: node.points, task.results))), 1)
        out.append(f"{task.descriptor}: {str(taskachieved)}p")
        for node in task.results: out.append(f"- {node.directive} ({str(round(node.points, 1))}p)")
    print(*out, sep="\n")
    achievedpts = sum(map(lambda task: max(0, task.points + sum(map(lambda node: node.points, task.results))), tasks))
    maxpts = sum(map(lambda task: task.points, tasks))
    print(f"Points achieved: {str(round(min(maxpts, achievedpts), 1))} / {str(round(maxpts, 1))}")

if __name__ == "__main__":
    main()
