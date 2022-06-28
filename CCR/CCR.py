#import needed tools
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import random





class VUT_FileAnalysis:

    def __init__(self,FileleName:"str",TestData:list) -> None:

        ''' class instance Constractor
        INPUT: FileleName --> the file name
        OUTPUT: NO return
        '''
        self.FileleName = FileleName
        self.TestData = TestData
        self.NewFileName ="FileAnalysis"


    def FileData_Handling(self)->str:
        ''' handling and adjusting the file -> isolate the Not Flat file data and handling the semicolon seperated data
        INPUT: No INPUT
        OUTPUT: NO return
        '''
        self.TestData = []

        # isolate the Test Data and assign it into TestData list
        with open(self.FileleName) as f:
            for line in f:
                l = line.strip()
                if l == "END_OF_HEADER":
                    break
                else:
                    self.TestData.append(l)



        self.NewFileName ="FileAnalysis"+self.FileleName
        file = open(self.NewFileName,"w")

        with open(self.FileleName) as f:
            for line in f:
                l = line.strip()

                if (l in self.TestData):
                    continue

                else:
                    if l != "END_OF_HEADER":
                        file.write(line)
        file.close()
        return self.NewFileName


    def Get_TestData(self) -> list:
        return self.TestData


'''
TestData = []

with open("TRIAL_220616_110008_00401_FBl_26_AUTOSAVE.txt") as f:
    for line in f:
        l = line.strip()
        if l == "END_OF_HEADER":
            break
        else:
            TestData.append(l)


file = open("trail_220616_110008_00401_FBl_26_AUTOSAVE.txt","w")

with open("TRIAL_220616_110008_00401_FBl_26_AUTOSAVE.txt") as f:
    for line in f:
        l = line.strip()
        if (l in TestData):
            continue
        else:
            if l != "END_OF_HEADER":
                file.write(line)
file.close()


df = pd.read_csv("trail_220616_110008_00401_FBl_26_AUTOSAVE.txt",sep=";")

print(df.head())
'''

vut = VUT_FileAnalysis("TRIAL_220616_110008_00401_FBl_26_AUTOSAVE.txt",[])
file = vut.FileData_Handling()
df = pd.read_csv(file,sep=";", skiprows=)
print(df.head())
