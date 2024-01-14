answer = "WORD"
guess = "_ " * len(answer)
print(guess)
lives = 5

def check_letter(answer, lives):
    contained = False
    global guess

    letter = str(input("Guess a letter: ")).upper()
    for i in range(len(answer)):
        if answer[i] == letter:
            guess = guess[:i*2] + letter + guess[i*2+1:]
            contained = True
    if contained == False:
        lives -= 1
        print("You have " + str(lives) + " lives left.")
        if lives == 0:
            print("You lose!")
            print("The word was " + answer)
            exit()
    print(guess)

while lives > 0:
    if guess.replace(" ", "") != answer:
        check_letter(answer, lives)
    else:
        print("You win!")
        exit()