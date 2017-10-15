#!/bin/bash

# create csv directory
if [ ! -d csv ]; then
    mkdir csv
fi

# create results directory
if [ ! -d results ]; then
    mkdir results
fi

# create test csv files
for n in 10 100 1000 10000 100000 1000000 10000000; do
    file="csv/test_"$n"_rows.csv"
    
    if [ ! -f $file ]; then
	echo "creating $n row dataset"
	python create_dataset.py $n 
    fi
done

# run pandas benchmark
num_replicates=10
python benchmark_test.py postgre $num_replicates
python benchmark_test.py pandas $num_replicates
./benchmark_postgre_direct.sh $num_replicates
