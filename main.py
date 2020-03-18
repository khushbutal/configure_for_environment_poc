import argparse
from shellExecutor import create_git_branch


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('gitBranch', help='git Branch')
    parser.add_argument('file_name', help='Stage Name')
    parser.add_argument('testCaseName', help='test case name')
    args = parser.parse_args()
    gitBranch = args.gitBranch
    file_name = args.file_name
    test_case_name = args.testCaseName
    create_git_branch(gitBranch, file_name, test_case_name)








