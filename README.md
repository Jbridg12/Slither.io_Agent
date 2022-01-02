# Slither Agent
The Slither Agent is a bot that allows for the automation or supervision of playing the game at http://slither.io. The agent
has two modes for playing the game: autonomous mode is where the agent decides and acts by itself, using the mouse to move the 
snake in the direction the decisionmaker engine decides; suggestion mode is where the agent get the recommended direction from
the engine and suggests a direction to the user via voice commands e.g. "Please head Northwest".


# Dependencies
This implementation of the slither agent requires a few external dependencies not listed in the writeup in order to run:
	pttsx3 // Python text to speech controller
	numpy

Additionally the Chromedriver provided is not necessarily the proper chromedriver for the user's system.
Navigate to the chromium website in order to discover and download the proper drivers for your system:
	
	https://sites.google.com/a/chromium.org/chromedriver/

# How do I use the Slither Agent?
The submitted file comes with the specified main.py python file. This allows for the user to run the file using:
	
	python main.py 

This command starts the slither agent in the autonomous mode and runs it for 15 games for default. If the user wants to change
these values they must change set both via the command line or neither. For example:
	
	python main.py autonomous 100
	
is a valid specification but 

	python main.py autonomous 
	
is not a valid command. The format is always 

	python main.py mode number_of_games

This allows for the user to specify the use case of the agent or just use the default mode and number of games if desired.

# Submission Info
- Joshua Bridges
- jbridg12
- 04/27/2021
