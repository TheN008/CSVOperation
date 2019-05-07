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
        self.filtered_files = []
        if len(args) == 0:
            raise UnexpectedArgumentError
        else:
            self.readCSV(args)
            self.FILENAMES = args 

    
    def readCSV(self, filenames):
        if(len(filenames)==1):
            self.CSVFile = dict(pandas.read_csv(filenames['name'], sep=filenames['separator']))
        else:
            self.read_files = [] #will contain pandas data frames
            for f in filenames: 
                    if type(f) != type({}):
                        raise UnexpectedArgumentError
                    self.read_files.append(pandas.read_csv(f['name'], sep=f['separator']))
        return self.read_files
                
    
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
        
        
    def findDifference(self, column_name, file_prefix):
        columnData = []
        difference = []
        required_rows = []
        index_data = []
        for a_file in self.read_files:
            column = a_file[column_name]
            columnData.append(list(column))

        for i in columnData:
            for j in columnData:
                if i == j:
                    continue
                else:
                    difference.append( list(  set(i).difference(set(j))  ) )

        for current_file, column_data in enumerate(columnData):
            required_row = []
            current_difference = difference[current_file]
            for different_value in current_difference:
                for index, column_value in enumerate(column_data):
                    if different_value == column_value:
                        required_row.append(index)
            required_rows.append(required_row)
        
        for count, fl in enumerate(self.read_files):
            required_row_numbers = required_rows[count]
            r = [i for i in range(max(required_row_numbers)) if i not in required_row_numbers]     
            fl = fl.drop(fl.index[r])
            fl.to_csv("{0}_{1}.csv".format(file_prefix, count+1), sep="\t") 

            
                    
    def findIntersection(self, column_name):
        columns = []
        dfs = []
        for count, fl in enumerate(self.read_files):
            columns.append(fl[column_name])
        columns = set.intersection(*map(set,columns))

        for count, f in enumerate(self.read_files):
            dfs.append( f.loc[ f[column_name].isin(columns) ] )
            dfs[count].drop_duplicates(subset=[column_name], keep='first', inplace=True)

        dfs = pandas.concat(dfs, ignore_index=True)

        dfs.drop_duplicates(subset=[column_name], keep='first')
        
        return dfs.drop_duplicates(subset=[column_name], keep='first').to_csv("1n2.csv", sep='\t')
          
                    
            
                   


    
    def filterDuplicates(self, file, column_name=''):
        csvfile = pandas.read_csv(file["name"], sep=file["separator"], header=0)
        csvfile = csvfile.drop_duplicates(subset=[column_name])
        self.filtered_files.append("%s_filtered.csv"%file["name"])
        csvfile.to_csv(self.filtered_files, sep='\t')
        
        
        

    def getOnly(self, column_name):
        intersecting_columns = []
        onlyData = []
        for count, fl in enumerate(self.read_files):
            intersecting_columns.append(fl[column_name])
        intersecting_columns = list(set.intersection(*map(set,intersecting_columns)))
        for fl in self.read_files:
            fl.loc[ fl[column_name].isin(intersecting_columns) ]
        
        for count, f in enumerate(self.read_files):
            onlyData.append( f[ ~f[column_name].isin(intersecting_columns) ] )
            onlyData[count].to_csv("only-%d"%count+1, sep="\t") 
        return onlyData


    def saveCSV(self, filename, dict = {}):
        header = self.CSVFile.keys()
        rows = []
        for key,value in self.CSVFile.items():
            rows.append(value)
        rows = list(map(list, zip(*rows)))
        CSVData = []
        CSVData.append(header)
        CSVData.extend(rows)
        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter="\t")
            writer.writerows(CSVData)

    
    
# change this


Operation = CSVOperation({'name': '1.csv', 'separator':','}, {'name': '2.csv', 'separator':','})

col_name = " Lastname"



print(Operation.getOnly(col_name))



            
            
        
            

