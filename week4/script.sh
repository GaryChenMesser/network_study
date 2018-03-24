if [ "$1" == "myforest.py" ]
then 
	python3 $1 --p $2 --r $3 --nodes $4
else
	python3 $1 --a $2 --c $3 --step $4 --init $5
fi

python plot_all.py $1 $2 $3 $4 $5
