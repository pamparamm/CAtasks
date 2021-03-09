from collections import deque
from pathlib import Path
from typing import Deque, List, Set, Tuple


def main():
    input_data = IOInteractor.read_input()
    graph = Graph(input_data)
    IOInteractor.write_output(graph.check_if_bigraph())


class Graph:
    def __init__(self, matrix_data: List[str]):
        self.vertices_count = int(matrix_data[0])
        self.vertices_matrix = matrix_data[1:]
        self.vertices = {
            str(vertex): [
                str(other_vertex)
                for other_vertex in range(1, self.vertices_count + 1)
                if self.vertices_matrix[vertex - 1].split()[other_vertex - 1]
                != "0"
            ]
            for vertex in range(1, self.vertices_count + 1)
        }

    def check_if_bigraph(self) -> List[str]:
        output: List[str] = ["Y"]
        color_count = 2
        colors: List[List[str]] = [[] for _ in range(color_count)]
        visited_vertices: Set[str] = set()
        vertices_queue: Deque[Tuple[str, int]] = deque()
        current_vertex = ("1", 0)
        vertices_queue.append(current_vertex)
        visited_vertices.add(current_vertex[0])
        while vertices_queue:
            current_vertex = vertices_queue.popleft()
            colors[current_vertex[1]].append(current_vertex[0])
            connected_vertices = self.vertices[current_vertex[0]]
            for connected_vertex_name in connected_vertices:
                connected_vertex = (
                    connected_vertex_name,
                    (current_vertex[1] + 1) % color_count,
                )
                if connected_vertex[0] not in visited_vertices:
                    visited_vertices.add(connected_vertex[0])
                    vertices_queue.append(connected_vertex)
                elif connected_vertex[0] in colors[current_vertex[1]]:
                    return ["N"]
        for color in colors:
            output += [" ".join(color)] + ["0"]
        return output[:-1]


class IOInteractor:
    _IN_PATH = Path("./in.txt").absolute()
    _OUT_PATH = Path("./out.txt").absolute()

    @classmethod
    def read_input(cls) -> List[str]:
        with cls._IN_PATH.open("r") as in_file:
            return in_file.read().splitlines()

    @classmethod
    def write_output(cls, output: List[str]):
        with cls._OUT_PATH.open("w") as out_file:
            return out_file.writelines("\n".join(output))


if __name__ == "__main__":
    main()
