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

        # Expected DataFrame Variable to hold Expected Data File
        self.Expected_DataFrame = None

        # VUT and FB DataFrame Variables to hold VUT and FB Data Files
        self.FB_DataFrame = None
        self.VUT_DataFrame = None

        # FB NaN Variables
        self.FB_Lat_NaN_Data = None
        self.FB_Lng_NaN_Data = None

        # VUT NaN Variables
        self.VUT_Lat_NaN_Data = None
        self.VUT_Lng_NaN_Data = None



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

        ''' file handling and Data isolation
        INPUT: None
        OUTPUT: None
        '''

        self.__FileData_Handling()
        try:
            self.DataFrame = pd.read_csv(self.FileleName , sep = ";" , skiprows = self.__Get_Headers_Length())

            # isolating the data of the file
            self.Expected_DataFrame = self.DataFrame.loc[:,"Name":"East[m]"]
            self.FB_DataFrame = self.DataFrame.loc[:,"Name.1":"DistanceFromOrigin[m]"]
            self.VUT_DataFrame = self.DataFrame.loc[:,"Name.2":]

            self.FB_Lat_NaN_Data = self.FB_DataFrame["Lat[wgs84].1"].isnull().sum()
            self.FB_Lng_NaN_Data = self.FB_DataFrame["Lng[wgs84].1"].isnull().sum()

            self.VUT_Lat_NaN_Data = self.VUT_DataFrame["Lat[wgs84].2"].isnull().sum()
            self.VUT_Lng_NaN_Data = self.VUT_DataFrame["Lng[wgs84].2"].isnull().sum()


        except:
            print("PLEASE Note THAT the FILE Might be Corrupted")



    def SHOW_VUT_NaN_Data(self):

        ''' Show VUT NaN Data
        INPUT: None
        OUTPUT: None
        '''
        print("VUT_Lat_NaN_Data = {}".format(self.VUT_Lat_NaN_Data))
        print("VUT_Lng_NaN_Data = {}".format(self.VUT_Lng_NaN_Data))
        print("\n")


    def SHOW_FB_NaN_Data(self):

        ''' Show FB NAN Data
        INPUT: None
        OUTPUT: None
        '''
        print("FB_Lat_NaN_Data = {}".format(self.FB_Lat_NaN_Data))
        print("FB_Lng_NaN_Data = {}".format(self.FB_Lng_NaN_Data))
        print("\n")


    def Get_NaN_Values(self,data_seg:str,column:str)-> int:

        ''' Show NaN Data in the given data Segment(VUT or FB) with the certain column and Show
            messages if inputs are wrong and also show some guides

        INPUT: data_seg:str -> either VUT or FB
               column:str -> data column in the data Segment

        OUTPUT: (int) Number of NaN Values in the passed data Segment
        '''
        data_seg = data_seg.upper()

        if (data_seg == "VUT"):

            if column in (self.VUT_DataFrame.columns):
                return self.VUT_DataFrame[column].isnull().sum()

            else:
                comment ="Wrong Column Name , Please Ckeck The Columns Names and Enter The Right Name\nFor The Right Name you Can use This line -> objectname.VUT_DataFrame.columns\n"
                print(comment)
                return -1

        elif (data_seg == "FB") :

            if column in (self.FB_DataFrame.columns):
                return self.FB_DataFrame[column].isnull().sum()
            else:

                comment ="Wrong Column Name , Please Ckeck The Columns Names and Enter The Right Name.\nFor The Right Name you Can use This line -> objectname.VUT_DataFrame.columns\n"
                print(comment)
                return -1

        else:
            print("Wrong Data Segment Name Please Enter The Right Name(VUT or FB)\n")
            return -1






# create object of type VUT_FileAnalysis
df = VUT_FileAnalysis("TRIAL_220616_110008_00401_FBl_26_AUTOSAVE.txt")
df.Read_CSV_File()


# check the Expected,FB & VUT Data
print(df.Expected_DataFrame.head())
print(df.VUT_DataFrame.head())
print(df.FB_DataFrame.head())

# test the Get_NaN_Values methods
data = df.Get_NaN_Values("fb","Lng[wgs84].1")
print(data)


# Number of NAN Values in the DataFrame of BOTH FB and VUT
df.SHOW_FB_NaN_Data()
df.SHOW_VUT_NaN_Data()


# PLOTING THE NaN Values in VUT and FB
VUTx = ["VUT Latitude","VUT Logitude"]
VUTy = [df.VUT_Lat_NaN_Data , df.VUT_Lng_NaN_Data]

FBx = ["FB Latitude","FB Logitude"]
FBy = [df.FB_Lat_NaN_Data,df.FB_Lng_NaN_Data]

plt.subplot(1,2,1)
plt.bar(VUTx,VUTy, color = 'red', edgecolor='black')
plt.title('NAN in VUT Data')

plt.subplot(1,2,2)
plt.bar(FBx,FBy,color = 'blue',edgecolor='black')
plt.title('NAN in FB Data')
plt.show()
