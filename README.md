# AvP Skin Selector
*A skin selector for the Aliens vs Predator game from 2010.*

I wrote this project in a couple of hours because my son and I started playing
this game's multiplayer mode, and he didn't have access to the pre-order skins.
I found instructions for editing the save file at 
https://steamcommunity.com/sharedfiles/filedetails/?id=1738932737, but I wanted
him to have something he could run without having to mess with a hex editor and
binary files.

## Instructions (Python script)

This script requires [Python 3](https://www.python.org) and the [Aliens vs. 
Predator game](https://store.steampowered.com/app/10680/Aliens_vs_Predator/).

You really only need to download avp_skins.py, although avp.ico is nice to have 
as the icon file used by the GUI.

To run the script, open a PowerShell window and enter:

    python avp_skins.py

This should bring up a window that is pre-populated with the path to your save
file. Clicking on the "Load" button should the set the three dropdowns to show
which skins you have selected for each race. After making any changes, you can
click on "Save" to update your save file. (You might want to make a backup copy 
of the file beforehand.) 


## Instructions (exe)

Make sure you have AvP installed first, of course. Then download the exe from 
the GitHub [releases](https://github.com/simlee009/avp_skins/releases/download/v1.0.0/avp_skins.exe) 
or the [dist](https://github.com/simlee009/avp_skins/blob/main/dist/avp_skins.exe) 
folder.

Run it, make sure that it has found the path to your saved game file, and click 
on the "Load" button. Make any changes you want, and then click "Save".
