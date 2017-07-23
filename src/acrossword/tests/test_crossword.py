from acrossword import crossword

crossword_string_10x5 = '\n'.join([' ' * 10] * 5) + '\n'


def test_crossword_loads_empty():
    loaded = crossword.loads(crossword_string_10x5)
    assert loaded, crossword.Crossword.empty((5, 10))


def test_crossword_dumps():
    empty_10x5 = crossword.Crossword.empty((5, 10))
    assert crossword.dumps(empty_10x5) == crossword_string_10x5


def test_crossword_write_word():
    cw_6x5 = crossword.Crossword.empty((5, 6))
    cw_6x5.write("żółw", pos=(1, 2))

    assert cw_6x5 == crossword.loads(
        '      \n'
        '  żółw\n'
        '      \n'
        '      \n'
        '      \n'
    )
    assert cw_6x5.word_placements == {"żółw": (1, 2, False)}


def test_crossword_write_word_vertically():
    cw_5x6 = crossword.Crossword.empty((6, 5))
    cw_5x6.write("cat", pos=(2, 1), vertical=True)

    assert cw_5x6 == crossword.loads(
        '     \n'
        '     \n'
        ' c   \n'
        ' a   \n'
        ' t   \n'
        '     \n'
    )
    assert cw_5x6.word_placements == {"cat": (2, 1, True)}


def test_crossword_multiple_writes():
    cw = crossword.Crossword.empty((3, 3))
    cw.write('cat', pos=(0, 2), vertical=True)
    cw.write('hat', pos=(2, 0), vertical=False)
    cw.write('mac', pos=(0, 0), vertical=False)

    assert cw == crossword.loads(
        'mac\n'
        '  a\n'
        'hat\n'
    )
    assert cw.letter_overlaps == 2


def test_crossword_shrink():
    bloated_crossword = crossword.loads(
        '      \n'
        '   c  \n'
        '   a  \n'
        ' hat  \n'
        '      \n'
        '      \n'
    )
    bloated_crossword.crop()

    assert bloated_crossword == crossword.loads(
        '  c\n'
        '  a\n'
        'hat\n'
    )
