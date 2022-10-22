import random
import os
import string

# Funtion to clear the terminal
def clear():
    os.system('cls')
 
# Functuion to print the hangman
def print_hangman(values):
    print()
    print("\t +--------+")
    print("\t |       | |")
    print("\t {}       | |".format(values[0]))
    print("\t{}{}{}      | |".format(values[1], values[2], values[3]))
    print("\t {}       | |".format(values[4]))
    print("\t{} {}      | |".format(values[5],values[6]))
    print("\t         | |")
    print("  _______________|_|___")
    print("  `````````````````````")
    print()
 
# Function to print the hangman after winning
def print_hangman_win():
    print()
    print("\t +--------+")
    print("\t         | |")
 
    print("\t         | |")
    print("\t O       | |")
    print("\t/|\\      | |")
    print("\t |       | |")
    print("  ______/_\\______|_|___")
    print("  `````````````````````")
    print()
 
# Function to print the word to be guessed
def print_word(values):
    print()
    print("\t", end="")
    for x in values:
        print(x, end="")
    print() 
 
# Function to check for win
def check_win(values):
    for char in values:
        if char == '_':
            return False
    return True    
 
def rand_word(): 
    f = open("dictionary.txt", "r")
    data = f.read().split('\n')
    f.close()
    return [word.upper() for word in data]

# Function for each hangman game
def hangman_game(word_list = rand_word(), alphabet = list(string.ascii_uppercase)):
    chosen_word = word_list[random.randint(0, len(word_list))].upper()
    clear()
 
    # Stores the letters to be displayed
    word_display = []
 
    # Stores the correct letters in the word
    correct_letters = []
 
    # Stores the incorrect guesses made by the player
    incorrect = []
 
    # Number of chances (incorrect guesses)
    chances = 0
 
    # Stores the hangman's body values
    hangman_values = ['O','/','|','\\','|','/','\\']
 
    # Stores the hangman's body values to be shown to the player
    show_hangman_values = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
 
    # Loop for creating the display word
    for char in chosen_word:
        if char.isalpha():
            word_display.append('_')
            correct_letters.append(char.upper())
        else:
            word_display.append(char)
    word_dis_len = len(word_display)
    for word in word_list:
        if len(word) != word_dis_len:
            word_list.remove(word)
    # Game Loop         
    while True:
        for w, letter in zip(word, word_display):
            if letter != '_' and w != letter:
                word_list.remove(word)
                break
        for letter in incorrect:
            if letter in alphabet:
                alphabet.remove(letter)
            for word in word_list:
                if letter in word:
                    word_list.remove(word)
                    break
        for letter in alphabet:
            if letter in word_display:
                alphabet.remove(letter)
        count = {letter:0 for letter in alphabet}
        for letter in alphabet:
            for word in word_list:
                if letter in word:
                    count[letter] += 1
        for letter in alphabet:
            if count[letter] == 0:
                alphabet.remove(letter)
                del count[letter]
        total = sum(count.values())
        prob = {letter: count[letter] / total for letter in alphabet}
        prob = dict(sorted(prob.items(), key=lambda item: item[1], reverse=True))
        print(list(prob.items())[:5])
        print(len(alphabet))
        print(alphabet)
        print(len(word_list))
        print(random.choices(word_list, k = 5))
        # Printing necessary values
        print_hangman(show_hangman_values)
        print_word(word_display)            
        print()
        print("Incorrect characters : ", incorrect)
        print()
 
 
        # Accepting player input
        inp = input("Enter a character = ")
        if len(inp) != 1:
            clear()
            print("Wrong choice!! Try Again")
            continue
 
        # Checking whether it is a alphabet
        if not inp[0].isalpha():
            clear()
            print("Wrong choice!! Try Again")
            continue
 
        # Checking if it already tried before   
        if inp.upper() in incorrect:
            clear()
            print("Already tried!!")
            continue   
 
        # Incorrect character input 
        if inp.upper() not in correct_letters:
             
            # Adding in the incorrect list
            incorrect.append(inp.upper())
             
            # Updating the hangman display
            show_hangman_values[chances] = hangman_values[chances]
            chances = chances + 1
             
            # Checking if the player lost
            if chances == len(hangman_values):
                print()
                clear()
                print("\tGAME OVER!!!")
                print_hangman(hangman_values)
                print("The word is :", chosen_word)
                break
 
        # Correct character input
        else:
 
            # Updating the word display
            for i in range(len(chosen_word)):
                if chosen_word[i] == inp.upper():
                    word_display[i] = inp.upper()
 
            # Checking if the player won        
            if check_win(word_display):
                clear()
                print("\tCongratulations! ")
                print_hangman_win()
                print("The word is :", chosen_word)
                break
        clear() 

if __name__ == "__main__":
 
    clear()

    # The GAME LOOP
    while True:
 
        # Printing the game menu
        print()
        print("-----------------------------------------")
        print("\t\tGAME MENU")
        print("-----------------------------------------")
        print("Press", 0, "to play")    
        print("Press", 1, "to quit")
         
        # Handling the player category choice
        try:
            choice = int(input("Enter your choice = "))
        except ValueError:
            clear()
            print("Wrong choice!!! Try again")
            continue
  
        # The EXIT choice   
        if choice == 1:
            print()
            print("Thank you for playing!")
            break
 
        # The overall game function
        hangman_game()
