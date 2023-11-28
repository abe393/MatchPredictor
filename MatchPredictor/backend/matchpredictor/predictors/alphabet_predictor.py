from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Prediction, Predictor
import itertools

class AlphabetPredictor(Predictor):
    def predict(self, fixture: Fixture) -> Prediction:
        #We should strip spaces in the case of bayern lever vs bayer munich 
        homeTeamName = (fixture.home_team.name).replace(" ","")
        awayTeamName = (fixture.away_team.name).replace(" ","")
        """edge cases to consider what if awayTeam has a smaller Team name like what if Milanese(HOME) vs Milan which in that case the shorter 
        word would be first alphabetically should we put it in a try exception block? if the exception runs due to out of bounds we just return the away
        team ? thats messy we can just run a check in the for loop"""
        for i in range(len(homeTeamName)):
            if (i + 1) > len(awayTeamName):
                return Prediction(Outcome.AWAY)
            if homeTeamName[i] > awayTeamName[i]:
                return Prediction(outcome=Outcome.AWAY)
            if homeTeamName[i] < awayTeamName[i]:
                return Prediction(outcome=Outcome.HOME)
        #if the for loop runs through then the same team played itself so it would be a draw.  
        return Prediction(outcome=Outcome.DRAW)