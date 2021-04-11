import time
import xml.etree.ElementTree as ET
from mal import *

class Finder:
    '''
    A class to find number of hours of watched anime.

    Attributes
    ----------
    animelist : str
        Anime titles seperated by commas. Default to None

    file : str
        MyAnimeList xml file containing data. Default to None

    
    Methods
    -------
    parse(file)
        parses xml to dict.

    find(mode='text')
        finds total time needed for each anime title.
    '''
    def __init__(self, animelist=None, file=None):
        if animelist:    
            self.animelist = animelist.split(',')
        
        else:
            self.animelist = animelist

        self.file = file

    def parse(self, file):
        '''
        Returns parsed xml as a dictionary

            Parameters:
                file (string): directory containing xml file

            Returns:
                dic (dictionary): containds data {malid: watched episodes}
        '''
        dic = {}

        tree = ET.parse(file)
        root = tree.getroot()

        for anime in root.findall('anime'):
            dic[int(anime.find('series_animedb_id').text)] = int(anime.find('my_watched_episodes').text)

        return dic

    def find(self, mode='text'):
        '''
        Finds average duration per episode and gets total hours watched.

        Parameters:
            mode (string): decides the method needed for extracting data.

        Returns:
            total (integer): hours watched
        '''
        
        if mode == 'text':  #If mode is 'text' then it will use self.animelist. Ex - Anime1, Anime2, Anime3
            total = 0

            for anime in self.animelist:
                print("searching...", end='\r')
                search = AnimeSearch(anime) #Searched for anime

                newsearch = Anime(int(search.results[0].mal_id)) #searched with malid to get more access to data

                duration = newsearch.duration.split()
                duration = int(duration[0]) #Gets average duration per episodes

                print("calculating...", end='\r')

                eps = newsearch.episodes #gets total episodes

                duration = eps * duration

                total += duration

            total = float(total / 60) #Convert to hours
            return total

        elif mode == "open":    #If mode is 'open' then it will use self.file. Ex - myanimelist.xml
            total = 0

            print("parsing...", end='\r')
            data = self.parse(self.file) #Parses xml file

            totalen = len(data.keys())

            for malid, eps in data.items(): #Iterate through each anime

                num = list(data.keys()).index(malid)

                print("{}/{} done - searching... MALid={}".format(str(num), totalen, malid), end='\r')
                anime = Anime(malid) #Search for anime

                print("calculating...", end='\r')
                try:
                    duration = anime.duration.split()
                    duration = int(duration[0]) #Get average duration per episode

                except AttributeError:
                    duration = 0 #If it has no episodes

                duration = eps * duration

                total += duration

            total = float(total / 60) #Converting to hours
            return total

#Simple useage of both modes
while True:
    command = input(">")

    if command == "help":
        print(">text - finds hours watched from a string given in the following format: anime1, anime2, anime3")
        print(">open - opens a MyAnimeList xml file and finds hours watched.")
        print(">exit - exits the program")
        print(">help - prints this message\n")

    if command == "text":
        lst = input("Enter anime, seperate with commas - ")
        brain = Finder(lst)
        hours = brain.find()

        print("You've watched {} hours of anime\n".format(hours))

    if command == "open":
        file = input("Enter file directory - ")
        brain = Finder(file=file)
        hours = brain.find("open")

        print("You've watched {} hours of anime\n".format(hours))

    if command == "exit":
        break
