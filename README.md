# High-throughput code to build and run jobs to find the USFE
# Lattice
There are three files for building, submitting jobs, and obtaining the lattice parameters. They are write_lattice.py, crawler_min.sh, and crawler_lattice.sh.
The write_lattice.py will create the folder structure for crawler_lattice.sh to crawl through and submit jobs. The crawler_min.sh will crawl through the file structure and activate the min.sh file and collect all of that data to a single txt file which the lattice parameter will be in the middle column.

## Required
The write_lattice.py needs min.sh, mlip.sh, lmp.batch, and fitted.mtp to be in the same folder as it. to edit the required files edit in this structure the top line below is the location of the file and its name, the second line copies that file to the desired location.

source = f'{file_python_original}/lmp.batch'

shutil.copy(source, file_inner)

## Changing the alloyes
If you want to change the alloy to something different the below three lines is how you set up the first part. The box_type varible will change which allow is filled in the box first. The second and third will edit the compensition of the box of atoms.

box_type = 'create_atoms 5 box\n'

set_type_1 = 'set type 5 type/ratio 4 '


The below line demonstrates how to use the above variables to inset them into the lmp_0K file. You will want to are any addition set_type to the line and a lattice_set_num.

full_message = f"{message_1}{box_type}{set_type_1}{changing} {lattice_set_num}{message_2}"

The way the write_lattice.py is set up is to change the concentraction, you can change this by changing what goes into the changing variable or replace it with something else. You can also eliminate it by removing the variable and changing the below and having the concentrations hard coded.

set_type_1 = 'set type 5 type/ratio 4 0.5'


# GSFE
There are four files for working with GSFE write_gsfe_many.py, write_gsfe_binary.py, crawler_batch.sh, and crawler_gsfe.sh.

## Required
For these write files to work mlip.ini, lmp.batch, gsfe_curve.sh, and fitted.mtp are needed to be in the same folder that the write files are located at. You can change which files it requires by editing the write_gsfe.py by copying the source/destination layout that is there or by removing it.

## Write Files
The write_gsfe.py and write_gsfe_binary.py will create the file structure in a way for the crawlers to navigate. The write_gsfe.py will create a depth of 1 and create 20 different folders for the different intergers needed to be changed. The write_gsfe_binary.py is an example of how to change the concentraction of an element in the case of calculating 0.01 to 0.99 of a binary alloy it will create 99 folders for each concentract and each of those contain 20 subfolders.

To use the file place it in the place of desire and call python3 write_gsfe.py to activate it. Note if there is already a folder in the place already named what you are calling in the code it will place an error. Delete or move the folder that has the same name.

To edit how many alloys you are using you will need to add or remove set_type_... and configure it to what you want. Then in the whileloop you will edit the full_message variable adding {set_type_...}{lattice_set_num}. to get them at different lines you will need to add a \n to the message.

## Crawlers
There are two types of crawlers crawler_batch.sh and crawler_gsfe.sh. Once the folder structure is created using python place these two files in the folder that was created. 
Note the location should be not with the 20 subfolders but with the main folder contents. 
Once inside the folder using the terminal call
sh crawler_batch.sh to go through your folder contents and create the jobs. Note there is a limit on the jobs so change the outer varible and initial start in both crawler files to limit the amount of jobs created.

Once all the jobs are finished run the crawler_gsfe.sh file using sh crawler_gsfe.sh. This will comment on the terminal the USFE value of the alloy and also create a txt file in the folder.
