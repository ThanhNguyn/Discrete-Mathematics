"""Dự án 1.3 - Trình lập lịch môn học.

Mỗi môn là một chuỗi và mỗi cạnh ``A -> B`` nghĩa là phải học A trước B.
"""
from __future__ import annotations

from collections import deque
from itertools import combinations


class CourseScheduler:
    def __init__(self, courses, prerequisites):
        self.courses = tuple(dict.fromkeys(courses))
        self._index = {course: i for i, course in enumerate(self.courses)}
        if len(self._index) != len(self.courses):
            raise ValueError("danh sách môn học có giá trị không hợp lệ")
        self.prerequisites = tuple(prerequisites)
        self.graph = {course: set() for course in self.courses}
        self.indegree = {course: 0 for course in self.courses}
        for prerequisite, course in self.prerequisites:
            if prerequisite not in self.graph or course not in self.graph:
                raise ValueError("ràng buộc chứa môn không có trong danh sách")
            if course not in self.graph[prerequisite]:
                self.graph[prerequisite].add(course)
                self.indegree[course] += 1

    def hop_le(self) -> bool:
        return len(self.lo_trinh()) == len(self.courses)

    def lo_trinh(self):
        indegree = self.indegree.copy()
        ready = deque(sorted(course for course in self.courses if indegree[course] == 0))
        order = []
        while ready:
            course = ready.popleft()
            order.append(course)
            for next_course in sorted(self.graph[course]):
                indegree[next_course] -= 1
                if indegree[next_course] == 0:
                    ready.append(next_course)
        return order

    def lich_hoc(self, capacity=5):
        if capacity < 1:
            raise ValueError("số môn tối đa mỗi kỳ phải dương")
        if not self.hop_le():
            raise ValueError("ràng buộc tiên quyết có chu trình")
        if not self.courses:
            return []
        prerequisite_masks = [
            sum(1 << self._index[prerequisite] for prerequisite, course in self.prerequisites
                if course == name)
            for name in self.courses
        ]
        full_mask = (1 << len(self.courses)) - 1
        frontier = {0: []}
        while frontier:
            next_frontier = {}
            for completed, schedule in frontier.items():
                available = [
                    i for i, required in enumerate(prerequisite_masks)
                    if not completed & (1 << i) and required & ~completed == 0
                ]
                for count in range(1, min(capacity, len(available)) + 1):
                    for selected in combinations(available, count):
                        new_mask = completed
                        for index in selected:
                            new_mask |= 1 << index
                        if new_mask not in next_frontier:
                            next_frontier[new_mask] = schedule + [
                                tuple(self.courses[index] for index in selected)
                            ]
            if full_mask in next_frontier:
                return next_frontier[full_mask]
            frontier = next_frontier
        raise RuntimeError("không thể tạo lịch học")

    def so_hoc_ky_toi_thieu(self, capacity=5) -> int:
        return len(self.lich_hoc(capacity))


MON_CNTT = (
    "Lập trình cơ bản", "Toán rời rạc", "Cấu trúc dữ liệu",
    "Cơ sở dữ liệu", "Lập trình hướng đối tượng", "Mạng máy tính",
    "Hệ điều hành", "Công nghệ phần mềm", "Trí tuệ nhân tạo",
    "Phát triển ứng dụng web",
)
RANG_BUOC_CNTT = (
    ("Lập trình cơ bản", "Cấu trúc dữ liệu"),
    ("Lập trình cơ bản", "Lập trình hướng đối tượng"),
    ("Toán rời rạc", "Cấu trúc dữ liệu"),
    ("Cấu trúc dữ liệu", "Cơ sở dữ liệu"),
    ("Cấu trúc dữ liệu", "Hệ điều hành"),
    ("Lập trình hướng đối tượng", "Công nghệ phần mềm"),
    ("Cơ sở dữ liệu", "Phát triển ứng dụng web"),
    ("Mạng máy tính", "Hệ điều hành"),
    ("Hệ điều hành", "Công nghệ phần mềm"),
)


if __name__ == "__main__":
    scheduler = CourseScheduler(MON_CNTT, RANG_BUOC_CNTT)
    print("Hợp lệ:", scheduler.hop_le())
    print("Topo:", scheduler.lo_trinh())
    print("Lịch tối ưu:", scheduler.lich_hoc())
    print("Số học kỳ:", scheduler.so_hoc_ky_toi_thieu())
