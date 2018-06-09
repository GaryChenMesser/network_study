if [ -d ./outputs/$2 ]
then
 echo "Directory ./output/$2 already exist!"
else
	$1
	if [ -e ./network.dat ]
	then
		mkdir ./outputs/$2
		echo $1 > ./outputs/$2/$2
		mv ./network.dat ./outputs/$2
		mv ./community.dat ./outputs/$2
		mv ./statistics.dat ./outputs/$2
	else
		echo "Cannot find network.dat!"
	fi
fi
