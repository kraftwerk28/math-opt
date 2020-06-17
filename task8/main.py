import sys
import math
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Task:
    '''Represents a single task from input set'''
    duration: int   # I
    deadline: int   # D
    pre_cost: int   # a
    post_cost: int  # b

    def __hash__(self):
        return hash(
            (self.duration, self.deadline, self.pre_cost, self.post_cost)
        )


class Node:
    '''Branch-and-bound algorithm tree NODE'''

    def __init__(self):
        self.task: Optional[Task] = None
        self.cost: int = 0
        self.children: List[Node] = []
        self.discontinued: bool = False


class BranchAlg:
    '''Branch-and-bound algorithm implementation'''

    def __init__(self):
        self._step = 0
        self._tasks = []  # All tasks
        self._root = Node()  # Branching tree root
        self._last_optimal = self._root  # Last (leaf) optimal task
        self._tasks_left = []
        self.path = []
        self.record = math.inf

    def parse(filename: str):  # Parse input set from file
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
        tasks = [Task(0, 0, 0, 0) for _ in lines[0].split()]
        fs = ['duration', 'deadline', 'pre_cost', 'post_cost']
        for li, line in enumerate(lines[:4]):
            for i, v in enumerate(line.split()):
                setattr(tasks[i], fs[li], int(v))
        res = BranchAlg()
        res._tasks = tasks
        res._tasks_left = [t for t in tasks]
        return res

    def step(self, prev, traverse=False):

        self._step += 1
        print(f'\n----- step #{self._step} -----')
        for t in self._tasks_left:
            overtime = t.duration + (prev.task.duration if prev.task else 0)
            if overtime < t.deadline:
                cost = (t.deadline - overtime) * t.pre_cost
            else:
                cost = (overtime - t.deadline) * t.post_cost
            print(
                f'Task #{self._tasks.index(t) + 1}:'
                ' Penalty = {}; {}'.format(
                    cost, 'late' if overtime < t.deadline else 'early'
                )
            )

            # Generate new sub-Node
            n = Node()
            n.task = t
            n.cost = cost
            prev.children.append(n)

        best = min(prev.children, key=lambda t: t.cost)
        best.discontinued = True
        self.path.append(self._tasks.index(best.task) + 1)
        self._last_optimal = best
        self._tasks_left.pop(self._tasks_left.index(best.task))

    def _task_num(self, node: Node) -> str:
        try:
            return str(self._tasks.index(node.task) + 1)
        except ValueError:
            return '*'

    def retraverse(self):
        def find_free_node(n):
            if not n.discontinued:
                return n
            for ch in n.children:
                return find_free_node(n)
        free = find_free_node(root)

    def print_tree(self):
        print('-' * 40)

        def print_node(node: Node, indent=0):
            if indent:
                idnt = ('    ' * (indent - 1)) + '^---'
                idnt = '|' + idnt[1:]
                rpr = idnt + f'{self._task_num(node)}: {node.cost}'
                if node.discontinued:
                    rpr += ' ⨯'
                print(rpr)
            for ch in node.children:
                print_node(ch, indent + 1)
        print_node(self._root)

    def find_record(self):
        self._tasks_left = [t for t in self._tasks]
        while self._tasks_left:
            self.step(self._last_optimal)
        self.retraverse()


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print('File not specified.')
        sys.exit(1)

    alg = BranchAlg.parse(args[0])
    alg.find_record()
    alg.print_tree()

    print('\nFinal result:')
    print(' -> '.join(str(t) for t in alg.path))
