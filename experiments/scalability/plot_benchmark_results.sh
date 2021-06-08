#!/usr/bin/gnuplot -c

reset

set style textbox opaque

set term postscript eps size 8, 2.5 color blacktext "Helvetica" 24
set output "benchmark_result.eps"

set key right bottom

set xlabel "Size (queries)"
set ylabel "Time (seconds)"

set logscale x #2
set logscale y #2

set yrange[0:]
#set ytics 0.1

set xrange[0.9:1100]
#set xtics 0.1

set grid lc rgb "#d5e0c9"

set style line 1 lc rgb '#0060ad' lt 1 lw 2 ps 1.5 # --- blue
set style line 2 lc rgb '#dd181f' lt 2 lw 2 ps 1.5 # --- red
set style line 3 lc rgb '#006400' lt 3 lw 2 ps 1.5 # --- green

set title ""

plot '-' using 1:2 title "live" with points ls 1,'-' using 1:2 title "builder" with points ls 2,'-' using 1:2 title "sandbox" with points ls 3
1 0.138362 0.008994
2 0.237867 0.005796
4 0.439948 0.015067
8 0.842658 0.024212
16 1.618094 0.032605
32 3.292831 0.048066
64 6.466880 0.118479
128 13.006591 0.286513
256 25.260706 0.131923
512 50.078852 0.160661
1024 101.542028 1.505337
e
1 0.329111 0.007134
2 0.628701 0.017054
4 1.193032 0.010875
8 2.320764 0.048585
16 4.645997 0.124795
32 9.165583 0.084384
64 18.295728 0.125852
128 36.589426 0.683842
256 72.895058 1.441130
512 145.178425 2.865281
1024 289.015123 2.564121
e
1 20.389243 0.148324
2 38.662069 0.190256
4 74.980196 0.691611
8 147.528980 0.474182
16 293.150735 4.501323
32 582.947699 2.427878
64 1163.804304 6.148258
128 2317.720807 12.767707
256 4650.547709 8.392094
512 9265.708766 30.693994
1024 18625.660183 39.968593
e
