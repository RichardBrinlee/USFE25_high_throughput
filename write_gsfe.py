import os
import shutil

# These three messages are breaking apart the lmp_gsfe.in file to edit sections of it
message_1 = '''#This is the file to calculate the <111> GSFE curve. Along this curve, there are 101 data points. orient [11-2] [111] [1-10], x, y, z

#shell   mkdir      dump

#variable	n loop 20
#label		loopn

# ------------------- INITIALIZE -------------------------------
units           metal
dimension	3
boundary        p p s
atom_style      atomic

# ------------------- ATOM DEFINE ------------------------------
'''

message_2 = '''variable        xl equal 0
variable        xh equal 3
variable        yl equal 0
variable        yh equal 2
variable        zl equal 0
variable        zh equal 8

lattice         bcc ${latparam} orient x 1 1 -2 orient y 1 1 1 orient z 1 -1 0
region          mybox block ${xl} ${xh} ${yl} ${yh} ${zl} ${zh}

create_box      5 mybox

mass 1 180.948
mass 2 92.9064
mass 3 50.9415
mass 4 95.94
mass 5 183.84
'''

message_3 = '''
# ------------------- FIELD DEFINE -----------------------------
pair_style        mlip mlip.ini
pair_coeff        * *

neighbor        0.3     bin
neigh_modify    delay   10

# ------------------- SETTINGS ---------------------------------
thermo          1000
thermo_style    custom step etotal

variable        fixz equal ${latparam}/sqrt(2.)*1.5

variable        tmp0 equal "zlo"      ##### 8>5.8799999999999999 (potential cutoff), variable
variable        zlo0 equal ${tmp0}+${fixz}
variable        tmp1 equal "zhi"
variable        zhi0 equal ${tmp1}-${fixz}
variable        tmp2 equal "(zlo+zhi)/2"
variable        zmid equal ${tmp2}

region		upbound block INF INF INF INF ${zhi0} INF units box    
region		lobound block INF INF INF INF INF ${zlo0} units box      

group		upbound region upbound
group		lobound region lobound
group		boundary union lobound upbound
group		mobile subtract all boundary

variable        d equal 10.5
variable        mid equal ${zmid}+${latparam}/sqrt(2.)*(${d}-10)

region		upper block INF INF INF INF ${mid} INF units box      #variable
region		lower block INF INF INF INF INF ${mid} units box      #variable

group		top region upper
group		bot region lower

variable        Nslip equal 1                   #the number of periods
variable        stepn equal 100
variable        stepm equal ${Nslip}*${stepn}+1

variable        area equal lx*ly

variable        disp equal (${latparam}*sqrt(3)/2)/${stepn}

displace_atoms  bot move 0 ${disp} 0 units box

variable        a loop ${stepm}
label           loopa

variable        rdisp equal ($a-1)/${stepn}

displace_atoms  bot move 0 -${disp} 0 units box

compute         peratom all pe/atom
compute         eatoms all reduce sum c_peratom

variable        gsfe equal c_eatoms/${area}*1.60218*10000

dump            1 all custom 10000 dump.* id type xs ys zs

thermo          1
thermo_style    custom step pe c_eatoms

fix		1 boundary setforce 0.0 0.0 0.0
fix		2 mobile setforce 0.0 0.0 NULL

min_style       cg
minimize	1e-12 1e-12 10000 10000           #minimize        0.0 0.0 100000 100000

print           "${rdisp} ${gsfe}" append gsfe_ori

undump          1
unfix           1
unfix		2
uncompute       peratom
uncompute       eatoms

next            a
jump            lmp_gsfe.in loopa

#clear
#next		n
#jump		lmp_HEA.in loopn'''

# This is where the lattice parameter goes
lattices = 3.21090000000005
# This is the changing interger that is next to the set_boxes
lattice_set_num = 134
lattice_message_1 = 'variable latparam equal '
lattice_message_2 = ' #variable\n\n'

# Type 1: Ta
# Type 2: Nb
# Type 3: V
# Type 4: Mo
# Type 5: W

# Working right to left on the elements
#Fill the box with an element
box_type = 'create_atoms 3 box\n'
# Set the changes 1/4 of the box with the second element
set_type_1 = 'set type 3 type/ratio 1 0.25 '
# Changes a third of the remaining box to the third element
set_type_2 = 'set type 3 type/ratio 2 0.3333 '
# Changes half of the remaining box to the last element 
set_type_3 = 'set type 3 type/ratio 4 0.5 '


# Creates a file in the directery this file is located in
file_python_original = os.path.dirname(os.path.abspath(__file__))
# Names the file
file_python_alloy = 'MoNbTaV'
file_python_use = f'{file_python_original}/{file_python_alloy}'

changing_name = 1
file_new = file_python_use + '/' +str(changing_name)
os.makedirs(file_new)
p = 1
lattice_set_num = 134

while p <= 20:
    file_inner = file_new + '/'+ str(p)
    os.makedirs(file_inner)
    f = open(file_inner + '/lmp_gsfe.in', 'w')

    # Uses f-stringe to write the contents inside of the lmp_gsfe.in file
    full_message = f"{message_1}{lattice_message_1}{lattices}{lattice_message_2}{message_2}{box_type}{set_type_1}{lattice_set_num}\n{set_type_2}{lattice_set_num}\n{set_type_3}{lattice_set_num}{message_3}"
    f.write(full_message)
    f.close()
    
    # This section uses shutil to copy the files from the directery where this file is and puts them in the targeted folders
    # This is due to some files running on bash not liking pythons new lines.
    source = f'{file_python_original}/lmp.batch'
    shutil.copy(source, file_inner)
    source = f'{file_python_original}/mlip.ini'
    shutil.copy(source, file_inner)
    source = f'{file_python_original}/fitted.mtp'
    shutil.copy(source, file_inner)
    source = f'{file_python_original}/gsfe_curve.sh'
    shutil.copy(source, file_inner)
    lattice_set_num = lattice_set_num + 5
    p += 1
