#!/bin/bash

function wait_ssh_connection() {
    host=$1
    while true
    do
        ssh -q $host -- : > /dev/null 2>&1
        if [ $? = 0 ]; then
            echo 'success'
            return 0;
        else
            echo 'failed'
        fi

        sleep 5
    done
}

name=$1
wait_ssh_connection $name
