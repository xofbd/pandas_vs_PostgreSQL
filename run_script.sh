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
for n in 1000 10000 1000000 1000000 1000000; do
    file="test_"$n"_rows.csv"
    
    if [ ! -f $file ]; then
	python create_dataset.py $n 
    fi
done

# run pandas benchmark
# python run_pandas_benchmark.py
