#!/usr/bin/env python3

import fnmatch
import glob 
import os
import sys

from common.colors import CustomColors
from common.settings import Settings
from common.decoder import Decoder
from common.mover import Mover
from common.types import UserTypes
from common.videoElement import VideoElement

def moveElements(iElements, iSettings):
    for aElement in iElements:
        aMover = Mover(aElement, iSettings.categories)
        aMover.move()
    # if it is movie, move to Movie dir
        # if it is HD (720 1080)
    
    # else if it is serie
    #   remove delimiters, all to lower, apply same process to all dir within serie
    #   if at least one of them matches => move file into it

def retrieveFilesToMove(iSettings):
    aFolder = iSettings.categories['Downloads']
    aExtensions = iSettings.extensions

    # init an empty list of video elements
    aVideoElementList = []
    
    print(CustomColors.YELLOW + 'Looking for all files with extension: ' + CustomColors.RED + aExtensions + CustomColors.ENDC)
    print(CustomColors.YELLOW + 'in folder: ' + CustomColors.RED + aFolder + CustomColors.ENDC)
   
    # maximum level of recursion will be 1
    aRecursionLevel = 0
    for aRootPath, aDirs, aFiles in os.walk(aFolder):
        #aRecursionLevel +=1
        #print ('Recursion level: ' + str(aRecursionLevel))
        #if aRecursionLevel <= 10:
            for aFileName in aFiles:
                if aFileName.endswith(tuple(aExtensions.replace(" ", "").split(','))): 
                    # store the parent directory of current file. It could be helpful
                    # whenever a series episode file name is not formatted according 
                    # the expected standard, but its containing directory does
                    aParentDir = aRootPath[aRootPath.rfind("/")+1:]
                    print(aRootPath)
                
                    # decode current file name into a video element BOM
                    aDecoder = Decoder(aFileName, aParentDir, iSettings.categories) 
                    aVideoElement = aDecoder.decode()
                    if aVideoElement is not None:
                        aVideoElement.setInputPath(aRootPath)
                        if aVideoElement.elementType == UserTypes.movie:
                            print(CustomColors.GREEN + 'Movie found: \'' + aVideoElement.title + '\'' + CustomColors.ENDC)
                        elif aVideoElement.elementType == UserTypes.serie:
                            print(CustomColors.BLUE + 'Serie found: \'' + aVideoElement.title + '\'' + CustomColors.ENDC)
                            print(CustomColors.BLUE + '             Season: \'' + aVideoElement.getSeason() + '\' - Episode: \'' + aVideoElement.getEpisode() + '\'' + CustomColors.ENDC)
                
                        # insert the video decoded element into the output list
                        aVideoElementList.append(aVideoElement)
    
    return aVideoElementList

if __name__ == '__main__':
	# init the settings, by config file if present, or by input requested to the user
    aSettings = Settings()
    print(aSettings.categories)
    
    # retrieve the files to move
    aFilesToMove = retrieveFilesToMove(aSettings)

    # move the files to their destination
    moveElements(aFilesToMove, aSettings)
    #print(aSettings.categories['TV Series'])
    #print(aSettings.alejandra)
