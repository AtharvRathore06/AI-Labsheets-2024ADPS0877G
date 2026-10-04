from agent import parse, find_path, WAREHOUSE


def run(text):
    grid, s, g = parse(text)
    return find_path(grid, s, g)


def test_main_map_has_path():
    path = run(WAREHOUSE)
    assert path is not None
    assert path[-1][1] == parse(WAREHOUSE)[2]


def test_path_never_enters_wall():
    grid, _, _ = parse(WAREHOUSE)
    for _, (r, c) in run(WAREHOUSE):
        assert grid[r][c] != "#"


def test_adjacent_goal():
    assert len(run("#####\n#SG##\n#####")) == 1


def test_blocked_goal():
    assert run("#####\n#S#G#\n#####") is None
