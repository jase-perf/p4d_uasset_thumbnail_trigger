# p4d_uasset_thumbnail_trigger
A server-side trigger for Helix Core to add thumbnail images for Unreal Engine uasset files (when they exist in Unreal Engine).

This will add a thumbnail attribute to the uasset file in Helix Core, allowing you to view thumbnails for most uasset files in Helix DAM and in P4V. This should work for any .uasset files that have a thumbnail image in the Unreal Editor content browser, but not files with a generic icon, like skeletal meshes, animations, physics materials, etc..

## Installation

### Install P4Python
The Helix Core server where p4d is running must have [Python3](https://wiki.python.org/moin/BeginnersGuide/Download) and [P4Python](https://www.perforce.com/manuals/p4python/Content/P4Python/python.installation.html) installed.

### Super User Credentials
The Helix Core server where p4d is running must have P4USER set to a super user account (ideally with an unlimited ticket so the login won't expire).
[Triggers, Scripts, Swarm; Preventing Login/Password Timeouts for Automated Systems](https://portal.perforce.com/s/article/2589)

### Add script to server
Copy the `create_uasset_thumbnails.py` script to the Helix Core server to a location that the server user has permission to access.

For example, if your p4d user is named `perforce` you could copy the file to `/home/perforce/triggers/create_uasset_thumbnails/create_uasset_thumbnails.py`

### Create trigger
From any machine with the Helix Core command line client installed, run the triggers command to edit the triggers and add a new line for the `create_uasset_thumbnails.py` script. (Make sure you do this as a Super user)

`p4 triggers`

```
Triggers:
	uasset_thumbs change-commit //... "python3 /home/perforce/triggers/create_uasset_thumbnails/create_uasset_thumbnails.py %change%"
```

Then save the file and close the text editor. Your terminal should say `Triggers saved.`

By default, this will run on all changelists submitted to the server, will check them for any .uasset files, and will add thumbnail attributes to any that it can. If you want to limit the trigger to only run on certain files, you can change the `//...` to a specific depot path, or a specific file type.
