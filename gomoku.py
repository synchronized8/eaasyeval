"""Gomoku game using tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 15
CELL_SIZE = 32
PADDING = 24
STONE_RADIUS = 12

EMPTY = 0
BLACK = 1
WHITE = 2


class GomokuGame:
    def __init__(self) -> None:
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK
        self.game_over = False

    def is_valid_move(self, row: int, col: int) -> bool:
        return (
            0 <= row < BOARD_SIZE
            and 0 <= col < BOARD_SIZE
            and self.board[row][col] == EMPTY
            and not self.game_over
        )

    def place_stone(self, row: int, col: int) -> bool:
        if not self.is_valid_move(row, col):
            return False
        self.board[row][col] = self.current_player
        if self.check_win(row, col):
            self.game_over = True
        else:
            self.current_player = WHITE if self.current_player == BLACK else BLACK
        return True

    def check_win(self, row: int, col: int) -> bool:
        player = self.board[row][col]
        if player == EMPTY:
            return False
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]
        for dr, dc in directions:
            count = 1
            count += self._count_in_direction(row, col, dr, dc, player)
            count += self._count_in_direction(row, col, -dr, -dc, player)
            if count >= 5:
                return True
        return False

    def _count_in_direction(self, row: int, col: int, dr: int, dc: int, player: int) -> int:
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count


class GomokuUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Gomoku")
        self.game = GomokuGame()

        canvas_size = PADDING * 2 + CELL_SIZE * (BOARD_SIZE - 1)
        self.canvas = tk.Canvas(
            root,
            width=canvas_size,
            height=canvas_size,
            bg="#DEB887",
            highlightthickness=0,
        )
        self.canvas.pack()

        self._draw_grid()
        self.canvas.bind("<Button-1>", self.handle_click)

    def _draw_grid(self) -> None:
        for i in range(BOARD_SIZE):
            x = PADDING + i * CELL_SIZE
            self.canvas.create_line(PADDING, x, PADDING + CELL_SIZE * (BOARD_SIZE - 1), x)
            self.canvas.create_line(x, PADDING, x, PADDING + CELL_SIZE * (BOARD_SIZE - 1))

    def handle_click(self, event: tk.Event) -> None:
        row, col = self._pixel_to_cell(event.x, event.y)
        if row is None or col is None:
            return
        if self.game.place_stone(row, col):
            self._draw_stone(row, col)
            if self.game.game_over:
                winner = "黑棋" if self.game.current_player == BLACK else "白棋"
                messagebox.showinfo("胜利", f"{winner}获胜！")

    def _pixel_to_cell(self, x: int, y: int) -> tuple[int | None, int | None]:
        left = PADDING - CELL_SIZE // 2
        right = PADDING + CELL_SIZE * (BOARD_SIZE - 1) + CELL_SIZE // 2
        if not (left <= x <= right and left <= y <= right):
            return None, None
        col = int(round((x - PADDING) / CELL_SIZE))
        row = int(round((y - PADDING) / CELL_SIZE))
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None, None

    def _draw_stone(self, row: int, col: int) -> None:
        x = PADDING + col * CELL_SIZE
        y = PADDING + row * CELL_SIZE
        color = "black" if self.game.board[row][col] == BLACK else "white"
        self.canvas.create_oval(
            x - STONE_RADIUS,
            y - STONE_RADIUS,
            x + STONE_RADIUS,
            y + STONE_RADIUS,
            fill=color,
            outline="black",
        )


def main() -> None:
    root = tk.Tk()
    GomokuUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
