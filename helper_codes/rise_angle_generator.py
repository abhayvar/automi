#!/usr/bin/env python

# Author: Arunim Joarder

gen_file = open("../helper_codes/rise_after_fall_gen_64steps.txt")
num_dxls_gen = 0
for line in gen_file:
    num_dxls_gen += 1
gen_file.close()

gen_file_torso = open("../helper_codes/rise_after_fall_gen_64steps_torso.txt")
num_dxls_gen_torso = 0
for line in gen_file_torso:
    num_dxls_gen_torso += 1
gen_file_torso.close()

init_file = open("../helper_codes/rise_init_angles_biped.txt")
num_dxls_init = 0
for line in init_file:
    num_dxls_init += 1
init_file.close()

init_file_torso = open("../helper_codes/rise_init_angles_torso.txt")
num_dxls_init_torso = 0
for line in init_file_torso:
    num_dxls_init_torso += 1
init_file_torso.close()

gen_file = open("../helper_codes/rise_after_fall_gen_64steps.txt")
GEN_INFO = [0]*num_dxls_gen
for dxl_id in range(num_dxls_gen):
    GEN_INFO[dxl_id] = []
    line = gen_file.readline()
    GEN_INFO[dxl_id].append([int(x) for x in line.split()])
gen_file.close()

gen_file_torso = open("../helper_codes/rise_after_fall_gen_64steps_torso.txt")
GEN_INFO_TORSO = [0]*num_dxls_gen_torso
for dxl_id in range(num_dxls_gen_torso):
    GEN_INFO_TORSO[dxl_id] = []
    line = gen_file_torso.readline()
    GEN_INFO_TORSO[dxl_id].append([int(x) for x in line.split()])
gen_file.close()

init_file = open('../helper_codes/rise_init_angles_biped.txt')
INIT_INFO = [0]*num_dxls_init
for dxl_id in range(num_dxls_init):
    INIT_INFO[dxl_id] = []
    line = init_file.readline()
    INIT_INFO[dxl_id].append([(x) for x in line.split()])
init_file.close()
for dxl_id in range(num_dxls_init):
    for i in range(3):
        INIT_INFO[dxl_id][0][i] = int(INIT_INFO[dxl_id][0][i])

init_file_torso = open('../helper_codes/rise_init_angles_torso.txt')
INIT_INFO_TORSO = [0]*num_dxls_init_torso
for dxl_id in range(num_dxls_init_torso):
    INIT_INFO_TORSO[dxl_id] = []
    line = init_file_torso.readline()
    INIT_INFO_TORSO[dxl_id].append([(x) for x in line.split()])
init_file_torso.close()
for dxl_id in range(num_dxls_init_torso):
    for i in range(3):
        INIT_INFO_TORSO[dxl_id][0][i] = int(INIT_INFO_TORSO[dxl_id][0][i])

goal_file = open('../revised_scripts/rise_angles_biped.txt', 'a')

goal_file_torso = open('../revised_scripts/rise_angles_torso.txt', 'a')


def calculate_ang(angle, ch, dxl_index):
    if ch == '+':
        return (angle + INIT_INFO[dxl_index][0][2])

    elif ch == '-':
        return (INIT_INFO[dxl_index][0][2] - angle)

    else:
        return angle

def calculate_ang_torso(angle, ch, dxl_index):
    if ch == '+':
        return (angle + INIT_INFO_TORSO[dxl_index][0][2]) % 1024

    elif ch == '-':
        return (INIT_INFO_TORSO[dxl_index][0][2] - angle) % 1024

    else:
        return angle

for i in range(num_dxls_init):
    for j in range(num_dxls_gen):
        if INIT_INFO[i][0][0] == GEN_INFO[j][0][0]:
            goal_file.write(str(GEN_INFO[j][0][0]))
            goal_file.write(' ')
            for goal_index in range(1, len(GEN_INFO[j][0])):
                goal_file.write(str(calculate_ang(GEN_INFO[j][0][goal_index], INIT_INFO[i][0][3], i)))
                goal_file.write(' ')
            goal_file.write('\n')

for i in range(num_dxls_init_torso):
    for j in range(num_dxls_gen_torso):
        if INIT_INFO_TORSO[i][0][0] == GEN_INFO_TORSO[j][0][0]:
            goal_file_torso.write(str(GEN_INFO_TORSO[j][0][0]))
            goal_file_torso.write(' ')
            for goal_index in range(1, len(GEN_INFO_TORSO[j][0])):
                goal_file_torso.write(str(calculate_ang_torso(GEN_INFO_TORSO[j][0][goal_index], INIT_INFO_TORSO[i][0][3], i)))
                goal_file_torso.write(' ')
            goal_file_torso.write('\n')
