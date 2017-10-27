#!/bin/bash

# initialize tables
psql -U $USER -d $USER --file=queries/init.sql > /dev/null

for file_A in csv/A/test_A_1000000_rows.csv; do  #csv/A/*; do
    num_rows=$(echo $file_A | grep -oP '\d+')
    file_B="csv/B/test_B_"$num_rows"_rows.csv"
    echo $file_A
    
    query_A="\COPY test_table_A FROM "$file_A" WITH DELIMITER ',';"
    query_B="\COPY test_table_B FROM "$file_B" WITH DELIMITER ',';"
    
    psql -U $USER -d $USER -c "$query_A" > /dev/null
    psql -U $USER -d $USER -c "$query_B" > /dev/null
    #pgbench -U $USER -d $USER -c "$query_A" > /dev/null
    #pgbench -U $USER -d $USER -c "$query_B" > /dev/null
    
    for task in select filter groupby_agg join; do
	echo $task
	pgbench -l -n -t $1 -U $USER --file=queries/$task.sql > /dev/null
	mv pgbench_log* pgbench_$task"_"$num_rows".log"
    done
done

# remove created tables
psql -U $USER -d $USER --file=queries/clean_up.sql
