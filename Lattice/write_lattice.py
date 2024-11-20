import os
import shutil

message_1 = """
#Shuozhi Xu, OU

# ------------------- INITIALIZE -------------------------------
units           metal
boundary        p p p
atom_style      atomic

# ------------------- ATOM DEFINE ------------------------------

#read_data	data.ternary

variable        xl equal 0
variable        xh equal 20
variable        yl equal 0
variable        yh equal 20
variable        zl equal 0
variable        zh equal 20

lattice         bcc 3.3 orient x 1 0 0 orient y 0 1 0 orient z 0 0 1
region          mybox block ${xl} ${xh} ${yl} ${yh} ${zl} ${zh}

create_box      5 mybox

mass 1 180.948
mass 2 92.9064
mass 3 50.9415
mass 4 95.94
mass 5 183.84

"""

message_2 = """

# ------------------- FIELD DEFINE -----------------------------
pair_style        mlip mlip.ini
pair_coeff        * *

neighbor        0.3     bin
#neigh_modify    one   200 page 200

# ------------------- SETTINGS ---------------------------------
#### Computes Required

variable r equal 0.8

change_box all x scale $r y scale $r z scale $r remap

variable a loop 400

label loop

variable b equal $r+$a*0.001

variable c equal $r+($a-1)*0.001

variable d equal $b/$c

change_box all x scale $d y scale $d z scale $d remap

thermo          1
thermo_style    custom step lx ly lz pe etotal

variable lat_para equal (lx/20+ly/20+lz/20)/3.

variable eatom equal etotal/count(all)

# ------------------- EQUILIBRATE -----------------------

#run 0

#print "${lat_para} ${eatom}" file a_E
fix 1 all print 1 "$b ${lat_para} ${eatom}" append a_E screen no title ""

run 1
unfix 1
next a

jump lmp_0K.in loop"""

# Sets MoNb, MoTa, MoV, MoW, NbTa, NbV, NbW, TaV, TaW, VW
# Type 1: Ta
# Type 2: Nb
# Type 3: V
# Type 4: Mo
# Type 5: W
box_type = 'create_atoms 1 box\n'
set_type = 'set type 1 type/ratio 2 '

changing = 0.99
file_python_original = os.path.dirname(os.path.abspath(__file__))
file_python_alloy = 'NbTa'
file_python_use = f'{file_python_original}/{file_python_alloy}'
lattice_nums = -1
lattice_set_num = 134

while changing > 0:
    p = 1

    changing_name = round(changing*100)
    file_new = file_python_use + '/' + str(changing_name)
    os.makedirs(file_new)
    
    f = open(file_new + '/lmp_0k.in', 'w')
    full_message = f"{message_1}{box_type}{set_type}{changing} {lattice_set_num}{message_2}"
    f.write(full_message)
    f.close()
    source = f'{file_python_original}/lmp.batch'
    shutil.copy(source, file_new)
    source = f'{file_python_original}/mlip.ini'
    shutil.copy(source, file_new)
    source = f'{file_python_original}/fitted.mtp'
    shutil.copy(source, file_new)
    source = f'{file_python_original}/min.sh'
    shutil.copy(source, file_new)
    p += 1

    changing = round(changing - 0.01, 2)
    print(changing_name)
    #print(changing)
