# campus-cli

A command line utility to handle my files as a teacher. 

## Commands

### strip-solutions
- Usage : ```campus-cli ./my-notebook.ipynb``` will generate a student file with code cells containing the string ```# Solution``` removed. The file is saved under the name ```./my-notebook-student.ipynb```

### strip-solutions --dry-run
- Usage : ```campus-cli --dry-run ./my-notebook.ipynb``` will show you which file will be stripped from its solution. 


### strip-solutions -r
- Usage : ```campus-cli -r my-folder/``` will  recursively find ```.ipynb``` files and generate a student file with code cells containing the string ```# Solution``` removed. 

