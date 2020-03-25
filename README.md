##### Procedure to add datacollector_tests_project_path environment variable.

Add datacollector_tests_project_path environment variable in ~/.bashrc, example provided below

    export datacollector_tests_project_path=~/project/gerrit/datacollector-tests

Change the datacollector_tests_project_path variable according to datacollector-tests project in your system.

##### Guidelines to generate the automated test case code.


  i) **python main.py -h** will show the arguments to pass.
  
  ii)  Command to generate code
   
    python main.py git_branch stage_file_name.py testCaseName
  
   eg:
   
    python main.py SDC-11111 test_influxdb_destination.py test_database_name 

