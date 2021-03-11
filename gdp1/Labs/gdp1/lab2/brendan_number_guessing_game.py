import random

secret_number = random.randrange(1, 129)

guesses = []
guess = 0
stop = False
while guess != secret_number:
    guess = input("Guess a number 1 to 128: ")

    # Allow user to quit without finishing
    if guess.isalpha() and guess == "q":
        stop = True
        guess = secret_number
    else:
        # Test the guess
        guess = int(guess)
        if guess < secret_number:
            print("Too low.")
        elif guess > secret_number:
            print("Too high.")
        else:
            print("Correct!")

        guesses.append(guess)

        # Terminate game after 7 guesses
        if len(guesses) == 7 and guess != secret_number:
            guess = secret_number
            print("You are out of guesses.")

if not stop:
    print()
    print("Your guesses: ", end=" ")
    for i in range(len(guesses)):
        print(guesses[i], end=" ")
