import pandas
import re
import sys
import csv



            
class UnexpectedArgumentError(Exception):
    
    
    def __init__(self, message=''):
        if len(message)>0:
            self.message = \
            """Expecting arguments to be dictionaries, 
            eg: CSVOperation({'name': 'FileName', 'separator':','}, {'name': 'AnotherFileName', 'separator':'\t'})"""        
        else:
            self.message = message
        
        super(UnexpectedArgumentError, self).__init__(self.message)
        
        
    
class MergeError(Exception):
    
    
    def __init__(self, message=''):
        self.message = message
        super(MergeError, self).__init__(self.message)
        


class CSVOperation(object):
    
    
    def __init__(self, *args):
        self.CSVFile = {}
        if len(args) == 0:
            raise UnexpectedArgumentError
        else:
            self.readCSV(args)

    
    def readCSV(self, filenames):
        if(len(filenames)==1):
            self.CSVFile = dict(pandas.read_csv(filenames['name'], sep=filenames['separator']))
        else:
            self.read_files = [] #will contain pandas data frames
            for f in filenames: 
                    if type(f) != type({}):
                        raise UnexpectedArgumentError
                    self.read_files.append(pandas.read_csv(f['name'], sep=f['separator']))
                
    
    def mergeCSV(self):
        titles = []
        unique_keys = set([])
        merged = {}
        for file in self.read_files:
            titles.append(set(file.keys()))
            
        for title in titles:
            unique_keys = unique_keys.union(title)
        unique_keys = list(unique_keys)
        
        for key in unique_keys:
            for f in self.read_files:
                fl = dict(f)
                if fl.__contains__(key):
                    if merged.__contains__(key):
                        merged[key].extend(list(fl[key]))
                    else:
                        merged[key] = list(fl[key])       
        self.CSVFile =  merged
        
        
    def findDifference(self, column_name):
        differences = []
        ips = []
        CSVFiles = [ dict(i) for i in self.read_files  ]
        for file in CSVFiles:
            ips.append(list(file[column_name]))           
            
            
        
    
    
    def filterDuplicates(self, file, column_name=''):
        csvfile = pandas.read_csv(file["name"], sep=file["separator"], header=0)
        csvfile.to_csv("test_merged.csv")
        #csvfile = csvfile.drop_duplicates(subset=[column_name])
        
        #df.to_csv("%s_filtered.csv"%(file["name"]))

    def saveCSV(self, filename):
        header = self.CSVFile.keys()
        rows = []
        for key,value in self.CSVFile.items():
            rows.append(value)
        rows = list(map(list, zip(*rows)))
        CSVData = []
        CSVData.append(header)
        CSVData.extend(rows)
        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(CSVData)




    
        
        
Operation = CSVOperation({'name': '1.csv', 'separator':'\t'}, {'name': '2.csv', 'separator':'\t'})

f = Operation.read_files

mgd = Operation.mergeCSV()

f0 = dict(f[0])

Operation.mergeCSV()

saved = Operation.saveCSV("merged.csv")

Filtered = Operation.filterDuplicates(file={"name": "merged.csv", "separator": ","}, column_name="Internal IP Address")
                

            


            
            
        
            
