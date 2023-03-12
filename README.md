# Find-and-Sync

Find-and-Sync is a Python script that assists users in configuring and synchronizing a source directory to a destination directory using the find command, rsync, and the json, os, and subprocess modules. The script searches for source and destination directories that match user input, prompts the user to select the correct directories, and then synchronizes the selected directories. Additionally, the script can save the sync settings for future use. If saved sync settings exist, the script will prompt the user to choose a saved option or create a new sync.

# Requirements
This script requires rsync and find to be installed on your system.

# Configuration
The script creates a sync_settings.json file and reads saved sync settings from the same directory as main.py.
