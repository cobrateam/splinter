#!/bin/bash

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

active_displays=$(ls /tmp/.X*-lock | sed 's/\/tmp\/\.X\(.*\)-lock/\1/')
last_active_display=$(echo "$active_displays" | sort -r | head -1)
new_display=$(echo "$last_active_display + 1" | bc)
xephyr_command="Xephyr :$new_display"

$xephyr_command 2> /dev/null &
DISPLAY=:$new_display make test

my_xephyr_pid=$(ps -A -o pid,cmd | grep Xephyr | \
        sed -n 's/[[:space:]]*\([0-9]*\) Xephyr :'"$new_display"'$/\1/p;')
kill -9 $my_xephyr_pid
