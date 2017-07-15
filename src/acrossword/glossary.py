
class Glossary(set):
    """
    List of words to be used in puzzle
    """

    def sorted_by_len(self):
        return list(sorted(self, key=len))
