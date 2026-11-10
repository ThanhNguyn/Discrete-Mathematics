"""Bài 1.37 - Gom nhóm các email bằng Union-Find."""
from __future__ import annotations


class UnionFind:
    def __init__(self, values=()):
        self.parent = {}
        self.rank = {}
        for value in values:
            self.add(value)

    def add(self, value):
        if value not in self.parent:
            self.parent[value] = value
            self.rank[value] = 0

    def find(self, value):
        if value not in self.parent:
            self.add(value)
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]

    def union(self, first, second):
        self.add(first)
        self.add(second)
        root_first, root_second = self.find(first), self.find(second)
        if root_first == root_second:
            return
        if self.rank[root_first] < self.rank[root_second]:
            root_first, root_second = root_second, root_first
        self.parent[root_second] = root_first
        if self.rank[root_first] == self.rank[root_second]:
            self.rank[root_first] += 1


def gom_nhom_email(pairs):
    union_find = UnionFind()
    for first, second in pairs:
        union_find.union(first, second)
    groups = {}
    for email in union_find.parent:
        groups.setdefault(union_find.find(email), []).append(email)
    return [sorted(group) for group in sorted(groups.values(), key=lambda group: group[0])]


if __name__ == "__main__":
    pairs = [
        ("an@example.com", "a.nguyen@example.com"),
        ("a.nguyen@example.com", "nguyen.an@example.com"),
        ("binh@example.com", "b.tran@example.com"),
    ]
    for group in gom_nhom_email(pairs):
        print(group)
