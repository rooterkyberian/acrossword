import io
import typing as t

import numpy


def _encode(c):
    return ord(c)


def _decode(b):
    return chr(b)


class Crossword:
    def __init__(
            self,
            board,
    ):
        self.board = board
        self.word_placements = {}  # { word: (y, x, vertical), ... }
        self.letter_overlaps = 0

    @classmethod
    def empty(
            cls,
            maxsize: t.Tuple[int, int] = (100, 100)
    ):
        return cls(numpy.zeros(maxsize, dtype=numpy.uint32))

    def __eq__(self, other):
        return numpy.array_equal(self.board, other.board)

    def __getitem__(self, pos):
        return _decode(self.board[pos])

    def write(
            self,
            word: str,
            pos: t.Tuple[int, int],
            vertical: bool = False,
    ):
        """

        TODO: use custom exceptions instead of ValueError

        :param word: w
        :param pos: (y, x) to start word from
        :param vertical:
            True if word should be written vertical (up->down)
            instead for horizontally (left->right)
        """
        assert len(word) > 1, (
            "Word cannot contain less than 2 characters in a crossword"
        )
        y, x = pos

        matched_chars = 0
        board = numpy.copy(self.board)
        if vertical:  # make UP new LEFT
            board = numpy.rot90(board, axes=(1, 0))
            board = numpy.flip(board, 0)
            y, x = x, y

        if y >= board.shape[1] or len(word) + x > board.shape[1]:
            raise ValueError("Word would exceed board bounds")

        # check if some word does not already exist at these coordinates
        if x - 1 > 0 and self.board[y][x - 1]:
            raise ValueError("Word would start right after another word")
        if len(word) + x + 1 < board.shape[1] and board[y][x]:
            raise ValueError("Word would start right before another word")

        encoded_word = [_encode(c) for c in word]
        for cur_x, c in enumerate(encoded_word, start=x):
            c_on_table = board[y][cur_x]
            if c_on_table and c != c_on_table:
                raise ValueError(
                    f"Word doesn't match {_decode(c_on_table)}!={_decode(c)}"
                )
            if not c_on_table:
                board[y][cur_x] = c
            else:
                matched_chars +=1

        if vertical:  # revert rotation
            board = numpy.rot90(board)
            board = numpy.flip(board, 0)
            y, x = x, y
        self.word_placements[word] = (y, x, vertical)
        self.board = board
        self.letter_overlaps += matched_chars

    @staticmethod
    def _remove_empty_rows(board: numpy.ndarray) -> numpy.ndarray:
        """
        Remove empty rows from board
        """
        board_height = board.shape[0]
        first_non_empty = last_non_empty = 0  # init only needed if height == 0
        for first_non_empty in range(board_height):
            if numpy.any(board[first_non_empty]):
                break
        for last_non_empty in range(board_height - 1, first_non_empty - 1, -1):
            if numpy.any(board[last_non_empty]):
                break
        return board[first_non_empty:last_non_empty + 1]

    def crop(self):
        """
        Trim empty spaces out of the crossword
        """
        board = self.board
        board = self._remove_empty_rows(board)
        board = numpy.rot90(board)
        board = self._remove_empty_rows(board)
        self.board = numpy.rot90(board, axes=(1, 0))


def dumps(crossword, empty=' '):
    dump = io.StringIO()
    for row in crossword.board:
        for c in row:
            dump.write(_decode(c) if c else empty)
        dump.write('\n')
    return dump.getvalue()


def loads(crossword_string, empty=' '):
    rows = [[]]
    for c in crossword_string:
        if c == '\r':  # ignore carriage return
            continue

        if c == '\n':
            if len(rows) >= 2 and rows[-1] and not rows[-2]:
                raise ValueError(
                    f"line {len(rows)}: "
                    'Empty lines are not allowed mid cross matrix'
                )
            if not (len(rows[0]) == len(rows[-1])):
                raise ValueError(
                    f"line {len(rows)}: "
                    "Each row of crossword matrix has to have the same length"
                )
            rows.append([])
        else:
            rows[-1].append(_encode(c) if c != empty else 0)

    while rows and not rows[-1]:  # remove empty trailing rows
        rows.pop()

    if not rows:
        raise ValueError("Crossword string was empty?")

    board = numpy.array(rows, dtype=numpy.uint32)
    crossword = Crossword(board)
    return crossword
