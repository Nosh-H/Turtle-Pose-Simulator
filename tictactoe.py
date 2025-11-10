from turtle import *
import time
def drawECKS(x, y):
  grid.penup()
  grid.goto(50*x-55, -50*y+35)
  grid.pendown()
  grid.write("X", font=("Arial", 16, "normal"))

def drawOH(x, y):
  grid.penup()
  grid.goto(50*x-55, -50*y +35)
  grid.pendown()
  grid.write("O", font=("Arial", 16, "normal"))

grid=Turtle()
grid.speed(0)
grid.penup()
grid.goto(25,-75)
grid.pendown()
for square in range (3):
  for _side in range (4):
    grid.forward(50)
    grid.left(90)
  if square < 2:
    grid.backward(50)
grid.forward(100)
grid.left(90)
grid.forward(50)
grid.right(90)
for square in range (3):
  for _side in range (4):
    grid.forward(50)
    grid.left(90)
  if square < 2:
    grid.backward(50)
grid.forward(100)
grid.left(90)
grid.forward(50)
grid.right(90)
for square in range (3):
  for _side in range (4):
    grid.forward(50)
    grid.left(90)
  if square < 2:
    grid.backward(50)

grid=Turtle()
grid.speed(0)

# Keeps track of which squares have x's or o's
takenArray = [[0,0,0],[0,0,0],[0,0,0]]

# Keeps track os which player's turn it is
turn = 1

# Prompts user for a value that is 0, 1, 2 and handles invalid inputs
def promptUser():
  while True:
    try:
      x_val = int(input("Enter X coordinate, where left is 0, middle is 1, and right is 2: "))
      y_val = int(input("Enter Y coordinate, where top is 0, middle is 1, and bottom is 2: "))
      if x_val in [0, 1, 2] and y_val in [0, 1, 2]:
        return x_val, y_val
      else:
        print("Please enter values of 0, 1, or 2 for both coordinates.")
    except ValueError:
      print("Invalid input. Please enter integer values of 0, 1, or 2, for both coordinates.")

# Prompts user to make their move
def move():
  # Initially prompt user
  x_val, y_val = promptUser()
    # Check if the input is not already taken
  while (takenArray[x_val][y_val] != 0):
    print("This square is already taken. Please choose another square.")
    x_val, y_val = promptUser()
  return (x_val, y_val)

# Check if the game is won
def gameIsWon(takenArray):
  # Check for each player
  for i in range(1, 3):
    # Check rows
    for row in takenArray:
      if row == [i, i, i]:
        print("Player " + str(i) + " wins!")
        return True
     #Check columns
    for col in range(3):
      if (takenArray[0][col] == i and takenArray[1][col] == i and takenArray[2][col] == i):
        print("Player " + str(i) + " wins!")
        return True
      # Check diagonals
      if (takenArray[0][0] == i and takenArray[1][1] == i and takenArray[2][2] == i) or (takenArray[0][2] == i and takenArray[1][1] == i and takenArray[2][0] == i):
        print("Player " + str(i) + " wins!")
        return True
  return False

# Main loop
for i in range(9):
  # Prompt the player for their move
  if (turn % 2 == 1):
    print("Player 1, your move:")
  else:
    print("Player 2, your move: ")
    
  (x, y) = move()
    # Update the taken array
  # Draw the player's move
  if (turn % 2 == 1):
    # It is player 1's turn (X)
    takenArray[x][y] = 1
    drawECKS(x, y)
  else:
    # It is player 2's turn (O)
    takenArray[x][y] = 2
    drawOH(x, y)
  # Now that both players have moved, check if the game is done
  if (gameIsWon(takenArray)):
    break
  elif (turn == 9):
    print("It's a draw!")
    break
  # Increment the turn counter
  turn += 1
