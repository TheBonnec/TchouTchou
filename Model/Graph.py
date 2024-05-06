class Vertex:
    def __init__(self, value: str, cost: int, units: int) -> None:
        self.value: str = value
        self.cost: int = cost
        self.units: int = units
        self.nextVertices: list[Vertex] = []


class Graph:
    def __init__(self, name: str, vertices: list[Vertex]) -> None:
        self.name: str = name
        self.listVertices: list[Vertex] = vertices