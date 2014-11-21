import re
from common.colors import CustomColors
from common.types import UserTypes
from common.videoElement import VideoElement

kMovieIdentifier = 'movie'
kSerieIdentifier = 'serie'
kIgnoreKeyword = 'sample'

class Decoder:

    # this method aims to identify if the serie category inserted
    # by the user is approximately similar to an hardcoded value here    
    def isSerieCategory(self, iCategory):
        # transform the file name in lower letters
        aLoweredCategory = iCategory.lower()
        
        # check if the serie identifier is contained in the category defined by the user
        if kSerieIdentifier in aLoweredCategory:
            return True
        return False

    # this method aims to identify if the movie category inserted
    # by the user is approximately similar to an hardcoded value here
    def isMovieCategory(self, iCategory):
        # transform the file name in lower letters
        aLoweredCategory = iCategory.lower()
        
        # check if the movie identifier is contained in the category defined by the user
        if kMovieIdentifier in aLoweredCategory:
            return True
        return False
        
    def setCategories(self, iCategories):
        if UserTypes.movie == '' or UserTypes.serie == '':
            for aCategory in iCategories.keys():
                if self.isSerieCategory(aCategory):
                    UserTypes.serie = aCategory
                elif self.isMovieCategory(aCategory):
                    UserTypes.movie = aCategory
            # if movie or serie categories have not been found throw an exception
            if UserTypes.movie == '':
                raise NameError('Movie category has not been defined')
            elif UserTypes.serie == '':
                raise NameError('Serie category has not been defined')
            print('Movie category: ' + UserTypes.movie)
            print('TV serie category: ' + UserTypes.serie)


    def searchDelimiter(self, iFileName):
        # remove the extension
        aPureFileName = iFileName[:iFileName.rfind(".")]

        # instantiate a map of not alphanum charachters with occurrences
        aDelimiterMap = {}

        # init max number of occurrences and the delimiter
        aMaxOccurrences = 0
        aFoundDelimiter = ""

        # loop in the filename, if current character is not an alphanum increment its counter
        for aChar in aPureFileName:
            if not aChar.isalnum():
                # not needed, but just for clarity purpose
                aDelimiter = aChar
                if aDelimiter in aDelimiterMap.keys():
                    aDelimiterMap[aDelimiter] +=1
                else:
                    # First occurrence of delimiter found, init its counter
                    aDelimiterMap[aDelimiter] = 1
                # check if current number of occurrences is the max
                if aDelimiterMap[aDelimiter] > aMaxOccurrences:
                    aMaxOccurrences = aDelimiterMap[aDelimiter]
                    aFoundDelimiter = aDelimiter
        return aFoundDelimiter


    def isSeriesEpisode(self, iFileName):
        # understand which is the separator
        # Algorithm: Remove the extension including the ".". Count the max number of a char different than a-z0-9
        aDelimiter = self.searchDelimiter(iFileName)
        
        # when using the directory name we could override a valid delimiter on behalf of a invalid one
        if aDelimiter != '':
            self.delimiter = aDelimiter

        # if it contains two separate numbers in a single word
        aRegExp = re.compile('.*' + aDelimiter + '.*[0-9]+[^' + aDelimiter + UserTypes.kForbiddenSerieSeparator + '0-9][0-9]+' + aDelimiter + '.*')
        if aRegExp.match(iFileName):
            return True

        return False

    def formatTitle(self, iTitle):
        aStandardDelimiter = UserTypes.kStandardDelimiter
        aFormattedTitle = ''
        
        for aWord in iTitle.split(self.delimiter):
            aFormattedTitle += aWord + aStandardDelimiter
        aFormattedTitle = aFormattedTitle[:aFormattedTitle.rfind(aStandardDelimiter)]
        
        return aFormattedTitle
    
    def retrieveTitle(self, iFileName, isSerie=False):
        aTitle = ''
        if isSerie == True:
            # regular expression aiming to find the serie and chapter, e.g. s01e03, 1x3, etc.
            aRegExp = re.compile('[' + self.delimiter + '].?[0-9]+[^' + self.delimiter + UserTypes.kForbiddenSerieSeparator + '0-9][0-9]+' + self.delimiter)
            aSerieEpisodeObject = aRegExp.search(iFileName)
            aRawTitle = iFileName[:aSerieEpisodeObject.start()]
            
        else:
            aRawTitle = iFileName[:iFileName.rfind(".")]
        
        aTitle = self.formatTitle(aRawTitle)
        
        return aTitle

    def retrieveSeasonEpisodeNumber(self, iFileName):
        # regular expression aiming to find the season and episode number
        aRegExp = re.compile('[' + self.delimiter + '].?[0-9]+[^' + self.delimiter + UserTypes.kForbiddenSerieSeparator + '0-9][0-9]+' + self.delimiter)
        aSerieEpisodeObject = aRegExp.search(iFileName)
            
        aRegExp = re.compile('[0-9]+')
        aSeasonEpisodeNumberObject = aRegExp.findall(aSerieEpisodeObject.group())
            
        return aSeasonEpisodeNumberObject

    def retrieveEpisodeTitle(self, iFileName, isFromFile=True):
        # regular expression aiming to find the season and episode number
        aRegExp = re.compile('[' + self.delimiter + '].?[0-9]+[^' + self.delimiter + UserTypes.kForbiddenSerieSeparator + '0-9][0-9]+' + self.delimiter)
        aEpisodeTitle = iFileName[aRegExp.search(iFileName).end():]
        
        if isFromFile:    
            return self.formatTitle(aEpisodeTitle[:aEpisodeTitle.rfind('.')])
        return self.formatTitle(self.formatTitle(aEpisodeTitle)) 

    def decode(self):
    	
        aVideoElement = {}
        aFileName = self.fileName
        aDirectoryName = self.directoryName
        
        if kIgnoreKeyword in self.fileName.lower():
            print('Ignored element: ' + self.fileName)
            return
        elif self.isSeriesEpisode(self.fileName):
            #print(CustomColors.GREEN + 'Serie episode found: ' + self.fileName + CustomColors.ENDC)
            aTitle = self.retrieveTitle(aFileName, True)
            aSeasonEpisode = self.retrieveSeasonEpisodeNumber(aFileName)
            
            aVideoElement = VideoElement(aTitle, UserTypes.serie, aFileName)
            aVideoElement.setSeasonChapter(aSeasonEpisode[0], aSeasonEpisode[1], self.retrieveEpisodeTitle(aFileName))
        # it could happen that the file name is not compliant with series one, but its containing folder is
        # thus we perform a "last chance" check on the parent folder
        elif self.isSeriesEpisode(aDirectoryName):
            aTitle = self.retrieveTitle(aDirectoryName, True)
            aSeasonEpisode = self.retrieveSeasonEpisodeNumber(aDirectoryName)
            
            aVideoElement = VideoElement(aTitle, UserTypes.serie, aFileName)
            aVideoElement.setSeasonChapter(aSeasonEpisode[0], aSeasonEpisode[1], self.retrieveEpisodeTitle(aDirectoryName, False))
        else:
            #print(CustomColors.BLUE + 'Movie found: ' + self.fileName + CustomColors.ENDC)
            aTitle = self.retrieveTitle(aFileName)
            aVideoElement = VideoElement(aTitle, UserTypes.movie, aFileName)
        return aVideoElement

    def  __init__(self, iFileName, iDirectoryName, iCategories):
        # set the categories
        self.setCategories(iCategories)
        # set inputs
        self.fileName = iFileName
        self.directoryName = iDirectoryName
