import re

def parse(filepath):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file to be parsed

    Returns
    -------
    data : array of parsed data + total area

    """
    # DEFINED AREAS
    area_alu = 3273
    area_mult = 40614
    area_lwsw = 1500
    area_64gpr = 26388
    area_8br = 258
    area_misc = 6739
    total_area = 0

    # VARIABLES NEEDED FOR CALCULATION OF AREA
    issue_width = 0
    res_mem_load = 0
    res_mem_store = 0
    res_mem_pft = 0
    res_issue_width = 0
    res_alu = 0
    res_mpy = 0
    res_memory = 0
    reg_r0 = 0
    reg_b0 = 0

    data = []

    # OPEN THE CONFIGURATION FILE AND MATCH STRINGS USING REGEX, LINE BY LINE
    # ALSO UPDATE THE ABOVE VARIABLES WITH THE CORRECT VALUES
    with open(filepath, 'r') as file:
        line = file.readline()
        while line:
            reg_match = _RegExLib(line)

            if reg_match.issue_width:
            	issue_width = int(reg_match.issue_width.group(2))
                data.append(issue_width)

            if reg_match.res_mem_load:
            	res_mem_load = int(reg_match.res_mem_load.group(2))
                data.append(res_mem_load)

            if reg_match.res_mem_store:
            	res_mem_store = int(reg_match.res_mem_store.group(2))
                data.append(res_mem_store)

            if reg_match.res_mem_pft:
            	res_mem_pft = int(reg_match.res_mem_pft.group(2))
                data.append(res_mem_pft)

            if reg_match.res_issue_width:
            	res_issue_width = int(reg_match.res_issue_width.group(2))
                data.append(res_issue_width)

            if reg_match.res_alu:
            	res_alu = int(reg_match.res_alu.group(2))
                data.append(res_alu)

            if reg_match.res_mpy:
            	res_mpy = int(reg_match.res_mpy.group(2))
                data.append(res_mpy)

            if reg_match.res_memory:
            	res_memory = int(reg_match.res_memory.group(2))
                data.append(res_memory)

            if reg_match.reg_r0:
            	reg_r0 = int(reg_match.reg_r0.group(2))
                data.append(reg_r0)

            if reg_match.reg_b0:
            	reg_b0 = int(reg_match.reg_b0.group(2))
                data.append(reg_b0)

            line = file.readline()

    # INDIVIDUAL AREA CALCULATION
    area_agr = (area_64gpr/64)*reg_r0*issue_width*issue_width/16
    area_multiplication = area_mult*res_mpy
    area_load_store = area_lwsw*res_memory
    area_arith_lu = area_alu*res_alu
    area_br = (area_8br/8)*reg_b0 

    # TOTAL AREA CALCULATION
    total_area = area_agr + area_multiplication + area_load_store + area_arith_lu + area_br
    data.append(total_area)
    return data


class _RegExLib:
    """Set up regular expressions"""
    # use https://regexper.com to visualise these if required
    _reg_issue_width = re.compile('RES: IssueWidth(\s+)(\d+)\n')
    _reg_res_mem_load = re.compile('RES: MemLoad(\s+)(\d+)\n')
    _reg_res_mem_store = re.compile('RES: MemStore(\s+)(\d+)\n')
    _reg_res_mem_pft = re.compile('RES: MemPft(\s+)(\d+)\n')
    _reg_res_issue_width = re.compile('RES: IssueWidth.0(\s+)(\d+)\n')
    _reg_res_alu = re.compile('RES: Alu.0(\s+)(\d+)\n')
    _reg_res_mpy = re.compile('RES: Mpy.0(\s+)(\d+)\n')
    _reg_res_memory = re.compile('RES: Memory.0(\s+)(\d+)\n')
    _reg_reg_r0 = re.compile('REG: \$r0(\s+)(\d+)\n')
    _reg_reg_b0 = re.compile('REG: \$b0(\s+)(\d+)\n')

    def __init__(self, line):
        # check whether line has a positive match with all of the regular expressions
        self.issue_width = self._reg_issue_width.match(line)
        self.res_mem_load = self._reg_res_mem_load.match(line)
        self.res_mem_store = self._reg_res_mem_store.match(line)
        self.res_mem_pft = self._reg_res_mem_pft.match(line)
        self.res_issue_width = self._reg_res_issue_width.match(line)
        self.res_alu = self._reg_res_alu.match(line)
        self.res_mpy = self._reg_res_mpy.match(line)
        self.res_memory = self._reg_res_memory.match(line)
        self.reg_r0 = self._reg_reg_r0.match(line)
        self.reg_b0 = self._reg_reg_b0.match(line)
        #self.reg_b0 = self._reg_reg_b0.search(line)


# ASSUMES THAT configuration.mm IS PRESENT IN THE SAME DIRECTORY
if __name__ == '__main__':
    filepath = 'configuration.mm'
    data = parse(filepath)

    print(data[:-2])
    print("Total area utilized = " + str(data[-1]))