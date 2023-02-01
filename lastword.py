#!/usr/bin/env python3

import hashlib
import binascii
import random

system_random = random.SystemRandom()

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Converts string with 0 and 1 to hexadecimal
def binToHexa(n):
    bnum = int(n)
    temp = 0
    mul = 1
    # counter to check group of 4
    count = 1
    # char array to store hexadecimal number
    hexaDeciNum = ['0'] * 100
    # counter for hexadecimal number array
    i = 0
    while bnum != 0:
        rem = bnum % 10
        temp = temp + (rem * mul)
        # check if group of 4 completed
        if count % 4 == 0:
            # check if temp < 10
            if temp < 10:
                hexaDeciNum[i] = chr(temp + 48)
            else:
                hexaDeciNum[i] = chr(temp + 55)
            mul = 1
            temp = 0
            count = 1
            i = i + 1
        # group of 4 is not completed
        else:
            mul = mul * 2
            count = count + 1
        bnum = int(bnum / 10)
    # check if at end the group of 4 is not completed
    if count != 1:
        hexaDeciNum[i] = chr(temp + 48)
    # check at end the group of 4 is completed
    if count == 1:
        i = i - 1
    return hexaDeciNum[i]


print(color.YELLOW + 'Welcome to lastword.py!' + color.END)
print('Select the first words of your mnemonic with your personal method')
print('This tool calculates a possible last word that respects the BIP39 standard')
print(color.RED + 'DISCLAIMER: ' + color.END + 'always check that seeds are valid!\n')

# select seed lenght
tour = True
while tour:
    s_len = input(
        color.DARKCYAN + 'How many words do you want your mnemonic seed to have? (12/15/18/21/24)\n' + color.END)
    if s_len.isnumeric():
        s_len = int(s_len)
        if (s_len == 12 or s_len == 15 or s_len == 18 or s_len == 21 or s_len == 24):
            print(color.DARKCYAN + f'Please, insert the first {s_len - 1} words of your mnemonic seed' + color.END)
            tour = False
        else:
            print(color.RED + f'{s_len} not accepted! Please chose between 12, 15, 18, 21 or 24 words' + color.END)

# select seed language
tour2 = True
while tour2:
    print(color.DARKCYAN + 'Select the language for your mnemonic seed, typing the corresponding number' + color.END)
    print('  1 - english\n  2 - italian\n  3 - spanish\n  4 - french\n  5 - portuguese\n  6 - czech\n  7 - japanese\n  8 - chinese simplified\n  9 - chinese traditional\n  10 - korean')
    s_lang = input()
    if s_lang.isnumeric():
        s_lang = int(s_lang)
        if (s_lang > 0 and s_lang < 11):
            tour2 = False
            if s_lang == 1:
                wl = open('Wordlists/b39en', 'r')
            elif s_lang == 2:
                wl = open('Wordlists/b39it', 'r')
            elif s_lang == 3:
                wl = open('Wordlists/b39es', 'r')
            elif s_lang == 4:
                wl = open('Wordlists/b39fr', 'r')
            elif s_lang == 5:
                wl = open('Wordlists/b39pr', 'r')
            elif s_lang == 6:
                wl = open('Wordlists/b39cz', 'r')
            elif s_lang == 7:
                wl = open('Wordlists/b39jp', 'r')
            elif s_lang == 8:
                wl = open('Wordlists/b39cn', 'r')
            elif s_lang == 9:
                wl = open('Wordlists/b39cn2', 'r')
            elif s_lang == 10:
                wl = open('Wordlists/b39kr', 'r')
        else:
            print(color.RED + 'Unallowed number, only numbers between 1 and 10 are allowed' + color.END)
    else:
        print(color.RED + 'Unallowed answer, only numbers between 1 and 10 are allowed' + color.END)

# user provides words
seed_str = ''  # stores the first words of the seed
str_bin = ''
wordlist = wl.read()
i = 0
while i < (s_len - 1):
    word = input(color.DARKCYAN + f'please insert the {i + 1} word: ' + color.END)
    if ('\n' + word + '\n') in wordlist:
        i += 1
        seed_str = seed_str + word + ' '
        wl.seek(0)
        for num, line in enumerate(wl, 1):
            if word in line:
                index_dec = num - 1
                print(color.YELLOW + 'index: ' + color.END + f'{index_dec}')
        bin_word = str(bin(index_dec)[2:])
        bin_word = bin_word.zfill(11)
        str_bin += bin_word
    elif (word + '\n') in wordlist:
        wl.seek(0)
        for num, line in enumerate(wl, 1):
            if word in line:
                index_dec = num - 1
        if index_dec == 0:
            print(color.YELLOW + 'index: ' + color.END + f'{index_dec}')
            i += 1
            seed_str = seed_str + word + ' '
            bin_word = str(bin(index_dec)[2:])
            bin_word = bin_word.zfill(11)
            str_bin += bin_word
    else:
        print(color.RED + 'Unallowrd word!' + color.END)

# number of bits of entropy corresponding to each mnemonic seed lenght
ent = 256
if s_len == 12:
    ent = 128
elif s_len == 15:
    ent = 160
elif s_len == 18:
    ent = 192
elif s_len == 21:
    ent = 224

# Fill entropy
max_rand = 2 ** (ent - (11 * (s_len - 1)))  # each word corresponds to 11 bits. Some bits missing to reach the requested entropy to calculate checksum
ran_bits = str(bin(system_random.randint(0, max_rand))[2:])  # random bits to add to reach entropy bits
ran_bits = ran_bits.zfill(ent - (11 * (s_len - 1)))
print(color.YELLOW + '\nRandom bits added: ' + color.END + f'{ran_bits}')
str_bin += ran_bits  # adds last bits before the checksum

bytes = int(ent / 8)
tmp_bin = str_bin
# convert string with 0 and 1 to hex and to binary
bin_list = []
start = 0
part = 4
while start < len(tmp_bin):  # Splitting string in 4 digits parts
    bin_list.append(tmp_bin[start: start + part])
    start += part
# convert list with four 0 and 1 digits to list with hexadecimal letters
hex_list = []
for bn in bin_list:
    hex_list.append(binToHexa(bn))
hex_ent = ''.join(hex_list)  # creates hexadecimal string of entropy

tmp_bin = binascii.unhexlify(hex_ent)  # binary of entropy
tmp_hex = binascii.hexlify(tmp_bin)  # hexadecimal of entropy

str_hash = hashlib.sha256(tmp_bin).hexdigest()  # hashing binary of entropy

# Converting hash to binary
int_hash = int(str_hash, base=16)
bin_hash = str(bin(int_hash))[2:]

# Adding checksum to entropy
checksum = bin(int(str_hash, 16))[2:].zfill(256)[: bytes * 8 // 32]
print(color.YELLOW + 'Checksum: ' + color.END + f'{checksum}')
binary_seed = (bin(int(tmp_hex, 16))[2:].zfill(bytes * 8) + checksum)

# Finding the last word
last_word_bin = binary_seed[-11:]  # isolate the last 11 bits (random bits + checksum)
last_word_index = int(last_word_bin, 2)

wl.seek(0)
for i, line in enumerate(wl):  # access wordlist at the desired index
    if i == last_word_index:
        last_word = line.strip('\n')

print(color.YELLOW + f'Last word: ' + color.END + f'{last_word} (index: {last_word_index})')
mnemonic = seed_str + last_word  # add last word to mnemonic
print(color.GREEN + '\nYour mnemonic:' + color.END)
print(color.DARKCYAN + mnemonic + color.END)

print(color.BLUE + '\n==============================' + color.END)
print(color.BLUE + '= Made by the AnuBitux Team! =' + color.END)
print(color.BLUE + '==============================\n' + color.END)
