import json
import os
import shutil

from common.colors import CustomColors
from common.types import UserTypes

""" Configuration file path """
kSettingsDirectory = "./settings"
kAssociationConfiguration = kSettingsDirectory + "/associationConfiguration.json"

class Mover:
    def compressName(self, iNameToCompress):
        aSpacelessName = iNameToCompress.replace(UserTypes.kStandardDelimiter, "")
        return aSpacelessName.lower()

    def retrieveTvSerieFolder(self, iTitle):
        aExistingTvSerieFolder = ''
        
        # in order to match more results in the research of a similar TV serie existing folder
        # it is better to compare current TV serie compressed title with existing compressed ones
        aCompressedTvSerieTitle = self.compressName(iTitle)
        
        for aRootPath, aDirs, aFiles in os.walk(self.outputDirectory):
            for aDirectory in aDirs:
                # compress the directoryname in lowercase-spaceless
                aDirectoryCompressedName = self.compressName(aDirectory)
                
                # I assume that if the current TV serie title is contained on an existing
                # TV serie title or vice-versa, this means that the TV serie is already present
                if (aDirectoryCompressedName in aCompressedTvSerieTitle) or (aCompressedTvSerieTitle in aDirectoryCompressedName):
                    aExistingTvSerieFolder = aDirectory
                # else if the config file exists
                elif aCompressedTvSerieTitle in self.knownAssociations.keys():
                    aExistingTvSerieFolder = self.knownAssociations[aCompressedTvSerieTitle]
        return aExistingTvSerieFolder

    def saveConfiguration(self):
        # check the existence of the configuration directory
        if not os.path.isdir(kSettingsDirectory):
            # create a new directory
            os.makedirs(kSettingsDirectory)
            os.chmod(kSettingsDirectory, 0o750)
        
        # save the configuration in new file
        aOutputFile = open(kAssociationConfiguration, 'w')
        json.dump(self.knownAssociations, aOutputFile, indent=4)
        aOutputFile.close()

    def move(self):
        aSerieOutputFolder = '' 
        aSerieOutputPath = ''
        aExtension = self.fileName[self.fileName.rfind('.'):] 

        if self.elementType == UserTypes.serie:
            # scan the present TV series and look if current one alreay exists
            aExistingSerieTvDirectory = self.retrieveTvSerieFolder(self.title)
            
            if aExistingSerieTvDirectory != '':
                aSerieOutputPath += '/' + aExistingSerieTvDirectory
                if self.title != self.originalTitle:
                    aCompressedTitle = self.compressName(self.originalTitle)
                    self.knownAssociations[aCompressedTitle] = aExistingSerieTvDirectory

                    # save the new/update configuration file
                    self.saveConfiguration()

                print('TV Serie already existing in folder: ' + aExistingSerieTvDirectory)
                aSerieOutputFolder = '/' + aExistingSerieTvDirectory
            else:
                print('New serie found: ' + self.title)
                aSerieOutputPath += '/' + self.title
                aCreateNewFolder = input('Do you want to create a new folder with this name? \'Y/n\'')
                if aCreateNewFolder.lower() == 'y':
                    aSerieOutputFolder = '/' +self.title
                    # create the new directory
                    aNewDirPath = self.outputDirectory + aSerieOutputFolder
                    os.makedirs(aNewDirPath)
                    # change the rights
                    os.chmod(aNewDirPath, 0o776)
                    # change the user/group cloning them from the input file
                    aUid = os.stat(self.inputDirectory + '/' + self.fileName).st_uid
                    aGid = os.stat(self.inputDirectory + '/' + self.fileName).st_gid
                    os.chown(aNewDirPath, aUid, aGid)
                    print(CustomColors.CYAN + 'Created new directory: ' + aSerieOutputFolder + CustomColors.ENDC)
                elif aCreateNewFolder.lower() == 'n':
                    self.title = input('Please insert the name of new TV Serie folder: ')
                    
                    # search if new title is an existing directory
                    # aExistingSerieTvDirectory = self.retrieveTvSerieFolder(aNewTitle)
                    #if aExistingSerieTvDirectory != '':
                    # create a compressed value of current title

                    # recursively call this method with the new title
                    self.move()
                    return
            aSerieOutputPath += UserTypes.kStandardDelimiter +UserTypes.kStandardSeparator 
            aSerieOutputPath += UserTypes.kStandardDelimiter + UserTypes.kSeriePrefix + self.seasonNumber + UserTypes.kEpisodePrefix + self.episodeNumber
            aSerieOutputPath += UserTypes.kStandardDelimiter + self.episodeTitle + aExtension
        #elif self.elementType == UserTypes.movie:
            
        # do the move here
        aInputPath = self.inputDirectory + '/' + self.fileName
        aOutputPath = self.outputDirectory + aSerieOutputFolder + aSerieOutputPath
        #print('File \'' + aInputPath + '\' should be moved to folder: \'' + aOutputPath + '\'')
        shutil.move(aInputPath, aOutputPath)
        print(CustomColors.CYAN + 'Moved: ' + self.fileName + ' to ' + self.outputDirectory + '/' + aSerieOutputFolder + CustomColors.ENDC)
	    
    def __init__(self, iElement, iCategories):
        self.elementType = iElement.elementType
        self.fileName = iElement.fileName
        self.originalTitle = iElement.title
        self.title = iElement.title
        if self.elementType == UserTypes.serie:
            self.episodeTitle = iElement.getEpisodeTitle()
            self.seasonNumber = iElement.getSeason()
            self.episodeNumber = iElement.getEpisode()
        self.outputDirectory = iCategories[self.elementType]
        self.inputDirectory = iElement.getInputPath()
        # check if the association configuration file exists
        if os.path.isfile(kAssociationConfiguration):
            aInputFile = open(kAssociationConfiguration)
            self.knownAssociations = json.load(aInputFile)
            aInputFile.close()
        else:
            self.knownAssociations = {}
