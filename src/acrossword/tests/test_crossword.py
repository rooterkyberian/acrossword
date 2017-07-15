from acrossword import crossword

crossword_string_10x5 = '\n'.join([' ' * 10] * 5) + '\n'


def test_crossword_loads_empty():
    loaded = crossword.loads(crossword_string_10x5)
    assert loaded, crossword.Crossword.empty((5, 10))


def test_crossword_dumps():
    empty_10x5 = crossword.Crossword.empty((5, 10))
    assert crossword.dumps(empty_10x5) == crossword_string_10x5


def test_crossword_write_word():
    cs_5x5 = crossword.Crossword.empty((5, 5))
    cs_5x5.write("żółw", pos=(1, 1))

    assert cs_5x5 == crossword.loads(
        '     \n'
        ' żółw\n'
        '     \n'
        '     \n'
        '     \n'
    )


def test_crossword_write_word_vertically():
    cs_5x6 = crossword.Crossword.empty((6, 5))
    cs_5x6.write("cat", pos=(1, 1), vertical=True)

    assert cs_5x6 == crossword.loads(
        '     \n'
        ' c   \n'
        ' a   \n'
        ' t   \n'
        '     \n'
        '     \n'
    )
