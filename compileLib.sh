#!/bin/bash
gcc -c -Wall -Werror -fPIC a6.c
gcc -shared -o liba6.so a6.o