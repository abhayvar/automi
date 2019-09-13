#!/bin/bash
for i in {1..12}
    do 
        if [i <= 8]
        then
            python3 ../helper_codes/rise_set_init_pos.py b $i & python3 ../helper_codes/rise_set_init_pos.py t $i
        else
            python3 ../helper_codes/rise_set_init_pos.py b $i && python3 ../helper_codes/rise_set_init_pos.py t $i
        fi
        sleep 1
    done