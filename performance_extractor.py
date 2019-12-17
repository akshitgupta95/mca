import re

#REGEX FOR MATCHING THE EXPRESSION FOR EXECUTION CYCLE COUNT
exec_cycle_regex = re.compile('Execution Cycles: (\s+)(\d+) \((.*)\)\n')

#REGEX FOR EXTRACTING TRACE 1's ILP DATA FROM THE TABLE'S ROWS
instruction_regex = re.compile('(\s+)1(\s+)(\d+).(\d+) (\s+)(\d+)(\s+)(\s+)(\d+)(\s+)(\d+)(\s+)(\d+)\n')

# OPEN THE FILE 'ta.log.000' AND MATCH STRINGS USING REGEX, LINE BY LINE
# IF A MATCH IS FOUND, WE'VE RETRIEVED THE NUMBER OF EXEC CYCLES
def get_execution_cycles_count(filepath='ta.log.000'):
    with open(filepath, 'r') as file:
        line = file.readline()
        while line:
            if exec_cycle_regex.match(line):
                exec_cycles_num = int(exec_cycle_regex.match(line).group(2))
                return exec_cycles_num

            line = file.readline()

#OPEN THE GENERATED FILE "pcntl.txt" AND ITERATE THROUGH ITS LINES
#THE SECOND COLUMN IN THE ROW CORRESPONDING TO TRACE 1 IS THE REQUIRED VALUE
#HACKHACK: WE KNOW THERE ARE A CERTAIN NUMBER OF TABLES IN THE GENERATED FILE, AND HENCE THE COUNT COMPARISON
#TO GET THE ROW FROM THAT TABLE
def get_trace_1_ilp_value(filepath='pcntl.txt', countCheck=1):
    with open(filepath, 'r') as file:
        line = file.readline()
        count = 0
        while line:
            if instruction_regex.match(line):
                count += 1
                if (count==countCheck):
                    ilp_value = float(instruction_regex.match(line).group(3) + str('.') + instruction_regex.match(line).group(4))
                    return ilp_value

            line = file.readline()