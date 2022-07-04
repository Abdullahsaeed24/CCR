#import needed tools
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math
import random
import colorama
from colorama import Fore





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

            #self.FB_DataFrame.fillna(method = 'backfill', axis = 0)
            #self.VUT_DataFrame.fillna(method = 'backfill', axis = 0)

            # delete the Information column in both VUT and FB DataFrame because it's entirly contain the NaN values so it's useless
            del(self.FB_DataFrame["Information.1"])
            del(self.VUT_DataFrame["Information.2"])

            # delete the NaN values in the rest of coulmns
            self.FB_DataFrame.dropna(axis = 0,inplace = True)
            #self.VUT_DataFrame.dropna(axis = 0,inplace = True)
            self.VUT_DataFrame.fillna(method = 'backfill', axis = 0,inplace = True)


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




    def __Calculate_Distance(self,**parameter) -> float:

        ''' Calculate the distance based on given parameters
        E -> East  (m)
        N -> North (m)

        (E1,N1) , (E2,N2)
        D^2 = (E2 - E1)^2 + (N2 - N1)^2
        d = sqrt(D^2)

        INPUT: Location N coordinates (E1 , N1)
               Location N+1 coordinates (E2 , N2)

        OUTPUT: return Distance  in meters
        '''

        Distance_square =  pow((parameter["E2"] - parameter["E1"]),2) + pow((parameter["N2"] - parameter["N1"]),2)
        return math.sqrt(Distance_square) # return d



    def __Calculate_Time(self ,**timestamp) -> float:

        ''' Calculate the time based on given parameters

        t1 -> time at Location 1 coordinates time in msec
        t2 -> time at Location 2 coordinates time in msec

        INPUT: t1 , t2

        OUTPUT: return time diffrance between t2-t1 in sec
        '''
        time  =  abs(timestamp['t2'] - timestamp['t1']) / 1000 # time convertion from msec into sec

        return time # time in sec




    def __Calculate_Velocity(self , **data) -> float:

        ''' Calculate the Velocity , Velocity should be in m/h (meter per hours)

        INPUT: d -> distance
               t -> time

        OUTPUT: return Velocity

        '''
        return (data['d'] / data['t']) * 3600  # convertion from m/sec into m/h



    def compare_velocity(self):

        for x in range(0,self.FB_DataFrame.shape[0]): # from  0  ----> shape[0] - 1   3460 -1

            if (x+1) == (self.FB_DataFrame.shape[0]-1):
                distance = self.__Calculate_Distance(E1 =self.FB_DataFrame["East[m].1"][x] , E2 =self.FB_DataFrame["East[m].1"][x+1] , N1 =self.FB_DataFrame["North[m].1"][x]  , N2 =self.FB_DataFrame["North[m].1"][x+1] )













# create object of type VUT_FileAnalysis
df = VUT_FileAnalysis("TRIAL_220616_110008_00401_FBl_26_AUTOSAVE.txt")
df.Read_CSV_File()

print(df.VUT_DataFrame.head())
print(df.FB_DataFrame)

print(df.VUT_DataFrame.isnull().sum() )
print(df.FB_DataFrame.isnull().sum())
print(df.FB_DataFrame)

d= []

d.append(d)

print(d )


print(len(df.FB_DataFrame["East[m].1"]))
print(df.FB_DataFrame.shape)
df.FB_DataFrame.to_csv("FB.csv")

#plt.hist(df.FB_DataFrame["North[m].1"],bins = 2000)
#plt.show()
'''
plt.subplot(1,2,1)
df.FB_DataFrame.boxplot("North[m].1")

plt.subplot(1,2,2)
df.FB_DataFrame.boxplot("East[m].1")
plt.show()
'''


'''
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
'''
