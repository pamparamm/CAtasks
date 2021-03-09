from collections import deque
from pathlib import Path
from typing import Deque, List, Set, Tuple


def main():
    input_data = IOInteractor.read_input()
    knight_pos = NotationConverter.from_chess(input_data[0])
    pawn_pos = NotationConverter.from_chess(input_data[1])
    board_dfs = BoardDFS(knight_pos, pawn_pos)
    IOInteractor.write_output(
        [
            NotationConverter.to_chess(result)
            for result in board_dfs.get_path_to_pawn()
        ]
    )


class IOInteractor:
    _IN_PATH = Path("./in.txt").absolute()
    _OUT_PATH = Path("./out.txt").absolute()

    @classmethod
    def read_input(cls) -> List[str]:
        with cls._IN_PATH.open("r") as in_file:
            return in_file.read().splitlines()

    @classmethod
    def write_output(cls, output: List[str]):
        with cls._OUT_PATH.open("w") as out_file:
            return out_file.writelines("\n".join(output))


class NotationConverter:
    CONVERTER_SHIFT = ord("a")

    @classmethod
    def from_chess(cls, chess_notation: str) -> Tuple[int, int]:
        return (
            ord(chess_notation[0]) - cls.CONVERTER_SHIFT,
            int(chess_notation[1]) - 1,
        )

    @classmethod
    def to_chess(cls, position: Tuple[int, int]) -> str:
        return f"{chr(position[0] + cls.CONVERTER_SHIFT)}{position[1]+1}"


class BoardDFS:
    LEFT_BOUND, RIGHT_BOUND, BOTTOM_BOUND, UP_BOUND = 0, 7, 0, 7
    KNIGHT_MOVES: List[Tuple[int, int]] = [
        (1, 2),  # Move format: (delta_col, delta_row)
        (-1, 2),
        (-2, 1),
        (-2, -1),
        (-1, -2),
        (1, -2),
        (2, -1),
        (2, 1),
    ]
    KNIGHT_MOVES.reverse()
    PAWN_MOVES = ((-1, -1), (1, -1))

    def __init__(self, knight_pos: Tuple[int, int], pawn_pos: Tuple[int, int]):
        self.initial_knight_pos = knight_pos
        self.pawn_pos = pawn_pos

    def get_path_to_pawn(self) -> List[Tuple[int, int]]:
        output: List[Tuple[int, int]] = []
        is_running = True
        forbidden_positions = [
            (self.pawn_pos[0] + a, self.pawn_pos[1] + b)
            for (a, b) in self.PAWN_MOVES
        ]
        visited_positions: Set[Tuple[int, int]] = set()
        position_stack: Deque[Tuple[int, int]] = deque()
        position_stack.append(self.initial_knight_pos)
        while position_stack and is_running:
            cur_position = position_stack.pop()
            visited_positions.add(cur_position)
            output.append(cur_position)
            possible_moves = [
                (cur_position[0] + a, cur_position[1] + b)
                for (a, b) in self.KNIGHT_MOVES
                if (self.LEFT_BOUND <= cur_position[0] + a <= self.RIGHT_BOUND)
                and (self.BOTTOM_BOUND <= cur_position[1] + b <= self.UP_BOUND)
            ]
            for move in possible_moves:
                if move == self.pawn_pos:
                    output.append(move)
                    is_running = False
                    break
                if (
                    move not in visited_positions
                    and move not in forbidden_positions
                ):
                    position_stack.append(move)
        return output


if __name__ == "__main__":
    main()
