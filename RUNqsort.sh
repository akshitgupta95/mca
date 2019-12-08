run qsort -O3
cd ./output-qsort.c
gprof a.out gmon-nocache.out > gmon-nocache.txt
pcntl qsort.s > pcntl.txt