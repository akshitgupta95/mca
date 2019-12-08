# README FOR THE MCA LAB1 FILES

This lab deals with performing simulations for various processor architecture configurations (pVEX). The simulations are performed on a Linux (openSUSE) VM.
The files below need to be present in the same directory as the .c files used for simulations.

## SOFTWARE REQUIRED
* python
* py packages ([pip](https://pypi.org/project/pip/) needs to be installed for this):
  * xlrd
  * xlsxwriter

* chmod needs to be performed on the bash files to allow them to execute
 
## COMPONENTS

### Excel file "CONFIGURATIONS.xls" containing the configuration parameters to run

An excel file needs to be present in the root directory, and should have exactly one "Sheet" with the following format:

CONFIG_INDEX_NO		ISSUE_WIDTH		MEM_LOAD		MEM_STORE		MEM_PFT		NUM_ALU		NUM_MPY		NUM_MEMORY		NUM_GPR		NUM_BR

The data in each column must correspond to the respective configuration's parameters.
CONFIG_INDEX_NO should be at (1, A).

### configuration_TEMPLATE.mm

Do not touch this file. It has text entries that are replaced based on the user's selected configurations in order to run architecture simulations.
The supporting .py files are used to replace the text where required.

### Python files

* extract_data_and_generate_excel_file.py - Reads the user's configurations from the Excel file, creates configuration.mm from the configuration_TEMPLATE.mm file, and runs a bash script for simulating that configuration for qsort.c. Repeats the step for convolution5x5.c. Extracts the simulation's results from the output directory and writes them to "PERF_RESULTS.xlsx" in the corresponding row. Repeats the process for every configuration.

* performance_extractor.py - Runs a regex match on the files "ta.log.000" and "pcntl.txt" in the simulation's output directories ("output-qsort.c/" and "output-convolution_5x5.c/") to obtain the values of "Execution Cycles" and trace 1's ILP.

### BASH scripts

These scripts run the commands needed for simulating the configurations specified through the configuration.mm file. The output of the pcntl command is written to "pnctl.txt" in the output directory of the generated files.

### PERF_RESULTS.xlsx

Contains the results of the simulations, more specifically the numbers for:
* Execution cycles
* Trace 1's ILP

