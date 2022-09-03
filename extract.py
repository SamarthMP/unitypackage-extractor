import constants
import os
import tarfile
import pathlib
import shutil
import tkinter as tk
import tkinter.ttk as ttk

globalStatusText = None

def error(err):

    if (globalStatusText != None):
        globalStatusText.config(text = "[ERROR] " + err)

    print("[ERROR] " + err)

def extractAsset(assetPath, outputPath, useMeta, progressBar, totalFileCount):

    #Get The First Line Of The pathname File
    pathname = open(os.path.join(assetPath, "pathname"), "r").read().split("\n")[0]

    #Make Directory Tree
    try:
        pathlib.Path(os.path.join(outputPath, os.path.dirname(pathname))).mkdir(parents=True, exist_ok=True) 
    except:
        error("Extraction Failed On Second Stage: Directory Tree Creation Of " + pathname)
        return

    #Move The Asset To It's Place
    try:
        assetFilePath = os.path.join(assetPath, "asset")

        #Make Sure That It's Actually A File First
        if (os.path.isfile(assetFilePath)):

            #Set Status
            if (globalStatusText != None):
                globalStatusText.config(text = "Moving " + os.path.basename(pathname))

            os.rename(assetFilePath, os.path.join(outputPath, pathname))
    except:
        error("Extraction Failed On Third Stage: Asset Moving " + os.path.join(assetPath, "asset") + " To " + os.path.join(outputPath, pathname))
        return

    #Move The Meta File To It's Place
    try:
        metaFilePath = os.path.join(assetPath, "asset.meta")

        #Make Sure That Meta Moving Is Enabled
        if (useMeta):
            os.rename(metaFilePath, os.path.join(outputPath, pathname + ".meta"))
    except:
        error("Extraction Failed On Fourth Stage: Meta Moving " + os.path.join(assetPath, "asset.meta") + " To " + os.path.join(outputPath, pathname + ".meta"))
        return

    print("[SUCCESS] Extracted " + pathname)

    if (progressBar != None):
        progressBar["value"] += 100 / totalFileCount

def extract(pkgPath, useMeta, progressBar, statusText):
    if (os.path.isfile(pkgPath)):

        #Init Status
        global globalStatusText
        globalStatusText = statusText

        #Set Output Path
        outputPath = os.path.splitext(pkgPath)[0] + "_Output"
        tempPath = os.path.join(os.path.splitext(pkgPath)[0] + "_Output", "Extractor_Temp")

        #Check If Output Already Exists:
        if (os.path.exists(outputPath)):
            error("Output Directory Already Exists: " + outputPath)
            return
        
        os.mkdir(outputPath)
        os.mkdir(tempPath)

        #Set Status
        if (globalStatusText != None):
            globalStatusText.config(text = "Extracting...")

        #Extract The Package As If It Was A Tar.GZ
        try:
            file = tarfile.open(pkgPath)
            file.extractall(tempPath)
            file.close()
        except:
            error("Extraction Failed On First Stage: targz Extraction")
            return

        #Get A List Of All Assets
        assets = [ f.path for f in os.scandir(tempPath) if f.is_dir() ]
        for asset in assets:
            extractAsset(asset, outputPath, useMeta, progressBar, len(assets))

        #Clean Up
        shutil.rmtree(tempPath)

        print("[SUCCESS] Extracted Assets To " + outputPath)

        #Only Show In File Manager If GUI Mode
        if (progressBar != None):
            try:
                from showinfm import show_in_file_manager
                show_in_file_manager(outputPath)
            except:
                pass

        if (progressBar != None):
            progressBar.stop()

        #Set Status
        if (globalStatusText != None):
            globalStatusText.config(text = "Extraction Complete!")
    else:
        error("File Does Not Exist: " + pkgPath)
