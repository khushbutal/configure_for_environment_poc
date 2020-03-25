import os
# Add datacollector_tests_project_path environment variable in ~/.bashrc, example provided below
# export datacollector_tests_project_path=~/project/gerrit/datacollector-tests
# Change the datacollector_tests_project_path variable according to datacollector-tests project.
DataCollectorPath = os.environ['datacollector_tests_project_path']
dockerKillScriptPath = ""
