#!/bin/bash
#
# 2.) combine log results (python script to do this)
# 2.a) place all log files of a certain row number into separate directories
# 2.b) loop through all directories, creating json


# initialize tables and directories
psql -U $USER -d $USER --file=queries/init.sql > /dev/null

if [ ! -d log ]; then
    mkdir log
fi

for file_A in csv/A/*; do
    num_rows=$(echo $file_A | grep -oP '\d+')
    file_B="csv/B/test_B_"$num_rows"_rows.csv"
    echo $file_A

    echo "DELETE FROM test_table_A;" > queries/load.sql
    echo "DELETE FROM test_table_B;" > queries/load.sql
    
    query_A="COPY test_table_A FROM ""'""$PWD"/"$file_A""'"" WITH DELIMITER ',';"
    query_B="COPY test_table_B FROM ""'""$PWD"/"$file_B""'"" WITH DELIMITER ',';"
    
    echo "$query_A" >> queries/load.sql
    echo "$query_B" >> queries/load.sql
    
    pgbench -ln -t $1 --file=queries/load.sql > /dev/null
    mv pgbench_log* log/pgbench_load_$num_rows".log"
    
    for task in select filter groupby_agg join; do
	echo $task
	pgbench -ln -t $1 --file=queries/$task.sql > /dev/null
	mv pgbench_log* log/pgbench_$task"_"$num_rows".log"
    done
done

# format results from logs
#if [ -d log ]; then
#    rm -rf log 
#fi	    
		
# remove created tables
psql -U $USER -d $USER --file=queries/clean_up.sql
