
# coding: utf-8

# In[11]:

from intelhex import IntelHex
import csv

class HexTruth: #Class which takes a dict or CSV file and converts it into an Intel Hex file for ROM burning.
    def __init__(self, csvFilename, loadDict = None, hexFilename=None ):
        if hexFilename is None: hexFilename = csvFilename.split(".")[0]+ ".hex"
        self.csvFilename = csvFilename
        self.hexFilename = hexFilename
        self.ih= IntelHex()
        self.hexDict = {};
        if loadDict is not None:
            self.hexDict = loadDict
            self.ih.fromdict(loadDict)
            self.writeFromIntelHex()
            
            
    def writeFromIntelHex(self): #Takes the IntelHex object and writes it to a hex file.
        f = open(self.hexFilename, 'w');
        self.ih.write_hex_file(f)
        f.close()
        print("Hex file generated.")
    
    def importCSV(self): #Opens a given csv filename and returns it's values as a list of lists.
        #list of lists = rows of columns
        self.csvTruth = []
        with open(self.csvFilename, newline='') as csvfile:
            csvReadingMachine = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvReadingMachine:
                self.csvTruth.append(row)
                if "#" in str(row):continue
                [addr, dat] = str(row).split("''")
                rangeIn = [0, addr.count(',') -1]
                if dat.count(",") is 1: rangeOut = [rangeIn[-1] + 2]
                else:rangeOut = [rangeIn[-1] + 2, rangeIn[-1] + 1 + dat.count(",")]

                binaryString = ""
                for j in range(rangeIn[0], rangeIn[-1] + 1):
                    binaryString+=str(row[j])
                #address = binaryString
                address = (int(binaryString,2))
                binaryString = ""
                for j in range(rangeOut[0], rangeOut[-1] + 1):
                    binaryString+=str(row[j])
                #data = binaryString; 
                data = (int(binaryString,2))
                #print(str(address) + ":" + str(data))
                self.hexDict[address] = data
            #print(row)
        return self.hexDict
    
   


# In[12]:

class TruthWriter:
    def __init__(self, dataSize = 8, signalSize = 8, selectorSize = 4):
        self.addressSize=signalSize+selectorSize
        self.dataSize = dataSize
        self.signalSize = signalSize;
        self.selectorSize = selectorSize;
    def genDict(self):
        logicDict = {}
        for i in range(0, 2**self.selectorSize):
            convertString = '{0:0' + str(self.selectorSize) + 'b}'
            selection = convertString.format(i)            
            for j in range(0, 2**self.signalSize):
                convertString = '{0:0' + str(self.signalSize) + 'b}'
                addrHalf = convertString.format(j)
                data = self.logicFunction(addrHalf, selection)
                #print(str(selection) +"|" + str(addrHalf) + " " + str(int(data,2)))
                #print(selection+addrHalf)
                logicDict[ int((selection+ addrHalf),2)] = int(data,2)
        return logicDict
    
    def logicFunction(self, addrHalf, selection):
        convertString = '{0:0' + str(self.dataSize) + 'b}'
        sansString = '{0:0' + str(self.dataSize-1) + 'b}'
        data = convertString.format(0)
        sansDataLength = sansString.format(0)
      
        if selection == "0000": #Means AND:
            allOnes = True
            for bit in addrHalf:
                if bit is not "1": allOnes = False;
            if allOnes: data = "1" + sansDataLength
                
        if selection == "0001": #Means OR:
            anyOnes = False
            for bit in addrHalf:
                if bit is "1": anyOnes = True
            if anyOnes: data = "1" + sansDataLength
            
        if selection == "0010": #Means Parity:
            numOne = addrHalf.count('1')
            if numOne%2 is 1: data = "1" + sansDataLength
                
        return data
      


# In[15]:

print("Welcome to HexTruther. Convert your CSV files to IntelHex. Please be sure you run this program in the same directory as the file you wish to convert.")
fileName = input("CSV filename? (press enter to autogenerate): ")
if fileName == "":
    endingName = input("Final Hex filename? (enter to leave same as CSV): ")
    if endingName == "": raise Exception("Hex filename left blank. Nowhere to write data. Please try again")
    tw = TruthWriter()
    tion = tw.genDict()
    print("Autogenerating Truthtable... ")
    tt = HexTruth(endingName, loadDict=tion)
else:  
    tt = HexTruth(fileName)
    hexDict = tt.importCSV()
    tt.ih.fromdict(hexDict)
    tt.writeFromIntelHex()




# In[ ]:



