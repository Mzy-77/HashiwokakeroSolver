from itertools import groupby

from Solver.puzzle import Island 

def FindCandidates(islands: list[Island]) -> list[ tuple[ int,int ] ] :
    Candidates: set[tuple[int, int]] = set()

    rows = sorted(islands, key=lambda island: ( island.row, island.column) )
    for _,rowsGroup in groupby(rows , key=lambda island: island.row):

        rowsGroup = list(rowsGroup)

        for first, second in zip(rowsGroup, rowsGroup[1:]):
            Candidates.add(
                (min(first.id, second.id), max(first.id, second.id))
            )

    columns = sorted(islands, key=lambda island: (island.column, island.row))
    for _,columnsGroup in groupby(columns, key=lambda Island: Island.column):
        columnsGroup = list(columnsGroup)

        for first, second in zip(columnsGroup, columnsGroup[1:]):
            Candidates.add(
                (min(first.id, second.id), max(first.id, second.id))
            )

    return sorted(Candidates)
    