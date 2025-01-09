## Text Dungeon

A text-based (for now!) adventure game that draws heavy inspiration from D&D and Pathfinder that is still in development

## Usage

Once you run the game's start file, you can interact with it via the Terminal/Command Line. The game will print prompts and information to the Terminal, which you as the player can then react to by inputting specifc commands.Every prompt comes with a list of available actions, and their respective hotkeys/codes. These are not case sensitive. 

Typing "exit" at any menu will save the current game state and quit the game. Upon re-running the start file, your last saved game state will automatically be loaded. Please note, while *YOUR* state will save and reload, the rest of the game will be randomly generated anew. Any items in your inventory will remain, but the Shopkeep's inventory will reset. You will also have to re-enter the Dungeon again, which means if you quit in the middle of a fight or event, you will not be returned to the same situation.

Entering "n" at the game's first prompt ("Would you like to enter the Dungeon?") will take you to the Overworld immediately.

## Install

To run the game, you first need to have Python installed on your machine, or in whichever environment you'd like to play in
* [MacOS](https://docs.python-guide.org/starting/install3/osx/)
* [Windows](https://www.python.org/downloads/windows/)
* [Linux](https://docs.python-guide.org/starting/install3/linux/)

Once Python is installed, you need the dungeon_text main file. You can either:
* [Download the ZIP file](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)
* [Clone the repoistory](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

Next, you have a choice between playing from the *src* file or the *stable* file. 

The *src* file represents the most current, but also unstable version of the game. It is, for all intents and purposes, a testing environment. There will likely be game breaking bugs, and it's not really designed to be playable, but just as a mechanism to add and test new features until they are ready for stable.

The *stable* file is the (hopefully) playable version of the project. It doesn't include as many features as the *src* file, but the game should be fully functional. 

Either way, to start the game, run this command from the dungeon_text directory:
* python3 *filename*/tui.py

where *filename* is whichever game version you'd like to play.

## Bugs & Feature Requests

Add an [issue on the Github repo](https://github.com/mrollinswaterman/dungeon_text/issues). 

## Attribution

Nothing yet.
