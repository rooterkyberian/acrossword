import copy
import itertools
import random
import typing as t

from acrossword import crossword
from acrossword.glossary import Glossary


def _indexes(word: str, c: str):
    return (
        index
        for index, word_c in enumerate(word)
        if word_c == c
    )


def random_generator(
        glossary: Glossary,
        size=None,
        r: random.Random = random,
) -> t.Generator[crossword.Crossword, None, None]:
    if not size:
        # assume longest words would line up in the same axis
        max_combo_length = sum(
            list(
                sorted(len(word) for word in glossary)
            )[:len(glossary) // 2]
        )
        # and as we are starting from a center, so twice the space is needed
        size = 2 * (2 * max_combo_length,)
    glossary = copy.deepcopy(glossary)
    cw = crossword.Crossword.empty(size)

    center = size[0] // 2, size[1] // 2
    start_word = glossary.pop_random(r=r)

    cw.write(
        start_word,
        pos=center,
        vertical=bool(r.getrandbits(1)),
    )
    yield cw

    spots_checked = set()
    while glossary:
        # find potential spots for a word start
        spots = cw.potential_spots
        spots -= spots_checked
        if not spots:
            break

        pos, vertical = r.choice(list(sorted(spots)))
        c = cw[pos]
        word = glossary.pop_random(
            words=glossary.containing(c),
            r=r,
        )
        if word is None:
            spots_checked.add((pos, vertical))
            continue

        try:
            offset = r.choice(list(
                _indexes(word, c)
            ))
            if vertical:
                pos = pos[0] - offset, pos[1]
            else:
                pos = pos[0], pos[1] - offset
            cw.write(word, pos=pos, vertical=vertical)
        except crossword.WordWriteError:
            glossary.add(word)
        else:
            taken_spots = [
                (pos[0] + y_offset, pos[1] + x_offset)
                for y_offset, x_offset in
                itertools.combinations_with_replacement(range(-1, 2), r=2)
            ]

            for surrounding_pos in taken_spots:
                spots_checked.add((surrounding_pos, True))
                spots_checked.add((surrounding_pos, False))

        yield cw


def gen_limited_fails(gen, max_fails):
    crossovers = -1
    fail_streak = 0
    cw = None
    for cw in gen:
        if cw.letter_overlaps > crossovers:
            fail_streak -= 1
        else:
            fail_streak += 1
        crossovers = cw.letter_overlaps
        if fail_streak > max_fails:
            break
    return cw


def random_gen(
        *args,
        **kwargs
) -> crossword.Crossword:
    return gen_limited_fails(
        random_generator(*args, **kwargs),
        max_fails=1000,
    )
