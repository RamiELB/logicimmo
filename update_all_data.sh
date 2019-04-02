#! /bin/bash

 res=$(ls in)

for i in $res ; do
	file=./in/$i
	./get_data < $file
done
