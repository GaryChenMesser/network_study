python3 convert.py ../../lfr/outputs/$1/network.dat ../../lfr/outputs/$1/community.dat $1

if [ ! -d ./$1 ]
then
	mkdir ./$1
fi

mv *.graphml ./$1
