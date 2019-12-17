run bcnt -O3
cd ./output-bcnt.c
gprof a.out gmon-nocache.out > gmon-nocache.txt
pcntl bcnt.s > pcntl.txt