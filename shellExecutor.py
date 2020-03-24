from loggerUtility import logger
from UserSetiing import DataCollectorPath
# from CodeGenerator import generate_code
import subprocess
import os


def create_git_branch(gitbranch, file_name, test_case):
    try:
        os.chdir(f'{DataCollectorPath}')
        logger.info(f'creating a git branch {gitbranch}')
        print(os.getcwd())
        cmd1 = 'git checkout master'
        cmd2 = f'git checkout -b {gitbranch}'
        subprocess.call(cmd1, shell=True)
        subprocess.call('git reset --hard origin/master',shell=True)
        subprocess.call('git pull', shell=True)
        result = subprocess.call(cmd2, shell=True)
        if not result:
            logger.info(f'successfully created git branch {gitbranch}')
            logger.info("generating code")
            # generate_code(gitbranch, file_name, test_case)
            #call your function here - this will put the input and expected data
            #call your second function - this will paramatrize and remove @stub
        else:
            raise Exception(f'git branch {gitbranch} already exist')
    except Exception as error:
        logger.error(error)






