# IMPORTS
from bs4.element import SoupStrainer
import requests, html5lib, curses, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv("constantVariables.env")

class sieveWeatherCom:
    def __init__(self):
        pass
    
    def Main(self):
        """CODE HERE>>>"""
        # SETUP

        self.URL = os.getenv("URL")
        
        self.vars = {
            'postal code': f'{os.getenv("POSTALCODE")}',
            'geographical location': '',
            'source': f'{self.URL}'
        }

        request = requests.get(self.URL)
        self.soup = BeautifulSoup(request.content, 'html5lib')

        # SETUP CURSES
        stdscr = curses.initscr()
        stdscr.clear()
        stdscr.refresh()
        
        # CURSES ADD WIDGETS
        self.Scrape()
        stdscr.addstr(f"Source: {self.vars['source']}\n")
        stdscr.addstr(f"{self.geoLoc}\n")
        stdscr.addstr(f"{self.temp}\n")
        stdscr.addstr(f"{self.tempSens}\n")
        stdscr.addstr(f"{self.moistureLVL}\n")
        stdscr.addstr(f"\nPress any key to continue...")
        k = stdscr.getch()
        stdscr.refresh()
        """<<<CODE HERE"""
        
    """FUNCTIONS"""

    def Scrape(self) -> str:
        self.temperature = self.soup.find('span', attrs={'data-testid':'TemperatureValue'})
        self.temperatureSensation = self.soup.find('span', attrs={'data-testid':'TemperatureValue'}, class_ = 'TodayDetailsCard--feelsLikeTempValue--Cf9Sl')
        self.humidity = self.soup.find('span', attrs={'data-testid':'PercentageValue'})
        self.geographicalLocation = self.soup.find('h1', class_ = 'CurrentConditions--location--kyTeL')
        
        prettyTemp = self.temperature.prettify()
        prettyTempSens = self.temperatureSensation.prettify()
        prettyHumidity = self.humidity.prettify()
        prettyGeoLoc = self.geographicalLocation.prettify()
        
        for i in prettyTemp:
            if i == '°':
                if prettyTemp[prettyTemp.index(i)-2] == '-': self.temp = f"The current temperature is: \
{prettyTemp[prettyTemp.index(i)-2]}{prettyTemp[prettyTemp.index(i)-1]}{i}C"
                else: self.temp = f"The temperature is: \
{prettyTemp[prettyTemp.index(i)-1]}{i}C"

        for i in prettyTempSens:
            if i == '°':
                if prettyTempSens[prettyTempSens.index(i)-3] == '-': self.tempSens = f"The current temperature sensation is: \
{prettyTempSens[prettyTempSens.index(i)-3]}{prettyTempSens[prettyTempSens.index(i)-2]}{prettyTempSens[prettyTempSens.index(i)-1]}{i}C"
                elif prettyTempSens[prettyTempSens.index(i)-2] == '-': self.tempSens = f"The current temperature sensation is: \
{prettyTempSens[prettyTempSens.index(i)-2]}{prettyTempSens[prettyTempSens.index(i)-1]}{i}C"
       
        for i in prettyHumidity:
            if i == '%': 
                if int(prettyHumidity[prettyHumidity.index(i)-3]) == 1: self.moistureLVL = f"The current humidity is: \
{prettyHumidity[prettyHumidity.index(i)-3]}{prettyHumidity[prettyHumidity.index(i)-2]}{prettyHumidity[prettyHumidity.index(i)-1]}{prettyHumidity[prettyHumidity.index(i)]}"
                elif isinstance(prettyHumidity[prettyHumidity.index(i)-3], None): self.moistureLVL = f"The current humidity is: \
{prettyHumidity[prettyHumidity.index(i)-2]}{prettyHumidity[prettyHumidity.index(i)-1]}{prettyHumidity[prettyHumidity.index(i)]}"
                elif isinstance(prettyHumidity[prettyHumidity.index(i)-2], None): self.moistureLVL = f"The humidity is: \
{prettyHumidity[prettyHumidity.index(i)-1]}{prettyHumidity[prettyHumidity.index(i)]}"

        for i in prettyGeoLoc:
            if i == '>':
                self.geoLoc = prettyGeoLoc[prettyGeoLoc.index(i)+2:prettyGeoLoc.index('/')-1]
        
        return (self.temp, self.tempSens, self.moistureLVL, self.geoLoc)
if __name__ == '__main__':
    sieve = sieveWeatherCom()
    sieve.Main()