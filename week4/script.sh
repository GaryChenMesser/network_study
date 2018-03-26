if [ "$1" == "main_forest.py" ]
then 
	python3 $1 --p $2 --r $3 --nodes $4
	python plot_all.py $1 $2 $3
elif [ "$1" == "main_heat.py" ]
then
	python3 $1 --f_max $2 --f_min $3 --b_max $4 --b_min $5 --insert $6 --nodes $7
	python plot_heat.py $1 $2 $3 $4 $5 $6
else
	python3 $1 --a $2 --c $3 --step $4 --init $5
	python plot_all.py $1 $2 $3
fi

