from ward import test


@test("Test ward setup")
def _():
    assert "!" in "Hello world !"
