run convolution_5x5 -O3
cd ./output-convolution_5x5.c
gprof a.out gmon-nocache.out > gmon-nocache.txt
pcntl convolution_5x5.s > pcntl.txt