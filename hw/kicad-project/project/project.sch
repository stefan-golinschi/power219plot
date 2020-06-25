EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L my-modules:ssd1306 M1
U 1 1 5EF4CB08
P 4500 4100
F 0 "M1" H 4500 4415 50  0000 C CNN
F 1 "ssd1306" H 4500 4324 50  0000 C CNN
F 2 "my-footprints:ssd1306" H 4500 4100 50  0001 C CNN
F 3 "" H 4500 4100 50  0001 C CNN
	1    4500 4100
	1    0    0    -1  
$EndComp
$Comp
L my-modules:gy219 M2
U 1 1 5EF4CDFD
P 4500 2900
F 0 "M2" H 4500 3481 50  0000 C CNN
F 1 "gy219" H 4500 3390 50  0000 C CNN
F 2 "my-footprints:gy-219" H 4450 3000 50  0001 C CNN
F 3 "" H 4450 3000 50  0001 C CNN
	1    4500 2900
	1    0    0    -1  
$EndComp
$Comp
L MCU_Module:Arduino_Nano_v3.x A1
U 1 1 5EF4D4BE
P 6700 3650
F 0 "A1" H 6700 2561 50  0000 C CNN
F 1 "Arduino_Nano_v3.x" H 6700 2470 50  0000 C CNN
F 2 "Module:Arduino_Nano" H 6700 3650 50  0001 C CIN
F 3 "http://www.mouser.com/pdfdocs/Gravitech_Arduino_Nano3_0.pdf" H 6700 3650 50  0001 C CNN
	1    6700 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4900 4150 5300 4150
Wire Wire Line
	5300 4150 5300 5000
Wire Wire Line
	5300 5000 7400 5000
Wire Wire Line
	7400 5000 7400 4050
Wire Wire Line
	7400 4050 7200 4050
Wire Wire Line
	4950 2950 5300 2950
Wire Wire Line
	5300 2950 5300 4150
Connection ~ 5300 4150
Wire Wire Line
	7200 4150 7450 4150
Wire Wire Line
	7450 4150 7450 4950
Wire Wire Line
	7450 4950 5350 4950
Wire Wire Line
	5350 4950 5350 4050
Wire Wire Line
	5350 2850 4950 2850
Wire Wire Line
	4900 4050 5350 4050
Connection ~ 5350 4050
Wire Wire Line
	5350 4050 5350 2850
Wire Wire Line
	4500 2500 6900 2500
Wire Wire Line
	6900 2500 6900 2650
Wire Wire Line
	4100 4050 3900 4050
Wire Wire Line
	3900 4050 3900 2450
Wire Wire Line
	3900 2450 6800 2450
Wire Wire Line
	6800 2450 6800 2650
Wire Wire Line
	4100 4150 3900 4150
Wire Wire Line
	3900 4150 3900 5150
Wire Wire Line
	3900 5150 5450 5150
Wire Wire Line
	4500 3300 4500 3400
Wire Wire Line
	4500 3400 5450 3400
Wire Wire Line
	5450 3400 5450 5150
Connection ~ 5450 5150
Wire Wire Line
	5450 5150 6700 5150
Wire Wire Line
	6700 4650 6700 5150
Wire Wire Line
	6800 4650 6800 4750
Wire Wire Line
	6800 4750 5650 4750
Wire Wire Line
	5650 4750 5650 3300
Wire Wire Line
	5650 3300 4500 3300
Connection ~ 4500 3300
$EndSCHEMATC
