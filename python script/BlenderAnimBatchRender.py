import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import filedialog, messagebox, ttk
from tkinter import *
import subprocess, os
from subprocess import Popen

root = tk.Tk()
renderNames,blenderLoc,runCommands,result,saveFile = [],[],[],[],[]
path = 'C:\Program Files\Blender Foundation\Blender 2.90'

def loadProject(): ## Load menubar command

    load = filedialog.askopenfile(initialdir="/", title="Load Batch Render Project",
                                      filetypes=(("Text Files", "*.txt"),("All Files","*.*")))
    if load == None:
        return
    else:
        renderNames.clear()
        blenderLoc.clear()
        runCommands.clear()
        frameFILES.delete(0,END)

        with open(f'{load.name}', 'r') as l:
            loadlist = l.read()
            loadlist = loadlist.split(',')
            newlist = [x for x in loadlist if x.strip()]

            ## Appends Blender Location to blenderLoc
            blenderLoc.append(f'{newlist[0]}')
            bDirectory.delete(0, END)
            bDirectory.insert(1,f"{newlist[0]}")
            messagebox.showinfo("",f"Blender Directory set to: {newlist[0]}")

            ## removes Blender Location in loadlist
            bd = newlist[0]
            newlist.remove(bd)

            ##Adds Loaded File Names to renderNames
            for names in newlist:
                renderNames.append(names)
                frameFILES.insert(END, f'{names}')


def saveProject(): ## Save menubar command

    saveFile.clear()

    save = filedialog.asksaveasfile(initialdir="/", title="Save Batch Render Project",
                                    mode='w', defaultextension='.txt',
                                    filetypes=(("Text Files", "*.txt"),("All Files","*.*")))
    if save == None:
        return
    else:

        saveFile.append(f'{blenderLoc[0]}' + ',')

        for names in renderNames:
            saveFile.append(names + ',')

        saveList = str("{}" * len(saveFile)).format(*saveFile)
        save.write(saveList)

        messagebox.showinfo('',f'Project saved to: {save.name}')


def blenderPath(): ## Blender Directory Command

    location = filedialog.askdirectory(initialdir="/")

    if location == '':
        return
    else:
        blenderLoc.clear()
        bDirectory.delete(0, END)
        messagebox.showinfo("", f"Blender Directory is: {location}")
        blenderLoc.append(location)

    bDirectory.insert(1,f'{location}')



def addBlendFile(): ## ADD button command

    if os.path.exists("render.bat"):
        os.remove("render.bat")

    filenames = filedialog.askopenfiles(initialdir="/", title="Select Files",
                                      filetypes=(("Blend Files", "*.blend"),("All Files","*.*")))

    if filenames == "":
        return

    frameFILES.delete(0,END)

    for names in filenames:
        renderNames.append(names.name)

    for add in renderNames:
        frameFILES.insert(END, f'{add}')

def removeFiles(): ## REMOVE button command

    if renderNames == []:
        messagebox.showinfo("","No Files to Remove!")
        return
    if frameFILES.curselection() == ():
        messagebox.showinfo('','No File Selected!')

    else:

        confirm = messagebox.askyesno("","Are you sure?")


        if confirm == True: ## removes the selected file

            curselect = frameFILES.curselection()
            selected = frameFILES.selection_get()

            print(renderNames)
            frameFILES.delete(curselect)
            renderNames.remove(selected)
            print(renderNames)

        else:
            return

def editFile():

    if os.path.exists("edit.bat"):
        os.remove("edit.bat")

    if renderNames == []:
        return
    if frameFILES.curselection() == ():
        messagebox.showinfo("","No File Selected!")
    else:
        selected = frameFILES.selection_get()

        editCommands = []

        editCommands.append(f"cd {blenderLoc[0]}")
        editCommands.append(f'blender "{selected}"')

        commandlist = str("{}\n" * len(editCommands)).format(*editCommands)


        e = open("edit.bat", "w")
        e.write(commandlist)
        e.close()

        p = subprocess.Popen('edit.bat', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, creationflags=0x08000000)

        # Until I get last line and the end of string:
        while p.stdout is not None:

            line = p.stdout.readline()

            root.mainloop() ## keeps gui responsive

            if not line:
                p.stdout.flush()
                break

        editCommands.clear()

def clearFilesList(): ## Clear Files List

    if renderNames == []:
        messagebox.showinfo('', "Empty List!")

    else:

        cf = messagebox.askyesno("", "Are you sure?")

        if cf == True:
            pass
        else:
            return

        renderNames.clear()
        saveFile.clear()
        runCommands.clear()
        frameFILES.delete(0,END)

def renderAll(): ## render button command

    runCommands.clear()
    statusFrame.delete(0,END)

    if blenderLoc == []: ## asks user if the path to Blender is correc
        messagebox.showinfo("", "No Blender Directory Set!")
        if messagebox.NO:
            blenderPath()
            return


    if renderNames == []: ## tells user that there are no files selected for rendering
        messagebox.showinfo("", "No Files to Render!")
        return
    else: ## render is a go

        if os.path.exists("render.bat"):
            os.remove("render.bat")

        renderConfirm = messagebox.askyesno('', 'ARE YOUR REALLY READY?')

        if renderConfirm == True:

            cancelled = []
            currentBlend = []

            ## Creates the render.bat file

            runCommands.append(f'cd {blenderLoc[0]}')

            for files in renderNames:
                runCommands.append(f'blender -b "{files}" -a')

            commandlist = str("{}\n" * len(runCommands)).format(*runCommands)

            # with open('render.bat', 'w') as f:
            #     f.write(commandlist)

            f = open("render.bat", "w")
            f.write(commandlist)
            f.close()

            # Draw progressbar:
            style = ttk.Style()
            style.theme_use('default')
            style.configure("black.Horizontal.TProgressbar", background='green')
            bar = Progressbar(frame2, style='black.Horizontal.TProgressbar', mode='indeterminate')
            bar.pack(anchor='s', fill='x')

            # Execute some job with multiple lines on stdout:
            p = subprocess.Popen('render.bat', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, creationflags=0x08000000)

            def cancelRender():
                c = messagebox.askyesno('', 'Are you sure?')

                if c == True:
                    Popen("TASKKILL /F /PID {pid} /T".format(pid=p.pid))
                    cancelled.append("Cancelled")
                    currentBlend.clear()
                    runCommands.clear()
                else:
                    return

            cancel = tk.Button(frame2, text="Cancel", command=cancelRender)
            cancel.pack(anchor='s')

            bar.start()

            frame = 1

            # Reads each line from the process
            while p.stdout is not None:

                line = p.stdout.readline()

                # Add line in list and remove carriage return
                l = line.decode('UTF-8').rstrip('\r')

                # Updates Progress Bar
                # And Status

                bar.update()

                if l.startswith("Read blend:"):

                    b = list(l.replace("Read blend:", "").strip('\n'))
                    b2 = []
                    blend = []

                    for c in reversed(b):
                        if c == '/':
                            break
                        b2.append(c)

                    for c in reversed(b2):
                        blend.append(c)

                    blendName = ''.join(blend)

                    if currentBlend != []:
                        statusFrame.delete(0,END)
                        currentBlend.clear()

                    currentBlend.append(blendName)

                    statusFrame.insert(END, f'RENDERING: {blendName}')
                    statusFrame.insert(END, '---')
                    statusFrame.insert(END, '')
                    statusFrame.yview(END)

                if l.startswith("Fra:"):

                    if frame <= 8: #frames in ones gets printed

                        currentframe = int(l[4:5])

                        if currentframe > frame:
                            frame += 1
                            statusFrame.insert(END, f'Now rendering frame {currentframe}...')
                            statusFrame.yview(END)

                    if (frame >= 9) and (frame <= 98): #frames in tens gets printed

                        currentframe = int(l[4:6])

                        if currentframe > frame:
                            frame += 1
                            statusFrame.insert(END, f'Now rendering frame {currentframe}...')
                            statusFrame.yview(END)

                    if (frame >= 99) and (frame <= 998): #frames in hundreds gets printed

                        currentframe = int(l[4:7])

                        if currentframe > frame:
                            frame += 1
                            statusFrame.insert(END, f'Now rendering frame {currentframe}...')
                            statusFrame.yview(END)

                    if (frame >= 999) and (frame <= 9998): #frames in thousands gets printed

                        currentframe = int(l[4:8])

                        if currentframe > frame:
                            frame += 1
                            statusFrame.insert(END, f'Now rendering frame {currentframe}...')
                            statusFrame.yview(END)

                    if (frame >= 9999) and (frame <= 99998): #frames in ten-thousands gets printed

                        currentframe = int(l[4:9])

                        if currentframe > frame:
                            frame += 1
                            statusFrame.insert(END, f'Now rendering frame {currentframe}...')
                            statusFrame.yview(END)

                    if (frame >= 99999) and (frame <= 999998): #frames in hundred-thousands gets printed

                        currentframe = int(l[4:10])

                        if currentframe > frame:
                            frame += 1
                            statusFrame.insert(END, f'Now rendering frame {currentframe}...')
                            statusFrame.yview(END)

                if l.startswith("Append"):
                    statusFrame.select_set(END)
                    statusFrame.delete(statusFrame.curselection())

                if l.startswith("Blender quit"):
                    frame = 1
                    statusFrame.delete(0,END)
                    statusFrame.insert(END, f'RENDERED: {currentBlend[0]}')
                    statusFrame.yview(END)


                # Ends loop when process is done
                if not line:
                    p.stdout.flush()
                    break

            if cancelled != []:
                bar.stop()
                statusFrame.delete(0, END)
                statusFrame.insert(END, "***RENDER CANCELLED***")
                cancelled.clear()

            else:
                statusFrame.delete(0, END)
                statusFrame.insert(END, 'ALL FILES RENDERED!')
                statusFrame.yview(END)
                bar.stop()
                messagebox.showinfo("", "RENDER DONE!")

            bar.destroy()
            cancel.destroy()

        else:
            return

## Canvas
canvas = tk.Canvas(root, height=550, width=700)
canvas.pack()

## Menu Bar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=loadProject)
filemenu.add_command(label="Save", command=saveProject)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


## Frames
frame = tk.Frame(root, bg="#d6d6d6", bd=20)
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.02)

frame2 = tk.Frame(frame, bg="#d6d6d6", relief="groove")
frame2.place(relwidth=0.9, relheight=0.8, relx=0.05, rely=0.12)

file = tk.Label(frame2, text="Blend Files:", bg="#d6d6d6")
file.pack(anchor='nw')

frameFILES = tk.Listbox(frame2, bg="white", height=11)
frameFILES.pack(side='top', fill='x')

status = tk.Label(frame2, text="Status:", bg="#d6d6d6")
status.pack(anchor='sw')

statusFrame = tk.Listbox(frame2, bg="black",fg='white', height=5)
statusFrame.pack(anchor='s',fill='x')


## Top Buttons
openFile = tk.Button(frame, text="Add", padx=10, pady=5, fg="black", command=addBlendFile)
openFile.place(relwidth=0.15, relheight=0.075, relx=0.05, rely=0.01)

editFile = tk.Button(frame, text="Edit", padx=10, pady=5, fg="black", command=editFile)
editFile.place(relwidth=0.15, relheight=0.075, relx=0.215, rely=0.01)

removeFile = tk.Button(frame, text="Remove", padx=10, pady=5, fg="black", command=removeFiles)
removeFile.place(relwidth=0.15, relheight=0.075, relx=0.380, rely=0.01)

clearList = tk.Button(frame, text="Clear List", padx=10, pady=5, fg="black", command=clearFilesList)
clearList.place(relwidth=0.15, relheight=0.075, relx=0.79, rely=0.01)

## Bottom Buttons
renderButton = tk.Button(frame, text="RENDER", padx=10, pady=5, fg="black", command=renderAll)
renderButton.place(relwidth=0.15, relheight=0.09, relx=0.79, rely=0.935)

## Blender Directory
if blenderLoc == []:
    blenderLoc.append((f'{path}'))

bDirectoryTitle = tk.Label(frame, text=f"Current Blender Directory:", bg="#d6d6d6")
bDirectoryTitle.place(relx=0.05, rely=0.92)

bDirectory = tk.Entry(frame)
bDirectory.place(relwidth=0.50, relheight=0.05, relx=0.05, rely=0.97)
bDirectory.insert(1,f"{blenderLoc[0]}")

changeButton = tk.Button(frame, text="Change", padx=10, pady=5, fg="black", command=blenderPath)
changeButton.place(relwidth=0.15, relheight=0.09, relx=0.56, rely=0.935)

root.iconbitmap('BABR.ico')
root.title("Blender Animation Batch Renderer")
root.config(menu=menubar)
root.mainloop()

#removes generated .bat files
if os.path.exists("edit.bat"):
    os.remove("edit.bat")

if os.path.exists("render.bat"):
    os.remove("render.bat")