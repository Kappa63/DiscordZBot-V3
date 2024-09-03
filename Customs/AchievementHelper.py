from typing import List
import numpy as np
    
class GeneralAchievements:
    def __init__(self, acq:List[int]) -> None:
        self.achieved = acq
    
    def addAchieved(self, id:int) -> None:
        if id not in self.achieved:
            self.achieved.append(id)
    
    def getAchieved(self) -> List[int]:
        return self.achieved