# Slyrex Arma3 Helpful Server Scripts
 This is just a project to make simple scripts for help for arma3, such as automatically formatting mods from a folder etc, the current project does as follows:
 It is a simple gui which will select and remember your MOD folder and your param file and will automatically update your param file with the correct formatting for mods after the mod=@test123;test;123 etc.
    It will remember the mods you have unfiltered incase you didn't want to load a specific mod, making it much easier to quickly update a modlist to your params when you've downloaded a new mod set for a campaign instead of copy and pasting.

# Changelog 
    Initial - added functionality to format mods

    v2 - added GUI and functionality to auto update param file

    v3 - added settings.json to remember unfiltered mods

    v4 - added choose your own path for param file and mods folder, save settings for path functionality and mods folder and will load and remember them

    v5 - Added HTML parsing to extract the mod ids and mod names from a HTML modlist to make it easier for server admins to move to a new modlist.

    v5.1 - Added parse modlist html results to steamcmd batch file will now auto-format all mods in a mod list like steamcmd +login anonymous +workshop_download_item 107410 WORKSHOPID +quit

    v6.0 - Fixed a typo with mods= and changed it to correct formatting mod=", Added a check box to export them with a @ or not, changed how steamcmd export works, will now export a bat file and a text file you save, will prompt you for login to save to file and destiation directory.
    Added lowercase all files in folder in the fringe cases of copy and pasting while steamcmd is down.
    few other bug fixes.

    More to come, please request suggestions to make your life easier.

# Installation
To run this file, make sure you have Python installed to PATH https://www.python.org/downloads/

And open a commandline and type: pip install beautifulsoup4
<<<<<<< HEAD
Then run the script from commandline

> This project is very much a WIP and I'm using it as a practice tool to learn python
=======
and launch it from command line


> Note this project is very much a WIP and I'm using it as a practice tool to learn python.
>>>>>>> f43199ea2b59869cc0d68fa3c1b300de89ddbb8b
