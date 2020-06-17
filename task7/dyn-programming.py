#!/usr/bin/env python
import os
import sys
import math
# import numpy as np


def memoize(log=False):
    cache = {}
    def wrapper(func):
        def wrapper(*args):
            key = ':'.join(str(a) for a in args)
            if key in cache:
                return cache[key]
            else:
                res = func(*args)
                cache[key] = res
                if log: print('Cache:', list(cache.values()))
                return res
        return wrapper

    return wrapper


class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.start = None
        self.end = None

    def parse(fpath: str):
        with open(fpath, 'rt') as f:
            raw = f.read()
        nodes = set()
        edges = []
        for i in (l for l in raw.splitlines() if l):
            fr, to, val = i.split()[:3]
            nodes.add(fr)
            nodes.add(to)
            edges.append((fr, to, int(val)))
        nodelist = list(nodes)
        nodelist.sort()
        g = Graph(nodelist, edges)

        # Finding start / end points
        to_dirs = [e[1] for e in edges]
        from_dirs = [e[0] for e in edges]

        start_cand = [n for n in nodes if n not in to_dirs]
        end_cand = [n for n in nodes if n not in from_dirs]
        if len(start_cand) > 1:
            raise Exception('Multiple start points')
        if len(end_cand) > 1:
            raise Exception('Multiple end points')
        try:
            g.start = start_cand[0]
            g.end = end_cand[0]
        except:
            print('No start/end node specified.')
        return g

    def from_edges(self, node):
        return [e for e in self.edges if e[0] == node]

    def to_edges(self, node):
        return [e for e in self.edges if e[1] == node]


def shortest_till_v(graph, v, cache=None):
    if cache is None:
        cache = {}

    incoming_edges = graph.to_edges(v)
    conc = lambda a, b: (a[0] + b[0], a[1] + b[1])
    lengths = []

    if v in cache:
        return cache[v]
    cache[v] = math.inf
    for fr, to, w in incoming_edges:
        ln = None

        if fr == graph.start:
            ln = (w, fr)
        else:
            ln = conc(shortest_till_v(graph, fr, cache), (w, fr))
            if ln[0] < cache[v]:
                cache[v] = ln[0]
        lengths.append(ln)

    m = min(lengths, key=lambda a: a[0])
    return m


if __name__ == '__main__':
    graph = Graph.parse(sys.argv[1])
    length, sequence = shortest_till_v(graph, graph.end)
    print('Min length:', length)
    print('Sequence:', ' -> '.join((*sequence, graph.end)))
