#! /usr/bin/sh
expr "$(id | awk '{ print $1 }')" : "uid=\(.*\)(.*)" # generate user id
