if [ -d ./outputs/$2 ]
then
	echo "Directory ./output/$2 already exist!"
else
	mkdir ./outputs/$2
fi

if [ -e ../../lfr/outputs/$2/network.dat ]
then
	cp ../../lfr/outputs/$2/network.dat ./
fi

./src/comboCPP network.dat $1

if [ -e ./*_comm_comboC++.txt ]
then
	
	echo "./src/comboCPP network.dat $1" > ./outputs/$2/$2
	rm ./network.dat
	mv ./*_comm_comboC++.txt ./outputs/$2
else
	echo "Cannot find *_comm_comboC++.txt!"
fi

