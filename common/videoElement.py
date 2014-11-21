from common.types import UserTypes

class VideoElement:
    def getSeason(self):
        if self.elementType == UserTypes.serie:
            return self.season
        else:
            raise NameError('This element is not a ' + UserTypes.serie)

    def getEpisode(self):
        if self.elementType == UserTypes.serie:
            return self.chapter
        else:
            raise NameError('This element is not a ' + UserTypes.serie)
            
    def getEpisodeTitle(self):
        if self.elementType == UserTypes.serie:
            return self.episodeTitle
        else:
            raise NameError('This element is not a ' + UserTypes.serie)
    
    def getInputPath(self):
        if self.inputPath != None:
            return self.inputPath
        else:
            raise NameError('The input path has not been defined')
            
    def setInputPath(self, iPath):
        self.inputPath = iPath
        
    def setEpisodeTitle(self, iTitle):
        self.episodeTitle = iTitle

    def setSeasonChapter(self, iSeason, iChapter, iEpisodeTitle=None):
        self.season = iSeason
        self.chapter = iChapter
        if iEpisodeTitle == None:
            self.episodeTitle = ''
        else:
        	self.episodeTitle = iEpisodeTitle
        
    def __init__(self, iTitle, iType, iFileName):
        self.title = iTitle
        self.elementType = iType
        self.fileName = iFileName
