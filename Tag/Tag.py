#Tag application is run
#Tag screen opens
#AI and player are set as dots on grid screen
#AI and player begin on opposite sides of screen
#Timer is displayed at top of screen
#Start signal shows up and timer begins to count down (start button)
#AI has objective of maintaining distance from player within screen space before time runs out
#AI moves around screen by shifting in direction that increases variable distance from player
#AI moves one grid block every second
#Player has objective of tagging AI within screen space before time runs out
#Player can move around screen using arrow keys or wasd
#Player moves one grid block every second
#If player tags AI before time runs out screen flashes
    #Screen then reads victory and returns player to Candyland
#If player fails to tag AI before time runs out screen flashes
    #Screen then reads failure and returns player to Candyland

# Default player and computer starting locations
playerLocation = [0, 0]
computerLocation = [600, 600]

# Parameters for the size of the players
diameter = 10

# Max time that the game should run without the player getting caught. 
maxTime = 30

# All directions that the player and computer can move in + what value those directions map to.
directions = {
    1: [0, -1] #north
    2: [.5, -.5] #northeast
    3: [1, 0] #east
    4: [.5, .5] #southeast
    5: [0, 1] #south
    6: [-.5, .5] #southwest
    7: [-1, 0] #west
    8: [-.5, -.5] #northwest
}

#Tracking of player location by computer

""" Returns direction that computer should move in 
based on the location of the computer and player. """
def computerDirection():
    #Get difference in x and y values of the two players
    xDif = playerLocation[0] - computerLocation[0]
    yDif = playerLocation[1] - computerLocation[1]

    #Determine direction of player
    xDif = getDirection(xDif)
    yDif = getDirection(yDif)

    #Returns direction values based on xDif and yDif
    if (abs(xDif) == abs(yDif)):
        return [xDif * 1/2, yDif * 1/2]
    else:
        return [xDif, yDif]

""" Returns directional movement instructions based 
on difference values. """
def getDirection(difference):
    if (difference > 0):
        return 1
    else if (difference == 0):
        return 0
    else:
        return -1

""" Returns true if the game is supposed to be over and
returns false if the game is supposed to keep running."""
def checkGameEnd(time):
    

""" Returns true if player won and returns false is computer won. """
def getWinner(time):
    return time == maxTime