import os
from dotenv import load_dotenv
from openai import OpenAI
import tkinter as tk
from tkinter import messagebox

load_dotenv() #LOADS .env FILE
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") #GETS API KEY FROM .env FILE
client = OpenAI(api_key=f"{OPENAI_API_KEY}") #CONNECTS TO OPENAI API

def get_completion(prompt, model = "gpt-3.5-turbo"): #GETS COMPLETION FROM OPENAI API
    messages = [{"role": "user", "content":prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=1)
    return response.choices[0].message.content

level = str(input("Choose a level (A1, A2, B1, B2, C1, C2): ")).upper() #GETS LEVEL INPUT FROM USER
while level not in ["A1", "A2", "B1", "B2", "C1", "C2"]: #CHECKS IF LEVEL IS VALID
    level = str(input("Please enter a valid level (A1, A2, B1, B2, C1, C2): ")).upper()
answer = get_completion(f"Give me a {level} Level word just write the word.").upper() #GETS ANSWER FROM OPENAI API
question = get_completion(f"Define word '{answer}' but definitely don't use the word itself while defining and prompting. Keep it simple and short. Start defining directly not with 'This word' ") #GETS QUESTION FROM OPENAI API

# answer = "ANSWER" #UNCOMMENT HERE TO PLAY WITHOUT GPT API AND COMMENT GET COMPLETION FUNCTION AND ANSWER, QUESTION VARIABLES
# question = "QUESTION"

player = {"lives": 5, "correct_chars": [], "wrong_chars": [], "guess": "_ " * len(answer)} #PLAYER DICTIONARY

def guess_letter(answer):
    contained = False
    global player

    while True: #TAKES LETTER INPUT THAT IS ONE CHARACTER AND HAS NOT BEEN GUESSED BEFORE
        letter = str(input("Guess a letter: ")).upper()
        if len(letter) == 1:
            if letter in player:
                return(f"----- You have already found letter {letter}! -----")
                
            elif letter in player['wrong_chars']:
                return(f"----- You already guessed letter {letter}! -----")
            break
        else:
            return("----- Please enter a single letter! -----")
        
    for i in range(len(answer)): #CHECKS IF LETTER IS IN THE ANSWER AND ADDS IT TO GUESS
        if answer[i] == letter:
            contained = True
            player["guess"] = player["guess"][:i*2] + letter + player["guess"][i*2+1:]
            if letter not in player['correct_chars']: player['correct_chars'].append(letter)

    if contained: #CORRECT GUESS RETURN
        return(f"***** CORRECT! *****\n {player['guess']}  FAILS: {', '.join(player['wrong_chars'])}")
    else: #WRONG GUESS
        player['wrong_chars'].append(letter) 
        player["lives"] -= 1
        if player["lives"] > 0: #CHECKS IF PLAYER HAS LIVES LEFT
            return(f"----- WRONG! {player['lives']} LIVES LEFT! -----\n {player['guess']}  FAILS: {', '.join(player['wrong_chars'])}")
        elif player["lives"] == 0:
            return(f"***** YOU LOST! *****\n The word was => {answer}")
    return    

print("\n\n", player["guess"], f"({len(answer)})\n") #GAME STARTS HERE

while player["lives"] > 0: #INFINITE LOOP FOR GUESS FUNCTION UNTIL PLAYER WINS OR LOSES
    if player["guess"].replace(" ", "") != answer:
        print(question)
        print(guess_letter(answer), "\n\n--------------------------------------------------------------------------------------\n") 
    else:
        print("***** YOU WIN! *****")
        break
        



