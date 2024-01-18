answer = "SNAKE"
guess = "_ " * len(answer)
print(guess, f"({len(answer)})")
lives = 5
correct_chars = []
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
            if letter not in correct_chars: correct_chars.append(letter)

    if contained:
        return(f"***** CORRECT! *****\n {guess}")
    else:
        lives -= 1
        if lives > 0:
            if letter not in wrong_chars: 
                wrong_chars.append(letter)
            return(f"----- WRONG! {lives} LIVES LEFT! -----\n {guess}")
        elif lives == 0:
            return(f"***** You Lost! *****\n\n The word was => {answer}\n")
        
            
            # return(f"----- Wrong Guess {lives} lives left! -----\n {guess} ({len(answer)} letters)")

        # print("You have " + str(lives) + " lives. Wrong Attempts: " + str(wrong_chars))
        

while lives > 0:
    if guess.replace(" ", "") != answer:
        print(guess_letter(answer), "FAILS: ", ', '.join(wrong_chars))  
    else:
        print("***** You Win! *****")
        break
        
