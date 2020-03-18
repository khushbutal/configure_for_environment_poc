import os
import sys
import fileinput


class GlobalVariable:
    def __init__(self, file_path, test_case_name, file_name):
        self.file_path = file_path
        self.test_case_name = test_case_name
        self.file_name = file_name

    def set_global_variable(self):
        got_first_stub = False
        global_data = None
        # list all the test case which needs global variable to set
        with open(os.path.join(sys.path[0], 'global_variable_initializers/InitializeGlobalfor.txt'), 'r')as f:
            data = f.read().splitlines()
        for line in data:
            if line in self.test_case_name or line in self.file_name:
                with open(os.path.join(sys.path[0], f'global_variable_initializers/{line}.txt'), 'r') as f:
                    global_data = f.read()
        if global_data:
            for line in fileinput.FileInput(self.file_path, inplace=1):
                if not got_first_stub:
                    if '@stub' in line:
                        line = line.rstrip()
                        line = line.replace(line, f'{global_data}'+'\n\n'+'@stub\n')
                        got_first_stub = True
                sys.stdout.write(line)



