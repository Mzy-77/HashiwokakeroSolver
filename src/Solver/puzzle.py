from dataclasses import dataclass

@dataclass(frozen=True)
class Island:
    id: int
    row: int
    column: int
    required: int

@dataclass
class Puzzle:
    rows: int
    columns: int
    islands: list[Island]

    def validate(self) -> None:
        if self.rows <= 0 or self.columns <= 0:
            raise ValueError("Grid dimensions must be positive.")

        if not self.islands:
            ValueError("Puzzle must contain islands.")

        ids = set()
        positions = set()

        for island in self.islands :
            if island.id < 0 or island.id in ids :
                raise ValueError("Island IDs must be unique and non-negative.")

            ids.add(island.id)

            if not (0 <= island.row < self.rows):
                raise ValueError(f"Invalid row for island {island.id}.")
            if not (0 <= island.column < self.columns):
                raise ValueError(f"Invalid column for island {island.column}")

            position = (island.row, island.column)
            if position in positions:
                raise ValueError("Two islands cannot occupy the same cell.")

            positions.add(position)

            if not 1 <= island.required <= 8:
                raise ValueError("Island requirements must be between 1 and 8.")

@dataclass(frozen=True)
class Bridge:
    island_a: int
    island_b: int
    count: int = 1

    def __post_init__(self):
        if self.island_a == self.island_b:
            raise ValueError("An island cannot connect to itself.")

        if self.island_a > self.island_b:
            first = self.island_b
            second = self.island_a
            object.__setattr__(self, "island_a", first)
            object.__setattr__(self, "island_b", second)

        if self.count not in (1, 2):
            raise ValueError("Bridge count must be 1 or 2.")
