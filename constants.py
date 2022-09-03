import os
import sys

#App Constants
app_version = "1.0"

#Get App Path Based On App Type
if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
elif __file__:
    app_path = os.path.dirname(__file__)


#UI Contsants
ui_spacing = 1

#Constant Functions
def getVersionText():
    return "UnityPackage Extractor v" + app_version