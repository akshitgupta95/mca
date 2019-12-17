run engine -O3
cd ./output-engine.c
gprof a.out gmon-nocache.out > gmon-nocache.txt
pcntl engine.s > pcntl.txt