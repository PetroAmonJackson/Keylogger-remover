from tkinter import *
from tkinter import ttk
from functools import partial
from PIL import ImageTk, Image
import os 
import subprocess
'''import PyPDF2'''
from contextlib import ExitStack
from functools import partial
import threading
import platform

#window
tkWindow = Tk()

# Gets the requested values of the height and widht.
windowWidth = tkWindow.winfo_reqwidth()
windowHeight = tkWindow.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(tkWindow.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(tkWindow.winfo_screenheight()/2 - windowHeight/2)

 
# Positions the window in the center of the page.
tkWindow.geometry("+{}+{}".format(positionRight-170, positionDown-140))

tkWindow.configure(background='white')
tkWindow.resizable(0,0)
tkWindow.title('Keylogger Remove Tool')

frameMain = Frame(tkWindow,bg='green',width=820,height=300)
frameTop = Frame(tkWindow,bg='white')
frameBottom = Frame(tkWindow,bg='white')

imageSafe = Image.open("resources/safe.png")
imageSafe = imageSafe.resize((120, 120), Image.ANTIALIAS)
imageSafe = ImageTk.PhotoImage(imageSafe)

imageNotSafe = Image.open("resources/not_safe.png")
imageNotSafe = imageNotSafe.resize((120, 120), Image.ANTIALIAS)
imageNotSafe = ImageTk.PhotoImage(imageNotSafe)

imageScan = Image.open("resources/scan.png")
imageScan = imageScan.resize((120, 120), Image.ANTIALIAS)
imageScan = ImageTk.PhotoImage(imageScan)

imageReport = Image.open("resources/report.png")
imageReport = imageReport.resize((120, 120), Image.ANTIALIAS)
imageReport = ImageTk.PhotoImage(imageReport)

imageRemove = Image.open("resources/remove.png")
imageRemove = imageRemove.resize((120, 120), Image.ANTIALIAS)
imageRemove = ImageTk.PhotoImage(imageRemove)

imageProcess = Image.open("resources/process.png")
imageProcess = imageProcess.resize((120, 120), Image.ANTIALIAS)
imageProcess = ImageTk.PhotoImage(imageProcess)

scanNote = Label(frameTop, text="Scanning your computer...",fg='black',image=imageProcess,compound=LEFT, font=("Helvetica",12),background='white',width=580,height=180)

safeText = "Scan your computer first"
safeImage = imageNotSafe
safeNote = Label(frameTop, text=safeText,fg='green',image=safeImage,compound=LEFT, font=("Helvetica",12),background='white',width=580,height=180)


tkWindow.numkeyloggers = 0
scanned = []
def scanLinux():
    numkeyloggers = 0


    
    # f = open("keylogger_list.txt","w")
    newcontent = [] 
    os.chdir('/') 
    for root, dirs, files in os.walk("."): 
       for name in files : 
            x = os.path.join(root,name) 
            newcontent.append(x) 
    extensions = ['.py']
    patterns = ['logging.info(str(key))','new_hook.HookKeyboard()','pyxhook']
    for item in newcontent: 
        for ext in extensions:
            if str(item).find(ext)>=0:
                try:
                    with open(item.replace("./","/") ,'rb') as newfile:
                        content = newfile.read()
                    for pattern in patterns:
                        if str(content).find(pattern)>=0 and str(item).find("keylogger_remover_tool")<=0 and str(item).find("pyc"):
                            numkeyloggers+=1
                            print('['+str(numkeyloggers)+']--------------------------------------------------------')
                            print(item)
                            scanned.append(item)
                except OSError as e:
                    pass
    tkWindow.numkeyloggers = numkeyloggers
    safeNote.config(text="Completed Scanning ("+str(tkWindow.numkeyloggers)+" Keylogger Found) \n -------------------------------------- \n Now View Reports",image=imageNotSafe,fg='red')
   

def scanWindows():
    print("Windows")
    entries  = os.listdir("/")
    for entry in entries:
    	print(entry)

def background(scanMaster):
    if str(platform.system())==("Windows"):
        print("Runing in windows")
        safeNote.config(text=scanNote["text"],image=scanNote["image"])
        th = threading.Thread(target=scanLinux)
        th.start()
    elif str(platform.system())==("Linux"):
        print("Runing in Linux")
        safeNote.config(text=scanNote["text"],image=scanNote["image"])
        th = threading.Thread(target=scanLinux)
        th.start()
    else:
        print("Sorry os not recognized")


tkWindow.processState = ""
tkWindow.buttonState = "Scan"

#btn report clicked function
def report():
	f = open(keylogger_list, "r")
	return(f.read())
	f.close()

def reportWin(topname):
    reportWindow = Tk()

    # Gets the requested values of the height and widht.
    windowWidth = reportWindow.winfo_reqwidth()
    windowHeight = reportWindow.winfo_reqheight()
    
    # Gets both half the screen width/height and window width/height
    positionRight = int(reportWindow.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(reportWindow.winfo_screenheight()/2 - windowHeight/2)

    
    # Positions the window in the center of the page.
    reportWindow.geometry("+{}+{}".format(positionRight+170, positionDown-140))

    wrapper1 = LabelFrame(reportWindow)
    wrapper2 = LabelFrame(reportWindow)

    mycanvas = Canvas(wrapper1,width=570,background="white")
    mycanvas.pack(side=LEFT,fill="both",expand="yes")

    yscrollbar = ttk.Scrollbar(wrapper1,orient="vertical",command=mycanvas.yview)
    yscrollbar.pack(side=RIGHT,fill=Y)

    mycanvas.configure(yscrollcommand=yscrollbar.set)

    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))

    myframe = Frame(mycanvas,background="white")

    mycanvas.create_window((0,0), window=myframe, anchor="nw")

    wrapper1.pack(fill="both",expand="yes",padx=10,pady=10)
    # wrapper2.pack(fill="both",expand="yes",padx=10,pady=10)

    frameAll = Frame(myframe,background="white")

    # A Label widget to show in toplevel
    if len(scanned)<=0:
        Label(myframe, text = "Scan first to view "+topname+".",background="white", font=("Helvetica",15),fg="black").pack(padx=15,pady=15)
    else:
        # reportWindow.destroy()
        num = 0
        for x in range(len(scanned)):
            num += 1
            # Frame for listing
            frameIn = Frame(frameAll,background="white")

            # Label for serial number
            Label(frameIn, text = str(num),fg="black", font=("Helvetica",12),background="white",anchor="w",padx=5,pady=5,width=6,wraplength=350,justify=LEFT).pack(padx=10,pady=0,fill="both",side=LEFT)

            # Label for text content
            Label(frameIn, text = scanned[x],fg="blue", font=("Helvetica",10),background="white",anchor="w",padx=5,pady=5,width=54,wraplength=350,justify=LEFT).pack(padx=10,pady=0,fill="both",side=LEFT)
            if topname=="Remove":
                def printer(x):
                    removing(scanned[x])
                    scanned.remove(scanned[x])
                    reportWindow.destroy()
                    reportWin("Remove")
                removebtn = Button(frameIn, text = "Remove",command=partial(printer,x),
                fg="white", font=("Helvetica",10),background="red",padx=5,pady=5).pack(side=LEFT)

            frameIn.pack(padx=10,pady=0)
            Label(frameAll, text = "-----------------------------------------------------------------",background="white", font=("Helvetica",15),fg="black").pack(padx=15,pady=0)
        frameAll.pack()

    reportWindow.resizable(False,False)
    reportWindow.title(topname+' | Scanned Keyloggers')

    reportWindow.mainloop()
    


#btn remove clicked function
def removing(removing):
    print("Removing     "+removing+"")
    if str(platform.system()=="Linux"):
        os.system("rm '"+removing+"'")
    else:
        pass
    print("Successful Removed")


def replaceChar(toReplace):
    return (((str(toReplace).replace("['","")).replace("']","")).replace("[","")).replace("]","")

# frameTop.pack(side=TOP,padx=0,pady=0,fill=BOTH)


if str(platform.system())=="Windows":
	scanButton = Button(frameBottom, text=tkWindow.buttonState,image=imageScan,compound=TOP, font=("Helvetica",25),background='grey',width=100,padx=50,pady=20,borderwidth=0,command=lambda : background(scanWindows))
elif str(platform.system())=="Linux":
	scanButton = Button(frameBottom, text=tkWindow.buttonState,image=imageScan,compound=TOP, font=("Helvetica",25),background='grey',width=100,padx=50,pady=20,borderwidth=0,command=lambda : background(scanLinux))

scanButton.pack(side=LEFT)


safeNote.pack()
reportButton = Button(frameBottom, text="Reports",image=imageReport,compound=TOP, font=("Helvetica",25),background='grey',width=100,padx=50,pady=20,borderwidth=0,command=partial(reportWin,"Reports"))
reportButton.pack(side=LEFT)


removeButton = Button(frameBottom, text="Remove",image=imageRemove,compound=TOP, font=("Helvetica",25),background='grey',width=100,padx=50,pady=20,borderwidth=0,command=partial(reportWin,"Remove"))
removeButton.pack(side=LEFT)

frameTop.pack(side=TOP,padx=0,pady=0,fill=BOTH)
frameBottom.pack(side=BOTTOM,padx=0,pady=0,fill=BOTH)

tkWindow.mainloop()
