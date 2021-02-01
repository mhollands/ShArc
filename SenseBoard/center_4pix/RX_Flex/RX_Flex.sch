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
Text Label 3750 2250 2    50   ~ 0
CIN1p
Text Label 3750 2450 2    50   ~ 0
CIN1m
Text Label 3750 2650 2    50   ~ 0
CIN2m
Text Label 3750 2850 2    50   ~ 0
CIN2p
Wire Wire Line
	3400 2850 3750 2850
Wire Wire Line
	3750 2650 3400 2650
Wire Wire Line
	3400 2450 3750 2450
Wire Wire Line
	3750 2250 3400 2250
$Comp
L Connector:TestPoint_2Pole P1
U 1 1 5F3DBC90
P 5200 2850
F 0 "P1" V 5200 2908 50  0000 L CNN
F 1 "TestPoint_2Pole" V 5245 2908 50  0001 L CNN
F 2 "Pixels:Differential_Sense_7x6" H 5200 2850 50  0001 C CNN
F 3 "~" H 5200 2850 50  0001 C CNN
	1    5200 2850
	0    1    1    0   
$EndComp
Text Label 5150 2600 2    50   ~ 0
CIN1m
Wire Wire Line
	5150 2600 5200 2600
Wire Wire Line
	5200 2600 5200 2650
Text Label 5150 3100 2    50   ~ 0
CIN1p
Wire Wire Line
	5150 3100 5200 3100
Wire Wire Line
	5200 3100 5200 3050
$Comp
L Connector:TestPoint_2Pole P2
U 1 1 5F3DDCEE
P 5750 2850
F 0 "P2" V 5750 2908 50  0000 L CNN
F 1 "TestPoint_2Pole" V 5795 2908 50  0001 L CNN
F 2 "Pixels:Differential_Sense_7x6" H 5750 2850 50  0001 C CNN
F 3 "~" H 5750 2850 50  0001 C CNN
	1    5750 2850
	0    1    1    0   
$EndComp
Wire Wire Line
	5700 2600 5750 2600
Wire Wire Line
	5750 2600 5750 2650
Text Label 5700 3100 2    50   ~ 0
CIN1p
Wire Wire Line
	5700 3100 5750 3100
Wire Wire Line
	5750 3100 5750 3050
$Comp
L Connector:TestPoint_2Pole P3
U 1 1 5F3DE861
P 6300 2850
F 0 "P3" V 6300 2908 50  0000 L CNN
F 1 "TestPoint_2Pole" V 6345 2908 50  0001 L CNN
F 2 "Pixels:Differential_Sense_7x6" H 6300 2850 50  0001 C CNN
F 3 "~" H 6300 2850 50  0001 C CNN
	1    6300 2850
	0    1    1    0   
$EndComp
Text Label 6250 2600 2    50   ~ 0
CIN2m
Wire Wire Line
	6250 2600 6300 2600
Wire Wire Line
	6300 2600 6300 2650
Text Label 6250 3100 2    50   ~ 0
CIN2p
Wire Wire Line
	6250 3100 6300 3100
Wire Wire Line
	6300 3100 6300 3050
$Comp
L Connector:TestPoint_2Pole P4
U 1 1 5F3DE871
P 6850 2850
F 0 "P4" V 6850 2908 50  0000 L CNN
F 1 "TestPoint_2Pole" V 6895 2908 50  0001 L CNN
F 2 "Pixels:Differential_Sense_7x6" H 6850 2850 50  0001 C CNN
F 3 "~" H 6850 2850 50  0001 C CNN
	1    6850 2850
	0    1    1    0   
$EndComp
Text Label 6800 2600 2    50   ~ 0
CIN2m
Wire Wire Line
	6800 2600 6850 2600
Wire Wire Line
	6850 2600 6850 2650
Text Label 6800 3100 2    50   ~ 0
CIN2p
Wire Wire Line
	6800 3100 6850 3100
Wire Wire Line
	6850 3100 6850 3050
$Comp
L Mechanical:MountingHole H1
U 1 1 5F3E43C4
P 4350 2700
F 0 "H1" H 4450 2700 50  0000 L CNN
F 1 "MountingHole" H 4450 2655 50  0001 L CNN
F 2 "MountingHole:MountingHole_2.1mm" H 4350 2700 50  0001 C CNN
F 3 "~" H 4350 2700 50  0001 C CNN
	1    4350 2700
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x09 J1
U 1 1 5F43F14A
P 3200 2550
F 0 "J1" H 3118 2017 50  0000 C CNN
F 1 "Conn_01x09" H 3118 2016 50  0001 C CNN
F 2 "Molex_FPC:Molex_5051100992_edge" H 3200 2550 50  0001 C CNN
F 3 "~" H 3200 2550 50  0001 C CNN
	1    3200 2550
	-1   0    0    -1  
$EndComp
Text Label 5700 2600 2    50   ~ 0
CIN1m
$Comp
L Mechanical:MountingHole H2
U 1 1 5F441B7E
P 4350 2900
F 0 "H2" H 4450 2900 50  0000 L CNN
F 1 "MountingHole" H 4450 2855 50  0001 L CNN
F 2 "MountingHole:MountingHole_2.1mm" H 4350 2900 50  0001 C CNN
F 3 "~" H 4350 2900 50  0001 C CNN
	1    4350 2900
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H3
U 1 1 5F441E2C
P 4650 2700
F 0 "H3" H 4750 2700 50  0000 L CNN
F 1 "MountingHole" H 4750 2655 50  0001 L CNN
F 2 "MountingHole:MountingHole_2.1mm" H 4650 2700 50  0001 C CNN
F 3 "~" H 4650 2700 50  0001 C CNN
	1    4650 2700
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H4
U 1 1 5F44200E
P 4650 2900
F 0 "H4" H 4750 2900 50  0000 L CNN
F 1 "MountingHole" H 4750 2855 50  0001 L CNN
F 2 "MountingHole:MountingHole_2.1mm" H 4650 2900 50  0001 C CNN
F 3 "~" H 4650 2900 50  0001 C CNN
	1    4650 2900
	1    0    0    -1  
$EndComp
NoConn ~ 3400 2950
NoConn ~ 3400 2750
NoConn ~ 3400 2550
NoConn ~ 3400 2350
NoConn ~ 3400 2150
$EndSCHEMATC
