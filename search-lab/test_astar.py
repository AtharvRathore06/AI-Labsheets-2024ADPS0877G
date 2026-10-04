from astar import parse, astar, bfs, WAREHOUSE


def solve(text, algo=astar):
    grid, s, g = parse(text)
    return algo(grid, s, g)


def test_original_map():
    path, _ = solve(WAREHOUSE)
    assert path[0] == parse(WAREHOUSE)[1]
    assert path[-1] == parse(WAREHOUSE)[2]


def test_trivial():
    path, _ = solve("#####\n#SG##\n#####")
    assert len(path) == 2


def test_unreachable_terminates():
    path, _ = solve("#######\n#S....#\n###.###\n#...#G#\n#######")
    assert path is None


def test_two_routes_picks_shortest():
    text = "#######\n#S...G#\n#.###.#\n#.....#\n#######"
    path, _ = solve(text)
    assert len(path) - 1 == 4


def test_astar_matches_bfs_length():
    a, _ = solve(WAREHOUSE, astar)
    b, _ = solve(WAREHOUSE, bfs)
    assert len(a) == len(b)
