import os
from dotenv import load_dotenv
from openai import OpenAI
import tkinter as tk
from tkinter import messagebox

load_dotenv()  # LOADS .env FILE
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # GETS API KEY FROM .env FILE
client = OpenAI(api_key=f"{OPENAI_API_KEY}")  # CONNECTS TO OPENAI API

def guess_letter(answer, letter, player, question_label):
    contained = False

    if letter in player["correct_chars"] or letter in player["wrong_chars"]:
        return f"----- You have already guessed letter {letter}! -----\n\n{question_label['text']}"

    if len(letter) != 1:
        return "----- Please enter a single letter! -----\n\n{question_label['text']}"

    for i in range(len(answer)):
        if answer[i] == letter:
            contained = True
            player["guess"] = player["guess"][: i * 2] + letter + player["guess"][i * 2 + 1:]
            if letter not in player["correct_chars"]:
                player["correct_chars"].append(letter)

    if contained:
        return f"***** CORRECT! *****\n {player['guess']}  FAILS: {', '.join(player['wrong_chars'])}\n\n{question_label['text']}"
    else:
        player["wrong_chars"].append(letter)
        player["lives"] -= 1
        if player["lives"] > 0:
            return f"----- WRONG! {player['lives']} LIVES LEFT! -----\n {player['guess']}  FAILS: {', '.join(player['wrong_chars'])}\n\n{question_label['text']}"
        elif player["lives"] == 0:
            return f"***** YOU LOST! *****\n The word was => {answer}"


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=1)
    return response.choices[0].message.content

def open_level_selection(root):
    level_window = tk.Toplevel(root)
    level_window.title("Select Level")

    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]

    for level in levels:
        level_button = tk.Button(level_window, text=level, command=lambda l=level: start_game(level_window, l))
        level_button.pack()

def start_game(level_window, selected_level):
    level_window.destroy()  # Close the level selection window

    # Additional code for level-specific logic can be added here
    answer = get_completion(f"Give me a {selected_level} Level word just write the word.").upper()
    question = get_completion(f"Define word '{answer}'. Keep it simple and short.").lower() + f"({len(answer)})"
    question = question.replace(answer.lower(), "_ " * len(answer)).capitalize()

    game_window = tk.Tk()
    app = GameApp(game_window, answer, question)
    game_window.mainloop()

class GameApp:
    def __init__(self, master, answer, question):
        self.master = master
        self.master.title("Word Guessing Game")
        self.player = {"lives": 5, "correct_chars": [], "wrong_chars": [], "guess": "_ " * len(answer)}
        self.answer = answer

        self.create_widgets()

        # Create question label only once
        self.question_label = tk.Label(self.master, text=question)
        self.question_label.pack()

    def create_widgets(self):
        self.guess_label = tk.Label(self.master, text="Guess a letter:")
        self.guess_label.pack()

        self.letter_entry = tk.Entry(self.master)
        self.letter_entry.pack()

        self.result_label = tk.Label(self.master, text="")
        self.result_label.pack()

        self.submit_button = tk.Button(self.master, text="Submit Guess", command=self.make_guess)
        self.submit_button.pack()

        # Bind the Enter key to the make_guess function
        self.master.bind('<Return>', lambda event=None: self.make_guess())


    def make_guess(self):
        letter = self.letter_entry.get().upper()
        result = guess_letter(self.answer, letter, self.player, self.question_label)
        self.result_label.config(text=result)

        if "_" not in self.player["guess"]:
            messagebox.showinfo("Game Over", "***** YOU WIN! *****")
            self.master.destroy()
        elif "YOU LOST" in result:
            messagebox.showinfo("Game Over", result)
            self.master.destroy()
        else:
            self.update_display()

    def update_display(self):
        self.letter_entry.delete(0, tk.END)
        self.guess_label.config(text=self.player["guess"])
        # Add the question label to the display
        self.question_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    level_button = tk.Button(root, text="Select Level", command=lambda: open_level_selection(root))
    level_button.pack()
    root.mainloop()
