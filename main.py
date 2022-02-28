import tictactoe
import AI

#########################################################
# when creating a game, you can pass AI as an argument,
# which will control the actions of the second player.
# If you do not pass arguments, then the second player will be controlled by human.
#########################################################

# player2 = AI.SimplePlayer() # it does random turns
player2 = AI.SmartPLayer() # it uses minmax algorythm to evaluate next turns
game = tictactoe.Game.inst(player2)


if __name__ == '__main__':
    game.play()

