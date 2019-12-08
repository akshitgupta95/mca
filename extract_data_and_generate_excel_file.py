#IMPORTANT: IF NEED BE, ADD SHEBANG LINE FOR POINTING TO THE CORRECT VERSION OF PYTHON

#IMPORTS
import os
import errno
import xlrd
import xlsxwriter 
import subprocess

#custom file for extracting performance parameters from generated files
#MUST BE PRESENT IN THE SAME DIRECTORY
import performance_extractor

#Parameter excel file filepath. The file name should be "CONFIGURATIONS.xls"
excel_filepath = ('CONFIGURATIONS.xls')

#configurations workbook, sheet
configurations_wb = xlrd.open_workbook(excel_filepath)
configurations_sheet = configurations_wb.sheet_by_index(0)
configurations_sheet.cell_value(0, 0) 

# Extracting number of rows 
number_of_configurations = configurations_sheet.nrows

#Keys corresponding to the parameters, to be replaced in the generated configuration file
replaceKeys = ['CONFIG_INDEX_NO', 'ISSUE_WIDTH', 'MEM_LOAD', 'MEM_STORE', 'MEM_PFT', 'NUM_ALU', 'NUM_MPY', 'NUM_MEMORY', 'NUM_GPR', 'NUM_BR']

dict_col_index = {'ISSUE_WIDTH' : 0 }

# Replace the keys in the template file with the "index" row's key values
def generate_configuration_file(index):
	# Read in the file
	with open('configuration_TEMPLATE.mm', 'r') as file :
		filedata = file.read()
	
	filedata_config = filedata
	
	for key in replaceKeys:
		filedata_config = filedata_config.replace(key, str(int(configurations_sheet.cell_value(i, dict_col_index[key]))))
	
	with open('configuration.mm', 'w') as file:
		file.write(filedata_config)

'''
currentDirectory = os.getcwd()
try:
	os.makedirs('configurations')
except OSError as exc: #The exception raised should only be a "directory exists" one
	if exc.errno != errno.EEXIST:
		raise
'''

#Keys corresponding to columns in the simulation result excel sheet
resultDict = {'CONFIG_INDEX_NO':0 , 'QSORT_EXEC_CYCLES':1, 'QSORT_TRACE1':2, 'CONV_EXEC_CYCLES':3, 'CONV_TRACE1':4 }

#Overwrites "PERF_RESULTS.xlsx" if it exists already, creates a new file otherwise
results_wb = xlsxwriter.Workbook('PERF_RESULTS.xlsx')
results_sheet = results_wb.add_worksheet()

#Create first row of the results excel sheet with the column headers
for key in resultDict:
	results_sheet.write(0, resultDict[key], key)

#For each row in the configuration excel sheet, copy the index nos to the results excel sheet to keep the index numbers consistent
for i in range(configurations_sheet.ncols):
	dict_col_index[configurations_sheet.cell_value(0,i)] = i

for i in range(1, number_of_configurations):
	#GENERATE CONFIGURATION FILE PER ROW OF THE "CONFIGURATIONS.xls" SHEET
	generate_configuration_file(i)
	
	#CALL BASH FILE TO SIMULATE ARCHITECTURE (qsort)
	subprocess.call('./RUNqsort.sh',shell=True)
	configuration_index = configurations_sheet.cell_value(i, dict_col_index['CONFIG_INDEX_NO'])
	results_sheet.write(i, resultDict['CONFIG_INDEX_NO'], configuration_index)

	#GET EXECUTION CYCLES COUNT FROM THE GENERATED FILES "ta.log.000" (qsort)
	qsort_exec_cycles = performance_extractor.get_execution_cycles_count('./output-qsort.c/ta.log.000')

	#GET TRACE 1'S INSTRUCTION COUNT (qsort)
	#ASSUMES THAT "pcntl.txt" HAS BEEN CREATED BY THE BASH FILE IN THE output DIRECTORY
	qsort_trace1_ilp = performance_extractor.get_trace_1_ilp_value('./output-qsort.c/pcntl.txt', 1)

	#WRITE RESULTS IN THE RESULTS EXCEL SHEET
	results_sheet.write(i, resultDict['QSORT_EXEC_CYCLES'], qsort_exec_cycles)
	results_sheet.write(i, resultDict['QSORT_TRACE1'], qsort_trace1_ilp)

	#CALL BASH FILE TO SIMULATE ARCHITECTURE (CONVOLUTION 5x5)
	subprocess.call('./RUNconv.sh',shell=True)

	#GET EXECUTION CYCLES COUNT FROM THE GENERATED FILES "ta.log.000" (CONVOLUTION 5x5)
	convolution5x5_exec_cycles = performance_extractor.get_execution_cycles_count('./output-convolution_5x5.c/ta.log.000')
	
	#GET TRACE 1'S INSTRUCTION COUNT (CONVOLUTION 5x5)
	#ASSUMES THAT "pcntl.txt" HAS BEEN CREATED BY THE BASH FILE IN THE output DIRECTORY	
	convolution5x5_trace1_ilp = performance_extractor.get_trace_1_ilp_value('./output-convolution_5x5.c/pcntl.txt', 3)
	
	#WRITE RESULTS IN THE RESULTS EXCEL SHEET
	results_sheet.write(i, resultDict['CONV_EXEC_CYCLES'], convolution5x5_exec_cycles)
	results_sheet.write(i, resultDict['CONV_TRACE1'], convolution5x5_trace1_ilp)

#CLOSE WORKBOOKS
configurations_wb.release_resources()
del configurations_wb
results_wb.close()
