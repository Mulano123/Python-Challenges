import random

number = random.randint(1, 50)

guess = 0
attempt = 0

name = str(input("Enter your Name : "))
print("")
print("Welcome to Guessing Game Number")
print("")
print("Guess a Number from 1 to 50")
print("")
print("Let's Begin")
print("")

while guess != number:

    guess = int(input("Enter a guess: "))

    if guess < number:
        print("Guess Higher")
        attempt = attempt + 1
    elif guess > number:
        print("Guess Lower")
        attempt = attempt + 1

print("")
print("Congratulations", name, ", You've Guess the Number!")
print("It took you", attempt, "attempts to guess")
