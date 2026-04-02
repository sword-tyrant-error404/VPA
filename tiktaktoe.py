#!/usr/bin/env python3
# games/tiktaktoe.py — runs as its own process
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from turtle import *
from tkinter import messagebox
from utils.tts import speak_male as talk


class TikTakToe:
    def __init__(self):
        self.cellCenter = {
            '1': (-200, 200), '2': (0, 200), '3': (200, 200),
            '4': (-200, 0),   '5': (0, 0),   '6': (200, 0),
            '7': (-200, -200),'8': (0, -200), '9': (200, -200),
        }
        self.turn = 'black'
        self.round = 0
        self.validMoves = list(self.cellCenter.keys())
        self.occupiedMoves = {'black': [], 'red': []}

    def draw_board(self):
        Screen()
        setup(600, 600, 10, 70)
        tracer(False)
        title("Tic Tac Toe")
        bgcolor('light yellow')
        hideturtle()
        pensize(5)
        for i in (-100, 100):
            up(); goto(300, i); down(); goto(-300, i); up()
            up(); goto(i, -300); down(); goto(i, 300); up()
        for cell, center in self.cellCenter.items():
            goto(center)
            write(cell, align='center', font=('Arial', 30, 'italic'))

    def position(self, x, y):
        if not (-300 < x < 300 and -300 < y < 300):
            return
        col = int((x + 300) // 200) + 1
        row = int((y + 300) // 200) + 1
        cell = str((3 - row) * 3 + col)
        if cell not in self.validMoves:
            messagebox.showerror("Invalid Move", "Cell already occupied.")
            return
        self.round += 1
        self.validMoves.remove(cell)
        self.occupiedMoves[self.turn].append(cell)
        goto(self.cellCenter[cell])
        dot(120, self.turn)
        update()
        if self._winner():
            self.validMoves = []
            messagebox.showinfo("Game Over", f'{self.turn} wins!')
            talk(f"Game over! {self.turn} wins!")
        elif self.round == 9:
            messagebox.showinfo("Game Over", "It's a tie!")
            talk("Game over! It's a tie!")
        self.turn = 'red' if self.turn == 'black' else 'black'

    def _winner(self):
        combos = [
            ['1','2','3'],['4','5','6'],['7','8','9'],
            ['1','4','7'],['2','5','8'],['3','6','9'],
            ['1','5','9'],['3','5','7'],
        ]
        return any(all(c in self.occupiedMoves[self.turn] for c in combo) for combo in combos)

    def main(self):
        self.draw_board()
        onscreenclick(self.position)
        done()


if __name__ == '__main__':
    talk("Starting Tic Tac Toe!")
    game = TikTakToe()
    game.main()
