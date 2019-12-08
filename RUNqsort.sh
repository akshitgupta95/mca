run ucbqsort -O3
cd ./output-ucbqsort.c
gprof a.out gmon-nocache.out > gmon-nocache.txt
pcntl ucbqsort.s > pcntl.txt