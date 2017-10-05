#!/bin/bash
# 1.) create task strings
# 2.) create N replicates for loop
# 3.) create case for which task to use
# 4.) create stdout
#     - create csv for each task results
# {'1000': {'load':[...], 'select':[...]}}
# take file with times and convert to list and dictionary (python function) and spit as json
# after

run_psql ()
{
    for var in "$@"; do
	echo $var
	psql -U $USER -d $USER -c "$var" > /dev/null
    done
}

run_test ()
{
for task in load select_ filter groupby_agg; do
    case $task in
	load) query1="DELETE FROM test_table;"
	      query2a="\COPY test_table FROM ""'"$1"'"
	      query2b=" WITH DELIMITER ',';"
	      query2=$query2a$query2b
	      ;;
	select_) query="SELECT section FROM test_table;"
	      ;;
	filter) query="SELECT section FROM test_table WHERE section='A';"
	      ;;
	groupby_agg) line1="SELECT AVG(score_1), MAX(score_2) "
		     line2="FROM test_table "
		     line3="GROUP BY section;"
		     query=$line1$line2$line3
	      ;;
    esac

    # repeat for N replicates
    for i in "seq 1 $2"; do
	if [ $task = "load" ]; then
	    time run_psql "$query1"
	    time run_psql "$query2"
	else
	    time run_psql "$query"
	fi
    done
done
}

# initialize test_table
run_psql "DROP TABLE IF EXISTS test_table;"
run_psql "CREATE TABLE test_table (score_1 float, score_2 float, section char(1));"

# loop through each csv file
FILES=csv/*.csv
N=2

for f in $FILES; do
    run_test $f $N
done
