#!/bin/bash
# (c) Samuel Lampa, 2013, UPPMAX
# Script that creates a file containing a module name on the first column on 
# each line, followed by all possible binaries of that file, separated by colon.

function module_bins() {
    { for mod in $(cat ../etc/modulescache|grep -v ":"|grep -oP "^[a-zA-Z][a-zA-Z0-9\-\_]*"|grep -v "/"|sort|uniq); do 
        echo $mod":"$(module show $mod 2>&1|grep prepend-path|grep -oP "\/[^\:]+"|sort|uniq|xargs ls|tr "\n" ":"); done; 
    } 2>/dev/null 
}

function bin_module_map() {
    read line;
    mod=$(echo $line|grep -oP "^[^\:]+");
    for bin in $(echo $line|tr ":" " "); do
        echo "$bin:$mod";
    done;
}

{ for line in $(module_bins); do 
    echo $line|bin_module_map;
done; } | grep -v bioinfo-tools|grep -v modules|grep -v "\."
