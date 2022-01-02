#   file:           agent.py
#   author:         Josh Bridges
#   description:
#       This file implements the agent for controlling the slither.io game
#       this class utilizes the window manager class and pynput in order to
#       control the slither.io game. If the mode is set to 'suggestion' then
#       it uses pyttsx3 to convert text to speech and talk to the human operators
#
#   usage:
#       this class can be used as follows:
#           var = agent.SlitherAgent([mode], [#_of_games]) // inputs are optional and default to autonomous and 15 games
#           var.start() //Starts the slither.io game 

import decisionmaker as dm
import wm
import time
import pyttsx3
import datetime 
from pynput.mouse import Button, Controller

#Alias the mouse controller so that we can import the keyboard controller
MC = Controller

from pynput.keyboard import Key, Controller

class SlitherAgent():
    #Contructor with default mode and number of games set 
    def __init__(self, mode='autonomous', games=15):
        self.mode = mode
        self.games = games
        #Create a decisionmaker instance set to the center of screen based on game_screen variable size
        self.DM = dm.DecisionMaker((300, 230))
        #Create instance for mouse, keyboard, and TTS controllers
        self.mouse = MC()
        self.keys = Controller()
        self.speaker = pyttsx3.init()
    
    #Main Program loop 
    def start(self):
        #Create and open browser window manager
        self.WM = wm.WindowManager()
        
        #Play for x many games 
        for i in range(self.games):
            
            #Write name to text field
            self.enter_name()
            #Press the play button or play again button
            self.press_play()
            #Set mouse to the snake's position on the screen
            self.mouse.position = (300, 350)
            #Sleep so that screenshot doesn't capture the play screen twice
            time.sleep(10)
            
            #Loop while alive and playing
            while True:
                
                #Take a screenshot of where the dead state text would be
                image = self.WM.takeScreenshot(200, 75, 200, 280)
                #Take a screenshot of the entire game screen
                game_screen = self.WM.takeScreenshot(600, 460, 0, 130)
                #Extract the final size text from dead screen
                text = self.WM.extractText(image)
                
                #While alive text is only one character, so state can be determined by checking size of text string
                if len(text) > 1:
                    #When dead create log file and return to outer for loop
                    self.log_game()
                    break
                    
                #In autonomous mode
                if self.mode == 'autonomous':
                    #Generate direction recommendation from the recommender 
                    dir = self.DM.generate_decision(game_screen)
                    
                    #Change the mouse position based on the direction recommendation
                    if dir == 'NE':
                        self.mouse.position = (320, 330)
                    elif dir == 'N':
                        self.mouse.position = (300, 330)
                    elif dir == 'NW':
                        self.mouse.position = (280, 330)
                    elif dir == 'W':
                        self.mouse.position = (280, 350)
                    elif dir == 'E':
                        self.mouse.position = (320, 350)
                    elif dir == 'S':    
                        self.mouse.position = (300, 370)
                    elif dir == 'SW':
                        self.mouse.position = (280, 370)
                    else:
                        self.mouse.position = (320, 370)
                    
                    #Do this every two seconds    
                    time.sleep(2)
                    
                #In suggestion mode
                elif self.mode == 'suggestion':
                    #Generate direction recommendation from the recommender
                    dir = self.DM.generate_decision(game_screen)
                    
                    #Create audio indication to user of recommeded direction
                    if dir == 'NE':
                        self.speaker.say("Please Head NorthEast")
                    elif dir == 'N':
                        self.speaker.say("Please Head North")
                    elif dir == 'NW':
                        self.speaker.say("Please Head NorthWest")
                    elif dir == 'W':
                        self.speaker.say("Please Head West")
                    elif dir == 'E':
                        self.speaker.say("Please Head East")
                    elif dir == 'S':    
                        self.speaker.say("Please Head South")
                    elif dir == 'SW':
                        self.speaker.say("Please Head SouthWest")
                    else:
                        self.speaker.say("Please Head SouthEast")
                        
                    #Play the audio to the user
                    self.speaker.runAndWait()
                    
                    #Once every two seconds
                    time.sleep(2)
                    
                #Invalid mode state
                else:
                    print("Invalid game mode.")
                    exit()
        
    
    #Function to modulate pressing the play button
    def press_play(self):
        #Go to play button on screen 
        self.mouse.position = (275, 460)
        #Click it 
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
    
    #Function to modulate typing in the player name: 'NAME'
    def enter_name(self):
        #Click on name field
        self.mouse.position = (250, 420)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        
        #Type in name
        self.keys.press('N')
        self.keys.release('N')
        self.keys.press('A')
        self.keys.release('A')
        self.keys.press('M')
        self.keys.release('M')
        self.keys.press('E')
        self.keys.release('E')
    
    #Creates file using the datetime of when the game ended
    def log_game(self):
        time = datetime.datetime.now()
        filename = str(time.month) + "-" + str(time.day) + "-" + str(time.year) + "-" + str(time.hour) + "." + str(time.minute) + "." + str(time.second) + "-run.csv"
        f = open(filename, "w")
        f.close()