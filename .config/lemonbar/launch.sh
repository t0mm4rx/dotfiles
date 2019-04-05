#!/bin/bash
python ~/.config/lemonbar/bar.py &

~/.config/lemonbar/bar.sh | lemonbar -g 1920x30 -o 1 -f 'pt mono' -o 0 -f "Font awesome 5 free solid" -o 0 -f "Font awesome 5 brands regular" | python ~/.config/lemonbar/process_inputs.py
