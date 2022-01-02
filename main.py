#   file:           main.py
#   author:         Josh Bridges
#   description:
#       this file utilizes the agent class to instantiate one based on the command line
#       arguments and run the game using the start() function call
#
#   usage:
#       run this file from the command line as  
#           python main.py mode #_of_games

import agent
import sys

#If the user passed command line arguments use those
if len(sys.argv) > 1:
    slither = agent.SlitherAgent(sys.argv[1], int(sys.argv[2]))
#Otherwise use default constructor
else:
    slither = agent.SlitherAgent()
    
#Start the game
slither.start()
