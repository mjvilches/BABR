# BABR (Blender Animation Batch Renderer)
An application that allows Blender users to render multiple batches of .blend files.

Just run Blender Animation Batch Renderer.exe and the rest should be easy to understand!

ADD - Allows users to add Blender poject files(.blend)

EDIT - Allows users to edit a selected Blender project file. This simply opens Blender.

REMOVE - Removes a selected file

Clear List - Clears the list of .blend files

CHANGE - allows users to change Blender Directory

RENDER - Starts rendering all the files in the list.

NOTE:

This application only works for Animation-related projects.

You should also keep BABR.ico in the same folder with either the .exe or .py file so it runs well.
However, you can delete this line:

root.iconbitmap('BABR.ico')

from the .py script to get rid of this issue but lose the icon image.

I used pyinstaller to create the .exe. And used PyCharm for python coding.

If you make changes in the python script and want to update the .exe:

Make sure to install pyinstaller. Delete the old .exe and run this command on cmd inside the same folder where the .py is:

pyinstaller --noconsole --onefile --noupx --icon=app.ico --name "name of app" app.py

omit "--icon-app.ico" if you don't want the icon.


