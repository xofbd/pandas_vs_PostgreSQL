#!/bin/bash
# 4.) create stdout
#     - create csv for each task results
# {'1000': {'load':[...], 'select':[...]}}
# take file with times and convert to list and dictionary (python function) and spit as json
# after

# runs postgre given query
run_psql ()
{
    for var in "$@"; do
	psql -U $USER -d $USER -c "$var" > /dev/null
    done
}

# runs benchmark for given task
run_test ()
{

# create results file for specific row number csv
num_rows=$(echo $1 | grep -oP '(?<=_).*(?=_)')
results_file=time_results_$num_rows
touch $results_file

# loop through each task
for task in load select filter groupby_agg; do
    echo $task >> $results_file
	
    case $task in
	load) query1="DELETE FROM test_table;"
	      query2a="\COPY test_table FROM ""'"$1"'"
	      query2b=" WITH DELIMITER ',';"
	      query2=$query2a$query2b
	      ;;
	select) query="SELECT section FROM test_table;"
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
    for i in $(seq 1 $2); do
	if [ $task = "load" ]; then
	    t1=$(/usr/bin/time -f "%e" psql -U $USER -d $USER -c "$query1" > /dev/null)
	    t2=$(/usr/bin/time -f "%e" psql -U $USER -d $USER -c "$query2" > /dev/null)
	    T=$(t1+t1)
	    
      
	    echo "$query1" "$query2"
	    echo $T >> $results_file
	else
	    T=$(/usr/bin/time -f "%e" psql -U $USER -d $USER -c "$query" > /dev/null)
	    echo $T >> $results_file
	fi
    done
done
}


# initialize test_table
drop_tb="DROP TABLE IF EXISTS test_table;"
create_tb="CREATE TABLE test_table (score_1 float, score_2 float, section char(1));"
run_psql "$drop_tb" "$create_tb"

# remove old time_results file
if [ -f time_results  ]; then
    rm time_results
fi

# loop through each csv file
FILES=csv/*.csv
N=5

for f in $FILES; do
    run_test $f $N
done

# run results formater
python format_results time_results

# clean up
rm time_results