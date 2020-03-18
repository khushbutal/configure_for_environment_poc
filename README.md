""""how to run?"""


1.before running edit the file UserSetting.PY .
change the DataCollectorPath to your data collector folder path.
2.Run main.py file 
  i)python main.py -h will show you the arguments to pass
  
  ii)how to generate code ?
   python main.py git_branch stage_file_name.py testCaseName
   
   
   eg:
   python main.py SDC-11111 test_influxdb_destination.py test_database_name 
