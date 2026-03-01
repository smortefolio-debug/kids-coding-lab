"""Colorful Click-the-Ball game for kids.

Run:
    python3 game.py
"""

import random
import tkinter as tk


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
BALL_SIZE = 60
START_SPEED_X = 5
START_SPEED_Y = 4


class BallGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Click the Bouncy Ball!")

        self.score = 0
        self.speed_x = START_SPEED_X
        self.speed_y = START_SPEED_Y

        # A colorful sky-blue play area.
        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg="#87CEEB",  # sky blue
            highlightthickness=0,
        )
        self.canvas.pack()

        # Score text at the top-left corner.
        self.score_text = self.canvas.create_text(
            15,
            15,
            anchor="nw",
            text="Score: 0",
            font=("Arial", 20, "bold"),
            fill="#1F2937",
        )

        # Add a happy title at the top center.
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            20,
            text="Click the ball as many times as you can!",
            font=("Arial", 16, "bold"),
            fill="#7C3AED",
        )

        # Create a colorful ball.
        x1, y1 = 100, 100
        x2, y2 = x1 + BALL_SIZE, y1 + BALL_SIZE
        self.ball = self.canvas.create_oval(
            x1,
            y1,
            x2,
            y2,
            fill="#FF6B6B",  # bright pink-red
            outline="#F59E0B",  # warm yellow border
            width=4,
        )

        # Listen for mouse clicks.
        self.canvas.bind("<Button-1>", self.on_click)

        # Start moving the ball.
        self.move_ball()

    def move_ball(self) -> None:
        """Move the ball and make it bounce off walls."""
        self.canvas.move(self.ball, self.speed_x, self.speed_y)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        # Bounce on left or right wall.
        if x1 <= 0 or x2 >= WINDOW_WIDTH:
            self.speed_x = -self.speed_x

        # Bounce on top or bottom wall.
        if y1 <= 0 or y2 >= WINDOW_HEIGHT:
            self.speed_y = -self.speed_y

        # Repeat this function every 16ms (~60 FPS).
        self.root.after(16, self.move_ball)

    def on_click(self, event: tk.Event) -> None:
        """Give a point when the click lands on the ball."""
        clicked_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if self.ball in clicked_items:
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

            # Move ball to a random new spot for extra fun.
            self.randomize_ball_position()

            # Change to a random bright color when clicked.
            self.canvas.itemconfig(self.ball, fill=self.random_bright_color())

    def randomize_ball_position(self) -> None:
        """Place the ball in a random position inside the window."""
        new_x1 = random.randint(0, WINDOW_WIDTH - BALL_SIZE)
        new_y1 = random.randint(50, WINDOW_HEIGHT - BALL_SIZE)
        new_x2 = new_x1 + BALL_SIZE
        new_y2 = new_y1 + BALL_SIZE
        self.canvas.coords(self.ball, new_x1, new_y1, new_x2, new_y2)

    @staticmethod
    def random_bright_color() -> str:
        """Return a random bright color in hex format."""
        bright_values = ["66", "99", "CC", "FF"]
        return "#" + "".join(random.choice(bright_values) for _ in range(3))


def main() -> None:
    root = tk.Tk()
    BallGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
