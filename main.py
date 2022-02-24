import tictactoe
import AI

#########################################################
# when creating a game, you can pass AI as an argument,
# which will control the actions of the second player.
# If you do not pass arguments, then the second player will be controlled by human.
#########################################################

# player2 = AI.SimplePlayer() # it does random turns
player2 = AI.SmartPLayer() # it uses minmax algorythm to make turns
game = tictactoe.Game.inst(player2)

# Class "Game" uses Singleton design pattern which is available through "inst()" method.
# Switch to True to enable singleton_check section
singleton_check = False
if singleton_check:
    game2 = tictactoe.Game.inst(player2)
    if id(game) == id(game2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")

game.play()
