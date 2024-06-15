# campus-cli

A command line utility to handle my files as a teacher. 

## Commands

### strip-solutions
- Create a student version of a notebook in which the code cells containing the solutions are removed. A code cell will is identified as a solution if it contains the string ```# Solution``` 
- Usage : ```campus-cli ./notebooks/my-notebook.ipynb``` will generate a student notebook file and save it under the name ```./notebooks/my-notebook-student.ipynb```

### strip-solutions -r
- Recursively apply ```strip-solutions``` to all notebooks within the folder passed as an argument. 
- Usage : ```campus-cli -r ./my-folder/``` 

### strip-solutions --dry-run
- Usage : ```campus-cli --dry-run ./notebooks/my-notebook.ipynb``` will show you which file will be stripped from its solution. 

### check-links
- Extract all urls from the document and checks it is valid ( 200 <= http_status_code < 300 )
- Usage :  ```campus-cli check-links ./kit_apprenant.pdf``` 

### check-links -r
- Recursively extract all urls from documents within the folder passed as an argument. Will only check ```.pdf```, ```.doc```, ```.doc```, ```.docx```, ```.md``` and ```.ipynb```.
- Usage :  ```campus-cli check-links ./kit_apprenant.pdf``` 