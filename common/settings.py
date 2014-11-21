import json
import os

""" Configuration file path """
kConfigurationDirectory = "./settings"
kConfigurationFile = kConfigurationDirectory + "/configuration.json"
      
class Settings:
    
    def loadConfiguration(self): 
        print('Initializing the custom settings..')
        aInputFile = open(kConfigurationFile)
        self.__dict__ = json.load(aInputFile)
        aInputFile.close()
    
    def saveConfiguration(self):
        print('Storing configuration file in : ' + kConfigurationFile) 
        
        # check the existence of the configuration directory
        if not os.path.isdir(kConfigurationDirectory):
            # create a new directory
            os.makedirs(kConfigurationDirectory)
            os.chmod(kConfigurationDirectory, 0o750)
        
        # save the configuration in new file
        aOutputFile = open(kConfigurationFile, 'w')
        json.dump(self.__dict__, aOutputFile, indent=4)
        aOutputFile.close()
         
    def manualConfigure(self):
        print('Settings not available..')
        print('INIT phase started..') 
        # Ask the extension supported to the user
        self.extensions = input('Enter the extensions of files you want to support separated by comma: ') 
        # Ask the categories supported to the user
        self.categories = {}
        self.categories["Downloads"] = input('Enter the absolute path of Downloads directory: ') 
        aCategory = ''
        while(aCategory != "quit"): 
            aCategory = input('Enter the new category (type \"quit\" to exit): ') 
            if aCategory != "quit":
                aRequest = "Enter the absolute path of new \"" + aCategory + "\" category: "
                aPath = input(aRequest) 
                self.categories[aCategory] = aPath
        # Save new configuration to file
        self.saveConfiguration()

    def checkConfigurationFileIntegrity(self):
        aIsConfigOk = False
        # TODO: add more integrity checks, such as a check on categories, paths, etc
        aIsConfigOk = os.path.isfile(kConfigurationFile)

        return aIsConfigOk
     
    def __init__(self):
        # check configuration file integrity
        if self.checkConfigurationFileIntegrity():
            self.loadConfiguration()
        else:
            # request the user the data to initialize the program
            self.manualConfigure()
            for aCategory in self.categories:
                print('Category: ' + aCategory); 
                aPath = self.categories[aCategory]
                print('Absolute path: ' + aPath)
                print(os.listdir(aPath)) 
                print('Exiting')

