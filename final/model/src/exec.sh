python3 ./$1/main.py ../network/$2/$2.graphml $2

if [ ! -d ../outputs/$1 ]
then
	mkdir ../outputs/$1
fi

mv ./$2.dat ../outputs/$1
