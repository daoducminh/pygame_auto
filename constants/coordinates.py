# -*- coding: utf-8 -*-

RD = 40  # Road width
BL = 140  # Block width
AL = 30  # Alley width

X0 = 0
X1 = X0 + RD
X2 = X1 + 140
X3 = X2 + 120
X4 = X3 + RD
X5 = X4 + BL
X6 = X5 + RD
X7 = X6 + 80
X8 = X6 + BL
X9 = X8 + RD
X10 = X9 + BL
X11 = X10 + RD
X12 = X0 + RD / 2
X13 = X3 + RD / 2
X14 = X5 + RD / 2
X15 = X8 + RD / 2
X16 = X10 + RD / 2

Y0 = 0
Y1 = Y0 + RD
Y2 = Y1 + 20
Y3 = Y2 + 10
Y4 = Y3 + 20
Y5 = Y3 + 40
Y6 = Y5 + AL
Y7 = Y6 + 40
Y8 = Y7 + RD
Y9 = Y8 + BL
Y10 = Y9 + RD
Y11 = Y10 + 30
Y12 = Y11 + AL
Y13 = Y12 + 50
Y14 = Y13 + AL
Y15 = Y14 + 30
Y16 = Y15 + RD
Y17 = Y0 + RD / 2
Y18 = Y17 + 20
Y19 = Y18 + 10
Y20 = Y19 + 15
Y21 = Y5 + AL / 2
Y22 = Y7 + RD / 2
Y23 = Y9 + RD / 2
Y24 = Y11 + AL / 2
Y25 = Y13 + AL / 2
Y26 = Y15 + RD / 2

A1 = (X0, Y0)
A2 = (X1, Y0)
A3 = (X10, Y1)
A4 = (X11, Y1)
B1 = (X1, Y1)
B2 = (X3, Y2)
B3 = (X4, Y2)
B4 = (X5, Y3)
B5 = (X6, Y3)
B6 = (X10, Y4)

C1 = (X1, Y7)
C2 = (X3, Y7)
C3 = (X4, Y7)
C4 = (X5, Y7)
C5 = (X6, Y7)
C6 = (X10, Y7)

D1 = (X1, Y8)
D2 = (X3, Y8)
D3 = (X4, Y8)
D4 = (X5, Y8)
D5 = (X6, Y8)
D6 = (X8, Y8)
D7 = (X9, Y8)
D8 = (X10, Y8)

E1 = (X1, Y9)
E2 = (X3, Y9)
E3 = (X4, Y9)
E4 = (X5, Y9)
E5 = (X6, Y9)
E6 = (X8, Y9)
E7 = (X9, Y9)
E8 = (X10, Y9)

F1 = (X1, Y10)
F2 = (X3, Y10)
F3 = (X4, Y10)
F4 = (X5, Y10)
F5 = (X6, Y10)
F6 = (X8, Y10)
F7 = (X9, Y10)
F8 = (X10, Y10)

G1 = (X1, Y15)
G2 = (X3, Y15)
G3 = (X4, Y15)
G4 = (X5, Y15)
G5 = (X6, Y15)
G6 = (X8, Y15)
G7 = (X9, Y15)
G8 = (X10, Y15)

H1 = (X0, Y16)
H2 = (X11, Y16)

I1 = (X6, Y5)
I2 = (X7, Y5)
I3 = (X7, Y6)
I4 = (X6, Y6)

J1 = (X2, Y11)
J2 = (X3, Y11)
J3 = (X3, Y12)
J4 = (X2, Y12)

K1 = (X1, Y13)
K2 = (X2, Y13)
K3 = (X2, Y14)
K4 = (X1, Y14)

O1 = (X12, Y17)
O2 = (X13, Y18)
O3 = (X14, Y19)
O4 = (X16, Y20)
O5 = (X14, Y21)
O6 = (X7, Y21)
O7 = (X12, Y22)
O8 = (X13, Y22)
O9 = (X14, Y22)
O10 = (X15, Y22)
O11 = (X16, Y22)
O12 = (X12, Y23)
O13 = (X13, Y23)
O14 = (X14, Y23)
O15 = (X15, Y23)
O16 = (X16, Y23)
O17 = (X2, Y24)
O18 = (X13, Y24)
O19 = (X12, Y25)
O20 = (X2, Y25)
O21 = (X12, Y26)
O22 = (X13, Y26)
O23 = (X14, Y26)
O24 = (X15, Y26)
O25 = (X16, Y26)

MAP_POSITION = (10, 10)

CAR_INIT_X = 10
CAR_INIT_Y = 10
