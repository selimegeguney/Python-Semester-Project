import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=f"{OPENAI_API_KEY}")

def get_completion(prompt, model = "gpt-3.5-turbo"):
    messages = [{"role": "user", "content":prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content

answer = get_completion("Give me a B1 Level word which is dfferent from old ones just write the word. ").upper()

question = get_completion(f"Define word '{answer}' but don't use word itself while defining and prompting. Keep it simple and short. Start defining directly not with 'This word' ")




guess = "_ " * len(answer)
print(question,"\n", guess, f"({len(answer)})")
lives = 5
# correct_chars = []
wrong_chars = []

def guess_letter(answer):
    contained = False
    global guess, lives, correct_chars, wrong_chars

    
    while True:
        letter = str(input("Guess a letter: ")).upper()
        if len(letter) == 1:
            if letter in correct_chars:
                return(f"----- You have already found letter {letter}! -----")
                
            elif letter in wrong_chars:
                return(f"----- You already guessed letter {letter}! -----")
            break
        else:
            return("----- Please enter a single letter! -----")
        
    for i in range(len(answer)):
        if answer[i] == letter:
            contained = True
            guess = guess[:i*2] + letter + guess[i*2+1:]
            # if letter not in correct_chars: correct_chars.append(letter)

    if contained:
        return(f"***** CORRECT! *****\n {guess}")
    else:
        wrong_chars.append(letter) 
        lives -= 1
        if lives > 0:   
            return(f"----- WRONG! {lives} LIVES LEFT! -----\n {guess}")
        elif lives == 0:
            return(f"***** YOU LOST! *****\n\n The word was => {answer}\n")
    return    

while lives > 0:
    if guess.replace(" ", "") != answer:
        print(question, "\n", guess_letter(answer), "FAILS: ", ', '.join(wrong_chars))  
    else:
        print("***** YOU WIN! *****")
        break
        
