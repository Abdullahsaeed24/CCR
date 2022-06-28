#import needed tools
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import random





class VUT_FileAnalysis:

    def __init__(self,FileleName:"str") -> None:

        ''' class instance Constractor
        INPUT: FileleName --> the file name
        OUTPUT: NO return
        '''
        self.FileleName = FileleName
        self.TestData = []
        self.DataFrame = None


    # privite method
    def __FileData_Handling(self)->str:

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


    # privite method
    def __Get_Headers_Length(self) -> None:

        ''' GET the headers number in the insertes file -> the headers number is not the entire number its just the just the first N
            HEADERS befor the the semicolon seperated Data
        INPUT: No INPUT
        OUTPUT: NO return
        '''
        self.__FileData_Handling()
        return len(self.TestData)+1



    def Get_Test_Headers(self) -> list:
        ''' GET the first N headers of the file
        INPUT: None
        OUTPUT: return list with the headers
        '''
        self.__FileData_Handling()
        return self.TestData


    def Read_CSV_File (self) -> None:

        self.__FileData_Handling()
        try:
            self.DataFrame = pd.read_csv(self.FileleName , sep = ";" , skiprows = self.__Get_Headers_Length())
        except:
            print("PLEASE Note THAT the FILE Might be Corrupted")



'''
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
'''






df = VUT_FileAnalysis("TRIAL_220616_110008_00401_FBl_26_AUTOSAVE.txt")
df.Read_CSV_File()
print(df.DataFrame.head())
print(df.DataFrame.describe())
