def main():
    widthSet = False
    heightSet = False
    
    while not widthSet:
    #takes input for width of the board
        try:
            width = int(input("Enter the width of your game board (4-10):"))
            if width >= 4 and width <= 10:
                #width must be between 4 and 10 inclusive.
                widthSet = True
            else:
                print("The width must be an integer from 4-10. Please try again.")
        except:
            print("The width must be an integer from 4-10. Please try again.")
        
    while not heightSet:
    #takes input for height of the board
        try:
            height = int(input("Enter the height of your game board (4-10):"))
            if height >= 4 and height <= 10:
                #height must be between 4 and 10 inclusive
                heightSet = True
            else:
                print("The height must be an integer from 4-10. Please try again.")
        except:
            print("The height must be an integer from 4-10. Please try again.")
        
    board = Board(width, height)
    #calls the board class to create an object
    board.display()
    #calls a method within the object to display the board
    allPlayersAdded = False
    players = []
    #list of all player objects
    
    while not allPlayersAdded:
        validName = False
        while not validName:
            name = input("Enter this player's name:")
            validName = True
            for player in players:
                if player.getName() == name:
                    validName = False
                    print("There is already a player called " + name + ". Please try again.")
                #loops through every player to see if the username has already been used
            if name == "Nobody":
                validName = False
                print("You cannot use the name \"Nobody\". Please try again.")
                #Nobody cannot be used as a username as it is used as a condition on line 85
        newPlayer = Player(name, len(players) + 1)
        #Makes a player object
        players.append(newPlayer)
        #adds the object to the list of player objects
        print("Player " + str(newPlayer.getNumber()) + " is: " + name)
        #Prints the player number and their name for the users
        if len(players) > 1 and len(players) < 4:
            #only allows between 2 and 4 players (inclusive)
            valid = False
            while valid == False:
                addMore = input("Keep adding players (y/n)")
                if addMore.lower() == "y" or addMore.lower() == "yes":
                    allPlayersAdded = False
                    valid = True
                elif addMore.lower() == "n" or addMore.lower() == "no":
                    allPlayersAdded = True
                    valid = True
                #option to add more players
                else:
                    print("Wrong input") 
        elif len(players) == 4:
            allPlayersAdded = True
    
    print()            
    print("This game has " + str(len(players)) + " players:")
    #prints the amount of players
    for player in players:
        print(player.getName())
        #prints the players' name
        
    gameOver = False
    winner = "Nobody"
	
    while not gameOver: 
        for player in players:
            print()
            print(player.getName() + ", it's your turn:")
            board.display()
            #displays the board by calling the display method on the board object
            player.makeMove(board)
            #calls the method within the player object to make a move
            winner = player.checkWinner(board) 
            #method within the player object to check if the player has won
            if winner != "Nobody" or board.boardFull():
                #if there is no winner or the board is full the game ends
                gameOver = True
                break
    
    board.display()
    print(winner + " wins the game!")
    #Outputs the winner's username and the board
    
class Board:
    def __init__(self,width,height):
        self.__columns = width
        self.__rows= height
        self.__board = [[""]*self.__columns for a in range (self.__rows)]
        #creates an empty board of the specified width and height
    
    def display(self):
        new_line = '\n'
        for y in range(self.__columns+1):
            new_line += ' - +'
        for x in range(0,self.__columns):
            if x < 1:
                print('0'.rjust(6,' '),end='')
            else:
                print(f'{x:>4}',end='')
        for i in range(0,self.__rows):
            print(new_line)
            print(" "+str(i)+" |",end = "")
            for x in range(0,self.__columns):
                print(f'{self.__board[i][x]:^3}' + '|',end = "")
        #formats the display of the board
        print(new_line)
        print()
    
    def get_width(self):
        #returns the width of the board
        return self.__columns
            
    def boardFull(self):
        tokens = ['1','2','3','4']
        full = False
        for x in range(self.__columns-1,-1,-1):
            for y in range(self.__rows-1,-1,-1):
                if self.__board[y][x] in tokens:
                    full = True
                else:
                    full = False
        #loops through the board (starting from the last column and the last row) to see if the board is full if there is any empty spaces, full becomes false
        return full        
        
    def columnFull(self,column):
        tokens = ['1','2','3','4']
        column_full = False
        for y in range(self.__rows-1,-1,-1):
            if self.__board[y][column] in tokens:
                column_full = True
            else:
                column_full = False
        return column_full
        #loops up the column to see if there are any empty spaces within the column
    
    def addToken(self,token, tokens):
        valid = False
        pointer = 0
        while not valid:
            x = int(input("Where would you like to drop the piece (x):"))
            if x > self.__columns-1:
                print("Invalid move - the board has a width of:",self.__columns)
            #checks if the x-coordinate is within the board
            elif self.columnFull(x) == True:
                print("Column",x,"is full")
                valid = False
            #checks for if the column is full
            else:
                for i in range(0,self.__rows):
                    #loops through the rows
                    if self.__board[i][x] in tokens:
                        pointer = i-1
                        break
                    #if the column has a token the pointer goes up 1 row
                    else:
                        pointer = None
                if pointer == None:
                    self.__board[self.__rows-1][x] = token
                    #if there are no tokens in the column then the token is placed on the last row of that column
                else:
                    self.__board[pointer][x] = token
                    #Otherwise the token is placed on the row above the token below it
                valid = True
    
    def checkWinner(self,token):
        if (self.checkVertical(token) == True or self.checkHorizontal(token) == True) or (self.checkRightDiagonal(token) == True or self.checkLeftDiagonal(token) == True):
            return True
        #calls methods to check if there are 4 tokens of the player's type in a row (vertically,horizontally and diagonally - both left and right)
        
    def checkVertical(self,token):
        won = False
        counter = 0
        for x in range(0,self.__columns):
            #loops through each column
            for y in range(0,self.__rows):
                #loops through each row
                if self.__board[y][x] == token:
                    counter+= 1
                    #if there is a token of the player's type the counter starts
                elif counter == 4:
                    won = True
                    #once the counter reaches 4 in a row won is true
                else:
                    counter = 0
                    #if there is a gap or space between tokens, the counter returns to 0
        return won
    
    def checkHorizontal(self,token):
        won = False
        counter = 0
        for y in range(0,self.__rows):
            #loops through each row
            for x in range(0,self.__columns):
                #loops through each column
                if self.__board[y][x] == token:
                    counter +=1
                    #if there is a token of the player's type in the column, 1 is added to the counter
                elif counter == 4:
                    won = True
                    #if there are 4 tokens in a row the counter will have a value of 4 and won will be true
                else:
                    counter = 0
                    #otherwise if there is a gap or space, the counter returns to 0
        return won
                    
    def checkRightDiagonal(self,token):
        won = False
        for y in range(0,self.__rows):
            #loops through each row
            for x in range(0,self.__columns):
                #loops through each column
                if self.__board[y][x] == token:
                    #if it reaches the player's token, it tries to check if the row below it has a token 1 to the left and then if the row below that has a token 2 to the left etc etc.
                    try:
                        if (self.__board[y+1][x-1] == token and self.__board[y+2][x-2] ==token) and self.__board [y+3][x-3] == token:
                            won = True
                            return won
                    #if it doesn't find that the tokens meet the condition or that the indexes fall outside the board, won is returned as false
                    except:
                        won = False
        return won
    
    def checkLeftDiagonal(self,token): 
        won = False
        for y in range(0,self.__rows):
            #loops through each row
            for x in range(0,self.__columns):
                #loops through each column
                if self.__board[y][x] == token:
                    #if it reaches the player's token, it tries to check if the row below it has a token 1 to the right and then if the row below that has a token 2 to the right etc etc.
                    try:
                        if (self.__board[y+1][x+1] == token and self.__board[y+2][x+2] ==token) and self.__board [y+3][x+3] == token:
                            won = True
                            return won
                    #if it doesn't find that the tokens meet the condition or that the indexes fall outside the board, won is returned as false
                    except:
                        won = False
        return won
        
class Player:
    def __init__(self,player_name,player_number):
        self.__tokens = ['1','2','3','4']
        self.__playerName = player_name
        self.__playerNumber = player_number
        self.__token = self.__tokens[player_number-1] #assigns a token from the list of tokens to the player object depending on their number.
    
    def getNumber(self):
        return self.__playerNumber
    #returns the player's number
    
    def getName(self):
        return self.__playerName
    #returns the player's name
    
    def makeMove(self,board):
        board.addToken(self.__token,self.__tokens)
    #calls the addToken method in the board so that the player's token can be added to the board object.
    
    def checkWinner(self,board):
        if board.checkWinner(self.__token) == True:
            return self.__playerName
        #calls the checkWInner method on the board so that the board can check if the player object has won
        else:
            return "Nobody"
        #returns Nobody if there is no winner
    
       
        
            

            
    
if __name__ == '__main__':
    main()
#Starts the program