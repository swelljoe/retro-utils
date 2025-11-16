#!/bin/sh
# Convert a bin charset to a series of bytes
# You don't need to do this, you can just load the bin file, but I want
# "source" I can work with.

xxd -g1 -c8 $1 \
| sed 's/^.*: //' \
| sed 's/  .*//' \
| awk '{
    printf ".byte "
    for (i=1; i<=NF; i++) {
        printf "$%s", toupper($i)
        if (i < NF) printf ","
    }
    printf "\n"
}'
