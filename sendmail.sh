#!/bin/bash
help(){
    echo "eg:$0 [subject] [address] [content_file] [file]"
    echo ""
    exit 1
}
if [ "$1"="" ]; then
    help
fi
if [ "$2"="" ]; then
    help
else
    mail_to=$2
    echo "Send mail to ${mail_to}"
fi
if [ "$4"="" ]; then
    mail -s $1 ${mail_to}<$3
else
    mail -s $1 -A $4 ${mail_to}<$3
fi
