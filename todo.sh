#!/bin/bash


function func_init() {
  todo_thing=$1
  todo_cmd=$2
  todo_time=$3
}

# shellcheck disable=SC2119
func_init $1 $2 $3
python3 /Users/mac/kizk/project/PY/TODO_tools/main.py ${todo_thing} ${todo_cmd} ${todo_time}
