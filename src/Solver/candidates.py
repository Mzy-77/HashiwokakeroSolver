from itertools import groupby

from Solver.puzzle import Island 

def FindCondidates(islands: list[Island]) -> list[ tuple[ int,int ] ] :
    Candidates = set()

    rows = sorted(islands, key=lambda island: ( island.row, island.column) )
    for _,rowsGroup in groupby(rows , key=lambda island: island.row):

        rowsGroup = list(rowsGroup)

        for first, second in zip(rowsGroup, rowsGroup[1:]):
            Candidates.add(
                tuple(sorted((first.id, second.id)))
            )

    colums = sorted(islands, key=lambda island: (island.column, island.row))
    for _,columsGroup in groupby(colums, key=lambda Island: Island.column):
        columsGroup = list(columsGroup)

        for fist, second in zip(columsGroup, columsGroup[1:]):
            Candidates.add(
                tuple(sorted((fist.id,second.id)))
            )

    return sorted(Candidates)
    