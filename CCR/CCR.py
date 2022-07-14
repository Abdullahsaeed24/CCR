#import needed tools
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math
import os
import glob
import shutil


FolderName = "Folder_Data.csv"
OldFolderName = None

class VUT_FileAnalysis:

    FB_FilesDataResult = {"FilePath":[],
            "%NaN":[],
            "NuberOfFrozen_Signal":[],
            "TimestampDrops":[],
            "MaxTimestampDrops":[],

            "JumpsInVelocity":[]}

    ALL_FB_FilesDataResult = {"FilePath":[],
            "%NaN":[],
            "NuberOfFrozen_Signal":[],
            "TimestampDrops":[],
            "MaxTimestampDrops":[],

            "JumpsInVelocity":[]}


    FB_FilesERRORS = {"FilePath":[],
            "Error":[],}



    File_Number = 0
    FilesDataResult = None
    ALLFilesDataResult = None
    ALLFilesErrors = None
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

        self.FB_RowsNum_Befor_drop = None
        self.VUT_RowsNum_Befor_drop = None


        # FB NaN Variables
        self.FB_Lat_NaN_Data = None
        self.FB_Lng_NaN_Data = None

        # VUT NaN Variables
        self.VUT_Lat_NaN_Data = None
        self.VUT_Lng_NaN_Data = None

        # FB Faild and Passed Data bassed on the velocity comparison
        self.FB_FaildData = None
        self.FB_PassedData = None

        # FB Faild and Passed Data counts
        self.FB_FaildData_Count = 0
        self.FB_PassedData_Count = 0

        self.TotalFrozenRecordsNumber = None
        self.NumberOfDrops = None
        self.MaxNumberOfDrops = None








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
            self.DataFrame = pd.read_csv(self.FileleName ,sep = ";" , skiprows = self.__Get_Headers_Length())

            # isolating the data of the file
            self.Expected_DataFrame = self.DataFrame.loc[:,"Name":"East[m]"]
            self.FB_DataFrame = self.DataFrame.loc[:,"Name.1":"DistanceFromOrigin[m]"]
            self.VUT_DataFrame = self.DataFrame.loc[:,"Name.2":]


            # delete the Information column in both VUT and FB DataFrame because it's entirly contain the NaN values so it's useless
            del(self.FB_DataFrame["Information.1"])
            del(self.VUT_DataFrame["Information.2"])

            # assign the rows number befor dropping data
            self.FB_RowsNum_Befor_drop = self.FB_DataFrame.shape[0]
            self.VUT_RowsNum_Befor_drop = self.VUT_DataFrame.shape[0]

            # assign the FB Latitude NaN Data and  FB Langitude NaN Data
            self.FB_Lat_NaN_Data = self.FB_DataFrame["Lat[wgs84].1"].isnull().sum()
            self.FB_Lng_NaN_Data = self.FB_DataFrame["Lng[wgs84].1"].isnull().sum()


            # assign the FB Latitude NaN Data and  FB Langitude NaN Data
            self.VUT_Lat_NaN_Data = self.VUT_DataFrame["Lat[wgs84].2"].isnull().sum()
            self.VUT_Lng_NaN_Data = self.VUT_DataFrame["Lng[wgs84].2"].isnull().sum()



            # delete the NaN values in the rest of coulmns - Delete the NaN data for all row
            self.FB_DataFrame.dropna(axis = 0,inplace = True)

            # reset the data index
            self.FB_DataFrame = self.FB_DataFrame.reset_index()

            # i did not remove the nan data because there are alot of columns have nan data and removing them cause remove all data
            self.VUT_DataFrame.fillna(method = 'backfill', axis = 0,inplace = True)


        except  Exception as e:

            VUT_FileAnalysis.FB_FilesERRORS["FilePath"].append(self.FileleName)
            VUT_FileAnalysis.FB_FilesERRORS["Error"].append(e)
            print("File Name is :",self.FileleName)
            print("PLEASE Note THAT the FILE Might be Corrupted ,{}".format(e))





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




    def __Calculate_Distance(self,**coordinates) -> float:

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

        E = coordinates["E2"] - coordinates["E1"]
        N = coordinates["N2"] - coordinates["N1"]

        Distance_square = pow(E,2) + pow(N,2)

        d = math.sqrt(Distance_square)

        return d # return d (m)



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





    def FB_Velocity_Assessment(self) -> None:

        ''' Calculate the distance , time diffrance between two points , velocity from point 1 to point 2
            and compare whether the velocity > 150 kilometer per hour or not if so assign its status as Failed otherwise Passed
            assign the calculated velocity in list called  ->> velocity_store
            asssign the status of the Velocity Assessment in list called ->> comparison_result
            INPUT: None
            OUTPUT: No return
        '''


        comparison_result = []
        velocity_store = []


        for x in range(0,self.FB_DataFrame.shape[0]-1,1): # 0 ---> FB_DataFrame.shape[0]-1

            # calculate the distance in meter
            distance  = self.__Calculate_Distance(E1 =self.FB_DataFrame["East[m].1"][x], E2 =self.FB_DataFrame["East[m].1"][x+1] , N1 =self.FB_DataFrame["North[m].1"][x] , N2 =self.FB_DataFrame["North[m].1"][x+1])
            # calculate the time in sec
            time = self.__Calculate_Time(t1 = self.FB_DataFrame["Timestamp[ms].1"][x] , t2 = self.FB_DataFrame["Timestamp[ms].1"][x+1])

            # calculate the velocity in m/h
            velocity = self.__Calculate_Velocity(d = distance , t = time)*0.001 # convert from m/h to km/h

            velocity_store.append(velocity)

            if velocity > 150 :
                comparison_result.append("Failed")


            else:
                comparison_result.append("Passed")


        comparison_result.append(comparison_result[-1])
        velocity_store.append(velocity_store[-1])

        # create a new coulmns in the FB DataFrame and assign the comparison_result list and velocity_store ti them
        self.FB_DataFrame["Velocity_Status"] = comparison_result
        self.FB_DataFrame["Velocity_"] = velocity_store

        # isolate the Faild Data and the Passed Data
        self.FB_FaildData = self.FB_DataFrame[self.FB_DataFrame["Velocity_Status"] == "Failed"]
        self.FB_PassedData = self.FB_DataFrame[self.FB_DataFrame["Velocity_Status"] == "Passed"]

        # assign the Faild Data  and  Passed Data Counts
        self.FB_FaildData_Count = self.FB_FaildData.shape[0]
        self.FB_PassedData_Count = self.FB_PassedData.shape[0]

    def Show_Failed_Velocity_Records(self) -> None:

        ''' show the failed velocity records
        INPUT: None
        OUTPUT: None
        '''
        print(self.FB_FaildData)



    def Show_Passed_Velocity_Records(self) -> None:

        ''' show the failed velocity records
        INPUT: None
        OUTPUT: None
        '''
        print(self.FB_PassedData)




    def FB_Frozen_DataRecords(self) -> None:
        '''
        INPUT:
        OUTPUT:
        '''

        TotalFreezingRecordsNumber = 0
        FreezingRecordsNumber = 1



        for x in range(0,len(self.FB_DataFrame["North[m].1"]),1): # 0 ---> 8


            if x < len(self.FB_DataFrame["North[m].1"])-1:

                if self.FB_DataFrame["North[m].1"][x] == self.FB_DataFrame["North[m].1"][x+1]:
                    FreezingRecordsNumber = FreezingRecordsNumber + 1
                    #print("FreezingRecordsNumber ",FreezingRecordsNumber)

                    if (x+1) == len(self.FB_DataFrame["North[m].1"])-1:

                        if FreezingRecordsNumber >= 5:
                            TotalFreezingRecordsNumber += FreezingRecordsNumber
                            FreezingRecordsNumber = 1
                            return TotalFreezingRecordsNumber




                else:

                    if FreezingRecordsNumber >= 3:

                        TotalFreezingRecordsNumber += FreezingRecordsNumber
                        FreezingRecordsNumber = 1
                        #print("\nTotalFreezingRecordsNumber ",TotalFreezingRecordsNumber,"--->",self.FB_DataFrame["North[m].1"][x],"\n")

                    else:
                        FreezingRecordsNumber = 1


        self.TotalFrozenRecordsNumber = TotalFreezingRecordsNumber
        #return TotalFreezingRecordsNumber





    def FB_TimeStamp_Drops(self):
        '''
        INPUT:
        OUTPUT:
        '''

        NumberOfDrops = 0
        MaxNumberOfDrops = 0
        TimeStampDiffrance = 0

        for x in range(0,len(self.FB_DataFrame["Timestamp[ms].1"]),1):

            # critical condition
            if (x+1) == (len(self.FB_DataFrame["Timestamp[ms].1"])-1):

                TimeStampDiffrance = self.FB_DataFrame["Timestamp[ms].1"][x+1] - self.FB_DataFrame["Timestamp[ms].1"][x]

                if TimeStampDiffrance > 10:
                    NumberOfDrops= NumberOfDrops + 1
                    #print("NumberOfDrops = ",NumberOfDrops)

                    if TimeStampDiffrance > MaxNumberOfDrops:
                        MaxNumberOfDrops = TimeStampDiffrance

                    else:
                        pass

                    #print("MaxNumberOfDrops = {}\nNumberOfDrops = {}".format(MaxNumberOfDrops,NumberOfDrops))
                    break


            # for safty
            elif (x+1) > (len(self.FB_DataFrame["Timestamp[ms].1"])-1):
                 break


            # if x+1 < len(self.FB_DataFrame["Timestamp[ms].1"])-1
            else:

                TimeStampDiffrance = self.FB_DataFrame["Timestamp[ms].1"][x+1] - self.FB_DataFrame["Timestamp[ms].1"][x]
                #print("TimeStampDiffrance = ",TimeStampDiffrance)
                if TimeStampDiffrance > 10:
                    NumberOfDrops= NumberOfDrops+1
                    #print("NumberOfDrops = ",NumberOfDrops)

                if TimeStampDiffrance > MaxNumberOfDrops:
                    MaxNumberOfDrops = TimeStampDiffrance

        #print("MaxNumberOfDrops = {}\nNumberOfDrops = {}".format(MaxNumberOfDrops,NumberOfDrops))

        self.NumberOfDrops = NumberOfDrops
        self.MaxNumberOfDrops = MaxNumberOfDrops





    def Collect_Facts(self):

        if VUT_FileAnalysis.File_Number == 0:

            VUT_FileAnalysis.FB_FilesDataResult = {"FilePath":[],
                    "%NaN":[],
                    "NuberOfFrozen_Signal":[],
                    "TimestampDrops":[],
                    "MaxTimestampDrops":[],

                    "JumpsInVelocity":[]}

        else:
            pass


        # assign file name
        VUT_FileAnalysis.FB_FilesDataResult["FilePath"].append(self.FileleName)
        VUT_FileAnalysis.ALL_FB_FilesDataResult["FilePath"].append(self.FileleName)

        # assign % of NaN data in the FB data

        if self.FB_Lat_NaN_Data > self.FB_Lng_NaN_Data:
            FB_NAN = self.FB_Lat_NaN_Data

        elif self.FB_Lat_NaN_Data < self.FB_Lng_NaN_Data:
            FB_NAN = self.FB_Lng_NaN_Data

        # this mean that they are equal to each
        else:
            FB_NAN = self.FB_Lat_NaN_Data


        FB_NAN = ( FB_NAN /self.FB_RowsNum_Befor_drop)* 100
        VUT_FileAnalysis.FB_FilesDataResult["%NaN"].append(FB_NAN)
        VUT_FileAnalysis.ALL_FB_FilesDataResult["%NaN"].append(FB_NAN)

        # assign number of frozen data
        self.FB_Frozen_DataRecords()

        VUT_FileAnalysis.FB_FilesDataResult["NuberOfFrozen_Signal"].append(self.TotalFrozenRecordsNumber)
        VUT_FileAnalysis.ALL_FB_FilesDataResult["NuberOfFrozen_Signal"].append(self.TotalFrozenRecordsNumber)

        # assign number of drops
        self.FB_TimeStamp_Drops();

        VUT_FileAnalysis.FB_FilesDataResult["TimestampDrops"].append(self.NumberOfDrops)
        VUT_FileAnalysis.ALL_FB_FilesDataResult["TimestampDrops"].append(self.NumberOfDrops)

        VUT_FileAnalysis.FB_FilesDataResult["MaxTimestampDrops"].append(self.MaxNumberOfDrops)
        VUT_FileAnalysis.ALL_FB_FilesDataResult["MaxTimestampDrops"].append(self.MaxNumberOfDrops)

        # assign number jumps in velocity
        self.FB_Velocity_Assessment()
        VUT_FileAnalysis.FB_FilesDataResult["JumpsInVelocity"].append(self.FB_FaildData_Count)
        VUT_FileAnalysis.ALL_FB_FilesDataResult["JumpsInVelocity"].append(self.FB_FaildData_Count)
        #----------------------------------------------------------------------------------------------------


        VUT_FileAnalysis.File_Number = self.File_Number+1





#********************************************************************************************************************************#
#*--------------------------------------------------- Trial_Files_Processing ----------------------------------------------------#
#********************************************************************************************************************************#


def Trial_Files_Processing(FolderPath:str)-> None:


    """process the TRIAL_files and store the result in DataFrame then convert the DataFrame to csv file and store it in FolderPath
       the file content after processing as following:
                        FilePath                      %NaN        NuberOfFrozen_Signal       TimestampDrops    MaxTimestampDrops      JumpsInVelocity
             ********--FileNPath--*********           6.9807             80                          20                 12                   10
       INPUT: FolderPath the folder directory
       OUTPUT: None -->  No return values but there is CSV File written in the directory
    """


    # Collect all TRIAL Files in the FolderPath and store them in TRIAL_files (Files Names)
    try:
        TRIAL_files = glob.glob(os.path.join(FolderPath, "*.TRIAL"))
    except:
        pass


    # define DataFrame Variable
    DataFrame = None

    try:
        # loop over the list of TRIAL_files Names
        for file in TRIAL_files:

            # create VUT_FileAnalysis object to process the passed file
            DataFrame = VUT_FileAnalysis(file)
            DataFrame.Read_CSV_File()
            DataFrame.Collect_Facts()

            # NOTE: VUT_FileAnalysis.FB_FilesDataFrame and VUT_FileAnalysis.FB_FilesDataResult are class Variables which mean they are shared between all class instances
            # Convert the VUT_FileAnalysis.FB_FilesDataResult dictionary into VUT_FileAnalysis.FB_FilesDataFrame DataFrame
            VUT_FileAnalysis.FilesDataResult = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in VUT_FileAnalysis.FB_FilesDataResult.items() ]))
            #VUT_FileAnalysis.FB_FilesDataFrame = pd.DataFrame(VUT_FileAnalysis.FB_FilesDataResult)

    except:
        pass


    if(os.path.exists(FolderPath+"\FolderResult.csv") and os.path.isfile(FolderPath+"\FolderResult.csv")):
        os.remove(FolderPath+"\FolderResult.csv")
    # Exception

    try:
        # convert the DataFrame to CSV File
        VUT_FileAnalysis.FilesDataResult.to_csv("Folder_Data.csv")
        # asssign "Folder_Data.csv" file directory to original
        original = r"C:\Users\aismail2\Documents\GitHub\CCR\CCR\Folder_Data.csv"
        # assign the FolderPath to target Variable to move the csv file from script directory to FolderPath
        target = FolderPath+"\FolderResult.csv"
        # move the csv file from script directory to FolderPath
        shutil.move(original, target)

    except:
        print("There is an Error")


    # clear the dictionary to make it ready to another folder data
    VUT_FileAnalysis.FB_FilesDataResult.clear()

    # reset the Files_Number Variable
    VUT_FileAnalysis.File_Number=0

    # reset the data DataFrame Variable
    VUT_FileAnalysis.FilesDataResult = None





rootdir = r"C:\Users\aismail2\Downloads\4a_nasta-20220627T102722Z-001\4a_nasta"
dirlist = []
for rootdir, dirs, files in os.walk(rootdir):
    for subdir in dirs:
        print(os.path.join(rootdir, subdir))
        dirlist.append(os.path.join(rootdir, subdir))



for x in dirlist:
    Trial_Files_Processing(x)


if(os.path.exists("Folder_Data.csv") and os.path.isfile("Folder_Data.csv")):
    os.remove("Folder_Data.csv")

if(os.path.exists("FolderData.csv") and os.path.isfile("FolderData.csv")):
    os.remove("FolderData.csv")
    print("file deleted")

VUT_FileAnalysis.ALL_FB_FilesDataFrame = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in VUT_FileAnalysis.ALL_FB_FilesDataResult.items() ]))
print(VUT_FileAnalysis.ALL_FB_FilesDataFrame)



try:

    if(FolderName == "Folder_Data.csv"):
        OldFolderName = "Folder_Data.csv"
        if(os.path.exists("Folder_Data.csv") and os.path.isfile("Folder_Data.csv")):
            os.remove("Folder_Data.csv")
        FolderName = "FolderData.csv"

    else:
        if(os.path.exists("FolderData.csv") and os.path.isfile("FolderData.csv")):
            os.remove("FolderData.csv")
        FolderName = "FolderData.csv"

    # convert the DataFrame to CSV File
    VUT_FileAnalysis.ALL_FB_FilesDataFrame.to_csv(FolderName)


except:
    print("delete error")
    pass


VUT_FileAnalysis.ALLFilesErrors = pd.DataFrame( VUT_FileAnalysis.FB_FilesERRORS)
print(VUT_FileAnalysis.ALLFilesErrors)
VUT_FileAnalysis.FB_FilesERRORS = {"FilePath":[],
            "Error":[],}

if(os.path.exists("FILES_ERRORS.csv") and os.path.isfile("FILES_ERRORS.csv")):
    os.remove("FILES_ERRORS.csv")
try:
    VUT_FileAnalysis.ALLFilesErrors.to_csv("FILES_ERRORS.csv")
except:
    pass




def main():
    pass
# construct interactive program ,all u need to pass the file name with respecting the file should be at the same program directory
if __name__ == "__main__":
	main()





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
