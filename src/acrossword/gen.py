import copy
import itertools
import random

import numpy

from acrossword import crossword
from acrossword.glossary import Glossary


def random_gen(
        glossary: Glossary,
        size=None,
        r: random.Random = random,
) -> crossword.Crossword:
    if not size:
        max_combo_length = max(len(word) for word in glossary) * len(glossary)
        size = 2 * (max_combo_length,)
    glossary = copy.deepcopy(glossary)
    cw = crossword.Crossword.empty(size)

    center = size[0] // 2, size[1] // 2
    start_word = glossary.pop_random(r=r)

    cw.write(
        start_word,
        pos=center,
        vertical=bool(r.getrandbits(1)),
    )

    spots_checked = set()
    fail_streak = 0
    while glossary:
        potential_positions = numpy.argwhere(cw.board)

        spots = {
            (tuple(pos), rotated)
            for pos, rotated in itertools.chain.from_iterable(
            zip(x, (False, True))
            for x in itertools.permutations(potential_positions, 2)
        )
        }
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
            offset = word.index(c)
            if vertical:
                pos = pos[0] - offset, pos[1]
            else:
                pos = pos[0], pos[1] - offset
            cw.write(word, pos=pos, vertical=vertical)
        except ValueError as e:
            glossary.add(word)
            fail_streak += 1
        else:
            fail_streak -= 1
            spots_checked.add((pos, vertical))

        if fail_streak >= 10:
            break

    return cw
