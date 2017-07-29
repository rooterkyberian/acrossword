import random
import typing as t


class Glossary(set):
    """
    List of words to be used in puzzle
    """

    def pop_random(self, words=None, r: random.Random = random):
        if words is None:
            words = self
        words = list(sorted(words))
        if not words:
            return None
        word = r.choice(words)
        self.remove(word)
        return word

    def containing(self, c: str) -> t.Generator[str, None, None]:
        """get words containing `c`"""
        return (
            word for word in self
            if c in word
        )
