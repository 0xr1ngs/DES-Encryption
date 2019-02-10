#! /usr/bin/env python
# -*- coding: utf-8 -*-

from libnum import *
from base64 import *

def IP(m):
    mbin = s2b(m)

    vector = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]
    L= []
    for i in vector:
        i -= 1
        L.append(mbin[i])
    S =  ''.join(L)
    return (S[:32], S[-32:])

def L_move(raw_key, count):
    if count == 1:
        length = len(raw_key)
        temp = raw_key[0]
        key = []
        for i in range(length - count):
            key.append(raw_key[i + count])
        key.append(temp)
        return ''.join(key)
    else:
        length = len(raw_key)
        temp1 = raw_key[0]
        temp2 = raw_key[1]
        key = []
        for i in range(length - count):
            key.append(raw_key[i + count])
        key.append(temp1)
        key.append(temp2)
        return ''.join(key)


def get_k(rawkey):
    pc_2 = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]
    K = []
    CD = []
    for times in range(16):
        times += 1
        if times == 1:
            keybin = s2b(rawkey)

            vector_c = [
                57, 49, 41, 33, 25, 17, 9,
                1, 58, 50, 42, 34, 26, 18,
                10, 2, 59, 51, 43, 35, 27,
                19, 11, 3, 60, 52, 44, 36,
            ]
            L = []
            for i in vector_c:
                i -= 1
                L.append(keybin[i])
            C0 = ''.join(L)
            C1 = L_move(C0, 1)


            vector_d = [
                63, 55, 47, 39, 31, 23, 15,
                7, 62, 54, 46, 38, 30, 22,
                14, 6, 61, 53, 45, 37, 29,
                21, 13, 5, 28, 20, 12, 4,
            ]
            L = []
            for i in vector_d:
                i -= 1
                L.append(keybin[i])
            D0 =  ''.join(L)
            D1 = L_move(D0, 1)

            key = C1 + D1
            L = []
            for i in pc_2:
                i -= 1
                L.append(key[i])
            key = ''.join(L)
            K.append(key)
            CD.append((C1, D1))

        elif times == 2 or times == 9 or times == 16:
            CD_last = CD.pop()
            Ck = L_move(CD_last[0], 1)
            Dk = L_move(CD_last[1], 1)

            key = Ck + Dk
            L = []
            for i in pc_2:
                i -= 1
                L.append(key[i])
            key = ''.join(L)
            K.append(key)
            CD.append((Ck, Dk))
        else:
            CD_last = CD.pop()
            Ck = L_move(CD_last[0], 2)
            Dk = L_move(CD_last[1], 2)

            key = Ck + Dk
            L = []
            for i in pc_2:
                i -= 1
                L.append(key[i])
            key = ''.join(L)
            K.append(key)
            CD.append((Ck, Dk))
    return K


def expand(R):
    vector = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    L = []
    for i in vector:
        i -= 1
        L.append(R[i])

    return ''.join(L)

def xor(s1, s2):
    L = []
    for i in range(len(s1)):
        L.append(str(int(s1[i]) ^ int(s2[i])))

    return ''.join(L)


def S_replace(ci):
    S_1 = [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ]
    S_2 = [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ]
    S_3 = [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ]
    S_4 = [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ]
    S_5 = [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ]
    S_6 = [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ]
    S_7 = [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ]
    S_8 = [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]

    ci1 = ci[:6]
    ci2 = ci[6:12]
    ci3 = ci[12:18]
    ci4 = ci[18:24]
    ci5 = ci[24:30]
    ci6 = ci[30:36]
    ci7 = ci[36:42]
    ci8 = ci[42:48]

    ci1_new = '{:04b}'.format(S_1[int(ci1[0] + ci1[5], 2)][int(ci1[1] + ci1[2] + ci1[3] + ci1[4], 2)])
    ci2_new = '{:04b}'.format(S_2[int(ci2[0] + ci2[5], 2)][int(ci2[1] + ci2[2] + ci2[3] + ci2[4], 2)])
    ci3_new = '{:04b}'.format(S_3[int(ci3[0] + ci3[5], 2)][int(ci3[1] + ci3[2] + ci3[3] + ci3[4], 2)])
    ci4_new = '{:04b}'.format(S_4[int(ci4[0] + ci4[5], 2)][int(ci4[1] + ci4[2] + ci4[3] + ci4[4], 2)])
    ci5_new = '{:04b}'.format(S_5[int(ci5[0] + ci5[5], 2)][int(ci5[1] + ci5[2] + ci5[3] + ci5[4], 2)])
    ci6_new = '{:04b}'.format(S_6[int(ci6[0] + ci6[5], 2)][int(ci6[1] + ci6[2] + ci6[3] + ci6[4], 2)])
    ci7_new = '{:04b}'.format(S_7[int(ci7[0] + ci7[5], 2)][int(ci7[1] + ci7[2] + ci7[3] + ci7[4], 2)])
    ci8_new = '{:04b}'.format(S_8[int(ci8[0] + ci8[5], 2)][int(ci8[1] + ci8[2] + ci8[3] + ci8[4], 2)])
    cipher = ci1_new + ci2_new + ci3_new + ci4_new + ci5_new + ci6_new + ci7_new + ci8_new
    return cipher

def func(R, K):
    R = expand(R)
    cipher = xor(R, K)
    cipher = S_replace(cipher)
    cipher = P_replace(cipher)

    return cipher

def P_replace(ci):
    P = [
        16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
    ]
    L = []
    for i in P:
        i -= 1
        L.append(ci[i])

    return ''.join(L)

def IP_1(cipher):

    vector = [
        40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
    ]

    L = []
    for i in vector:
        i -= 1
        L.append(cipher[i])

    return ''.join(L)


def DES():
    plain = 'qwertyui'
    key = 'abcdefgh'

    L0, R0 =  IP(plain)
    K = get_k(key)

    LR = []
    LR.append([L0, R0])

    for i in range(16):
        temp = LR.pop()
        L = temp[1]
        R = xor(temp[0],func(temp[1], K[i]))
        LR.append((L, R))
    cipher = R + L
    cipher = IP_1(cipher)
    print hex(int(cipher, 2))
    

if __name__ == '__main__':
    DES()
