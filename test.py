from main import CSVOperation

Operation = CSVOperation({'name': '1.csv', 'separator':'\t'}, {'name': '2.csv', 'separator':'\t'})

f = Operation.read_files

mgd = Operation.mergeCSV()

f0 = dict(f[0])

Operation.mergeCSV()

saved = Operation.saveCSV("merged.csv")

Filtered = Operation.filterDuplicates(file={"name": "merged.csv", "separator": ","}, column_name="Internal IP Address")