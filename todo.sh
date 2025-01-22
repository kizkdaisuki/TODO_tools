#!/bin/bash


function func_init() {
  todo_thing=$1
  todo_cmd=$2
  todo_time=$3
  todo_importance=$4
  todo_another=$5
}

func_init $1 $2 $3 $4 $5
python3 /Users/kizk/kizk/project/PY/TODO_tools/main.py ${todo_thing} ${todo_cmd} ${todo_time} ${todo_importance} ${todo_another}
