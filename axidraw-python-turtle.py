from appJar import gui
import traceback, os

precode = """\

import canvasvg
import turtle
canvasvg.configure(canvasvg.SEGMENT_TO_PATH)
turtle.tracer(0,0) #tracing animation completely off for speed, https://stackoverflow.com/a/31503663/933782
turtle.hideturtle() #dont show the turtle in output

"""

postcode = """\

turtle.update()   # displays the final image

"""

postcodesvg =  """\
canvas = turtle.getscreen().getcanvas()
canvasvg.saveall("test.svg", canvas)
"""

workingFile=None

def exportSVG(code):
    code.replace("import turtle", "")
    code=precode+code+postcode
    print(code)
    exec(code)

def runCode(code):
    code.replace("import turtle", "")
    code=precode+code+postcode
    print(code)
    try:
        exec(code)
    except: # catch *all* exceptions
        formatted_lines = traceback.format_exc().splitlines()
        app.warningBox("Code Error", "%s\n%s" % (formatted_lines[-1],formatted_lines[3]))      

def press(button):
    global workingFile
    code = app.getTextArea("turtleCode")
    
    if button == "Preview":       
        runCode(code)     
    elif button == "Clear":
        app.clearTextArea("turtleCode", callFunction=False)
    elif button == "Open":
        workingFile=app.openBox(title="Select File", dirName=None, fileTypes=[('python', '*.py')], asFile=False, parent=None, multiple=False, mode='r')
        if workingFile is not None and workingFile:
            with open (workingFile, "r") as myfile:
                data=myfile.read().strip()
            app.clearTextArea("turtleCode", callFunction=False)
            app.setTextArea("turtleCode", data, end=True, callFunction=False)
    elif button == "Save":
        if workingFile is not None:
            workingFile=app.saveBox(title=None, fileName=os.path.basename(workingFile), dirName=os.path.dirname(workingFile), fileExt=".py", fileTypes=[('python', '*.py')], asFile=None, parent=None)
        else:
            workingFile=app.saveBox(title=None, fileName=None, dirName=None, fileExt=".py", fileTypes=[('python', '*.py')], asFile=None, parent=None)
        if workingFile is not None and workingFile:    
            with open ( workingFile, "w" ) as outFile :
                outFile.write ( code )
            app.setLabel("statusbar", 'Saved {}'.format(workingFile))
    elif button == "Export SVG":
        exportSVG(code)
    elif button == "Send To AxiDraw":
        app.infoBox("Lets get to it", "You pressed "+button)        
    else:
        app.infoBox("Error", "There was an error. What button did you press?")

def tabKey(key):
    print(key)
    code = app.getTextArea("turtleCode")
    code.replace("\t", "    ")
    app.clearTextArea("turtleCode", callFunction=False)
    app.setTextArea("turtleCode", code, end=True, callFunction=False)

fileMenus = ["Open", "Save", "-", "Clear"]
plotMenus = ["Preview","Export SVG","-", "Plot on AxiDraw", "-", "Check Connection"]

with gui("Turtle Draw") as app:

    #Add menus
    app.addMenuList("File", fileMenus, press)
    app.addMenuList("Plot", plotMenus, press)

    app.setStretch('column')
    app.setSticky('enw')

    #Pre editor hardcoded
    app.addLabel("preCodeLabel", precode.strip())
    app.setLabelTooltip("preCodeLabel", "This code is always prepended to your code to ensure functonality.")
    app.setLabelBg("preCodeLabel", "white")
    app.getLabelWidget("preCodeLabel").config(font="Courier 9 normal")
    app.setLabelAlign("preCodeLabel", "left")
    app.setLabelRelief("preCodeLabel", "sunken")
    
    #Textarea with highlighting for turtle
    app.setStretch("both")
    app.setSticky('news')
    app.addScrolledTextArea("turtleCode").bind("<Tab>", tabKey)
    app.setTextAreaFont("turtleCode", family="Courier",size=9,weight="normal")

    #Post editor hardcoded
    app.setStretch('column')
    app.setSticky('enw')
    app.addLabel("postCodeLabel", "turtle.update()")
    app.setLabelTooltip("preCodeLabel", "This code is always appended to your code to ensure functonality.")
    app.setLabelBg("postCodeLabel", "white")
    app.getLabelWidget("postCodeLabel").config(font="Courier 9 normal")
    app.setLabelAlign("postCodeLabel", "left")
    app.setLabelRelief("postCodeLabel", "sunken")      

    #Bottom Statusbar
    app.setStretch('column')
    app.setSticky('esw')
    app.addLabel("statusbar", "Ready...")
    app.setPadding([0,0])
    app.setLabelFont("statusbar", family="Arial",size=9,weight="normal")
    app.setLabelAlign("statusbar", "left")
    app.setLabelRelief("statusbar", "sunken")
    

