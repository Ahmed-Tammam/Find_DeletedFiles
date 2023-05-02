
Windows Recycle Bin Dump Script

This script searches for deleted files in the Windows Recycle Bin and moves them to a specified dump directory. It uses the Windows Registry to locate the Recycle Bin directory and then iterates over all subdirectories to find deleted files. The dumped files are moved to a user-specified directory for further analysis

Requirements:

-The winreg module is required to access the Windows Registry. (pip install winreg)

-The script must be run with administrative privileges to access the Recycle Bin directory.

Usage
To use this script, simply run it from the command line or an IDE. The script will automatically search for the Recycle Bin directory and prompt the user for a dump directory. The dumped files will be moved to the specified directory, and the script will print the path of each dumped file to the console.

--------------------------------------------------------------------------------------------------------------------------------------
Feel free to customize this description as needed for your specific use case. Good luck with your project!
