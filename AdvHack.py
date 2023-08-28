import sys
import re
import random
import logging
logging.basicConfig(filename='myProgramLog.txt', level=logging.CRITICAL, format='%(asctime)s -  %(levelname)s -  %(message)s')

try:
    import AdvHackAdjacent
    logging.debug("AdvHackAdjacent Opened Successfully")
except:
    logging.critical("AdvHackAdjacent.py does not exist, EXITING PROGRAM...")
    sys.exit()
#DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION DESCRIPTION
"""
This is a simple copy of the Fallout series' hacking terminals, in which users are given a retro-looking sequence of random characters and are
tasked with finding the password from among them. It does not implement cheats, as the game does, but it will in the future. The player is given
5 attempts, each attemps will reduce the attempts remaining by one. The attempts left are denoted with []. If the user succeeds, the programs displays
a message and exits. If the user fails to guess the password in the alloted atempts, the password is revealed and then the program exits. This program also
implements a similarity system, which determines how similar to the correct password the Guess is.
If the user enters something that is not a word, they are penalized one Attempt.
If the user enters the decorative Hex codes to the side, they are not penalized.
If the user enters HELP, the description prints again, and the user is not penalized.
"""

#Class for stats
class Stats:
    def __init__(self, totalAttempts, accuracy, correctGuesses):
        self.totalAttempts = totalAttempts
        self.accuracy = accuracy
        self.correctGuesses = correctGuesses
    totalAttempts = 0.0
    accuracy = 0.0
    correctGuesses = 0.0;
    def getAccuracy(self):
        if(self.totalAttempts == 0):
            self.accuracy = 100.0
            return
        else:
            self.accuracy = self.correctGuesses/self.totalAttempts
    def printStats(self):
        self.getAccuracy()
        print("--STATS-----------------------------------------")
        print("Total Number of Attempts:" + str(int((self.totalAttempts))))
        print("Accuracy: " + str(self.accuracy * 100) + '%')
        print("Total number of correct guesses: " + str(int(self.correctGuesses)))
        print("------------------------------------------------")
    

try:
    logging.debug("Loading WordBank...")
    WordLibraries = AdvHackAdjacent.Word_Libraries
    logging.debug("Loading SymbolBank...")
    SymbolBank = AdvHackAdjacent.SymbolBank
    logging.info("Loading FillerSymbols...")
    FillerSymbols = []
    logging.info("Loading CheatLibraries..")
    CheatLibraries = []
    Guessing_Territory = ""
    Passcode = ""
    CheatLine = ''
    attempts = 4
    guess = ""
    logging.info("Loading Stats Object: data...")
    data = Stats(0, 0.0, 0)
    
except:
    logging.critical("Missing Critical Files! EXITING PROGRAM...")
    sys.exit()

try:
    logging.info(f"WordLibraries[0][0]: {WordLibraries[0][0]}. Loaded Succesfully!")
except:
    logging.critical("Word Libraries not found... EXITING PROGRAM...")
    sys.exit()

    
#FROM the above word libraries, Choose the passcode
def PasswordSelect(WordLibraries):
    logging.info("Choosing wordBank and Passcode...")
    WordBank = random.choice(WordLibraries)
    Passcode = random.choice(WordBank)
    logging.info(f"WordBank: {WordBank}\n\t\t\t\t\t\t\t\tPassword: {Passcode}")
    return WordBank, Passcode


          
def GenerateFiller(Symbols): #This will generate and then return a series of 192 * 2 (384) characters, consisting of {}[]<>/\%^&$#*()__=+? to act as the filler for the array
    FillerSymbols = []
    FillerString = ''
    for i in range(0, 384):
        FillerSymbols.append(random.choice(Symbols)); #Symbols is the generated Filler String that was created earlier
    for i in range(0, len(FillerSymbols)): # this loop takes fillerSymbols and makes it a string
        FillerString += FillerSymbols[i]
    return FillerString    
    


def ProcessInput(Input, WordBank, Password):
    Similarity = 0
    global attempts
    global totalAttempts
    HexGex = re.compile(r"(0x)\d*")
    if(Input == ""):
        print("In order to have a similarity, you do need to enter a word.")
        attempts += 1
        return
    if Input.upper() == Password:
        print("PASSWORD ACCEPTED")
        data.correctGuesses += 1
        return
    
    for item in WordBank:
        if Input.upper() == item: #If it is a valid word
            print("Incorrect Guess. Similarity =", end = '')
            #Determine the similarity to the password
            for i in range(0, len(Password)):
                if Input[i].upper() == Password[i]:
                    Similarity += 1
            print(" " + str(Similarity))
            return;
    if(HexGex.search(str(Input)) != None):
        print("Those Denote the line numbers, Please Enter a word in the bank, found to the right.")
        attempts += 1
        return
    print("That does not appear to be a word in the list")
    

#InterfaceForm returns a bank of strings and filler to display on the screeen

def InterfaceForm(filler, wordBank): #filler is a string that corresponds to 384 characters of filler, and wordbank is the words to mix in
    # break the long cheat string into 32 small strings. The Interface is layed out as such, with each number the index in interfaceText:
    newFiller = []
    validIndex = False
    logging.debug(f"{wordBank}")
    """This is the Interface: if will consist of a slightly randomized hex value that denotes the line, then the combination of the
       Filler string and potential passowrds that were generated earlier. each number is one of 32 lines of "Filler", and the Hex codes
       really dont matter, they just look neat

       HEX 0  HEX  16
       HEX 1  HEX  17
       HEX 2  HEX  18
       HEX 3  HEX  19
       HEX 4  HEX  20
       HEX 5  HEX  21
       HEX 6  HEX  22
       HEX 7  HEX  23
       HEX 8  HEX  24
       HEX 9  HEX  25
       HEX 10 HEX  26
       HEX 11 HEX  27
       HEX 12 HEX  28
       HEX 13 HEX  29
       HEX 14 HEX  30
       HEX 15 HEX  31
    """
   #turn filler from a string into a list, that way I can easily replace the values
    for letter in filler:
        newFiller.append(letter)
 
    #newFiller is now a list to add the words to:
    for word in wordBank:
        validIndex = False
        while(validIndex  == False):
            validIndex = True
            #Determine a random index in newFiller to add the word to
            addIndex = random.randint(0, len(newFiller)-8)
            #make sure that there isnt another word within 9 characters of that index, so the words are seperated
            for character in range(addIndex, addIndex +9):
                if(newFiller[character].isalpha()):
                    validIndex = False
                    continue
                if(addIndex > 185 and addIndex < 192):
                    validIndex = False
                    continue
            #if the program gets here, its found a valid landing spot to put the new word       
            #if not, iterate through newFiller from addIndex - addIndex+len(wordBank[i]) and add the words
        for index in range(addIndex, addIndex + len(word)):
            newFiller[index] = word[index - addIndex]
            #repeat the loop for every word in wordbank
    #echo the newFiller list
    global interfaceText
    interfaceText = []
    
    for num in range(0,32):
        interfaceText.append('')#each cell in this will correspond to a row in the final display
    for i in range(0, len(newFiller), 12):
        for letter in range(i, i+ 12):
            logging.debug("Letter: " + str(letter))
            interfaceText[int(i/12)] += interfaceText[int(i/12)].join(newFiller[letter]) # this needs to make interfaceText a [list] of 32 "strings"
        logging.debug("SUCCESS")
        logging.debug("Len(newFiller): " + str(len(newFiller)))
    return interfaceText
    

def printInterface(hexStart, FillText): #hex start is the fist hex number to print as flavortext on the side, and FillText is the List of lines for the console

    for i in range(16):
        print((hex((i + 1) * hexStart + 5000) + "  ").ljust(8),end='')
        print( FillText[i] + "  ", end='')
        print((hex((i+1) * hexStart + 5016) + "  ").ljust(8),end='')
        print(FillText[i + 16])

def displayTerminal():
    print( """WELCOME TO THE TERMINAL. BEFORE YOU IS A
SERIES OF SYMBOLS WITH WORDS MIXED IN.AMONG THOSE
WORDS IS THE PASSWORD, AND YOU WILL HAVE LIMITED
ATTEMPTS TO GUESS WHICH ONE IT IS.EACH INCORRECT
GUESS WILL GIVE YOU A SIMILARITY. THE NUMBER NEXT
TO THE SIMILARITY TELLS YOU HOW MANY LETTERS ARE
IN THE SAME PLACE BETWEEN THE WORDS YOU GUESSED
AND THE CORRECT PASSWORD. ALL WORDS ARE THE SAME
LENGTH. IF YOU WISH TO SEE THIS AGAIN, ENTER HELP
    """)
    

#EXECUTIONSECTION EXECUTIONSECTION EXECUTIONSECTION EXECUTIONSECTION EXECUTIONSECTION EXECUTIONSECTION EXECUTIONSECTION
def hack():
    WordBank = None
    Password = ""
    Guessing_Territory = []
    WordBank, Password = PasswordSelect(WordLibraries)
    WordBank = list(WordBank)
    Filler = GenerateFiller(SymbolBank)
    Guessing_Territory = InterfaceForm(Filler, WordBank)
    global attempts
    global totalAttempts
    try:
        displayTerminal()
    except:
        logging.debug("Terminal Display Error")
    print("-----------------------------------------------------")
    try:
        printInterface(random.randint(1000, 2500), Guessing_Territory)
    except:
        logging.critical("INTERFACE ERROR! EXITING PROGRAM...")
        sys.exit()
    print("-----------------------------------------------------")
    print("Attempts Remaining: " + "[]"*(attempts + 1))
    guess = input("Enter a Guess >>>")
    ProcessInput(guess, WordBank, Password)
    count = 1
    while(guess.upper()!= Password and attempts > 0):
        if(guess.upper() == "HELP"):
            displayTerminal()
        attempts = attempts - 1
        data.totalAttempts += 1
        if(count % 5 == 0):
            print("-----------------------------------------------------")
            printInterface(random.randint(1000, 2500), Guessing_Territory)
            print("-----------------------------------------------------")
        print("attempts Remaining: " + "[]"*(attempts + 1))
        guess = input("Enter a Guess >>>")
        ProcessInput(guess, WordBank, Password)
        if(guess == Password):
            data.totalAttempts += 1
            print("Thank you for your verification")
        if(guess != Password and attempts == 0):
            print("Number of attempts Exceeded")
            print("The Correct Password was " + Password)
            print("Exiting program...")
        count += 1
            
    return 

while(True):
    selection = 1

    print("--Menu---------------------------------")
    print("  1.)Attempt Hack.....................|")
    print("  2.)View Stats.......................|")
    print("  3.)Exit.............................|")
    print("-----------------------Enter a Number--")
    while(True):
        try:
            selection = int(input("Enter a Number>>"));
        except:
            print(selection)
            print("A number is required:")
            continue
        if(selection < 0 or selection > 3):
            print("Invalid Selection, try again...")
            continue
        if(selection == 1):
            print()
            print()
            attempts = 4
            hack()
            print()
            print()
            break
        if(selection == 2):
            print()
            print()
            data.printStats();
            print()
            print()
            break
        if(selection == 3):
            print("I hope you had fun!")
            sys.exit()
    
    
    
    







