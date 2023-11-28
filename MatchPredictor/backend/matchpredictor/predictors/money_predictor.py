from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Prediction, Predictor
import itertools
import requests 
import json
import os
class MoneyPredictor(Predictor):
    def WriteToJson(self,File,TeamName,Value):
        with open(File,'r+') as file:
            file_data = json.load(file)
            file_data[TeamName] = Value
            file.seek(0)
            json.dump(file_data, file, indent = 4)

    def CheckIfCached(self,TeamName):
        with open(r"DataFiles/TeamData.json") as json_data:
            data = json.load(json_data)
        if TeamName in data.keys():
            return(data[TeamName])
        else:
            return False
        
    def getTeamValue(self,TeamName):
        desc= self.CheckIfCached(TeamName=TeamName)
        if desc == False:
            url = f"https://transfermarkt-api.vercel.app/clubs/search/{TeamName}?page_number=1"
            resp = requests.get(url).json()
            try:
                value=resp["results"][0]['marketValue']
            except:
                value="1k"
            value=self.ConvertValuesToInt(value)
            self.WriteToJson(r"DataFiles/TeamData.json",TeamName,value)
            return value
        return desc
    def ConvertValuesToInt(self, value):
        value=value.replace("€","")
        #possible suffixes M,K,bn
        value= value.replace(" ","")
        if "bn" in value:
            multi = 1000000000
        if "m" in value:
            multi = 1000000
        if "k" in value:
            multi = 1000
        value=value.replace("bn","")
        value = value.replace("m","")
        value= value.replace("k","")
        value=float(value)
        return(value*multi)
        

    def predict(self, fixture: Fixture) -> Prediction:
        #print(os.getcwd())
        homeVal=self.getTeamValue(fixture.home_team.name)
        awayVal=self.getTeamValue(fixture.away_team.name)
        diff = abs(homeVal - awayVal)
        #print(diff,homeVal,awayVal)
        if (diff/homeVal) > 5 and (diff/awayVal) > 5:
            return Prediction(outcome= Outcome.DRAW)
        if homeVal > awayVal:
            return Prediction(outcome = Outcome.HOME)
        else:
            return Prediction(outcome=Outcome.AWAY)
