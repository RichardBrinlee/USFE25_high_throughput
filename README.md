# High-throughput code to build and run many files

## Lattice

## GSFE
There are four files for working with GSFE write_gsfe_mono.py, write_gsfe_binary.py, crawler_batch.sh, and crawler_gsfe.sh.

## Write Files
The write_gsfe_mono.py and write_gsfe_binary.py will create the file structure in a way for the crawlers to navigate. The write_gsfe_mono.py will create a depth of 1 and create 20 different folders for the different intergers needed to be changed. The write_gsfe_binary.py is an example of how to change the concentraction of an element in the case of calculating 0.01 to 0.99 of a binary alloy it will create 99 folders for each concentract and each of those contain 20 subfolders.

To use the file place it in the place of desire and call python3 'file_name' to activate it. Note if there is already a folder in the place already named what you are calling in the code it will place an error. Delete or move the folder that has the same name.

## Crawlers
There are two types of crawlers crawler_batch.sh and crawler_gsfe.sh. Once the folder structure is created using python place these two files in the folder that was created. 
Note the location should be not with the 20 subfolders but with the main folder contents. 
Once inside the folder using the terminal call
sh crawler_batch.sh to go through your folder contents and create the jobs. Note there is a limit on the jobs is change the inner and outer varibles to limit the amount of jobs created.

Once all the jobs are finished run the crawler_gsfe.sh file using sh crawler_gsfe.sh. This will comment on the terminal the USFE value of the alloy and also create a txt file in the folder.
