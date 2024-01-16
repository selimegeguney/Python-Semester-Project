answer = "ANSWER"
guess = "_ " * len(answer)
print(guess, f"({len(answer)})")
lives = 5
wrong_chars = []

def check_letter(answer):
    contained = False
    global guess, lives

    
    while True:
        letter = str(input("Guess a letter: ")).upper()
        if len(letter) == 1:
            break
        else:
            print("----- Please enter a single letter! -----")
        
    for i in range(len(answer)):
        if answer[i] == letter:
            guess = guess[:i*2] + letter + guess[i*2+1:]
            contained = True
    if contained == False:

        lives -= 1
        print("You have " + str(lives) + " lives left.")
        if lives == 0:
            print("***** You Lost! *****")
            print("The word was " + answer)
            exit()
    print(guess)

while lives > 0:
    if guess.replace(" ", "") != answer:
        check_letter(answer)
    else:
        print("***** You Win! *****")
        exit()