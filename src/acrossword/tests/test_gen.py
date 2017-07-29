import random

from acrossword import (
    crossword,
    gen,
    glossary,
)


def test_gen1_simplest():
    g = glossary.Glossary({
        'cat',
        'sad',
    })
    cw = gen.random_gen(g, r=random.Random(0))
    cw.crop()

    assert cw == crossword.loads(
        ' s \n'
        'cat\n'
        ' d \n'
    )
