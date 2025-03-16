import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import random 
import string

def read_file_to_string(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    return content

def get_shift(symbol, table):

    index = table.index[table['symbol'] == symbol][0]

    symbols = table['symbol'].tolist()

    N = len(table)

    new_index = index + np.random.randint(low = -int(N/2), high = int(N/2)+1)

    new_symbol = symbols[new_index] #np.random.choice(symbols)

    return new_index, new_symbol

def plot_symbol_distribution(symbols, counts):

    plt.figure(figsize=(10, 5))
    plt.bar(symbols, counts, color='skyblue', edgecolor='black')
    plt.xlabel("Symbols")
    plt.ylabel("Frequency")
    plt.title("Symbol Distribution in Given String")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)


def get_distribution(string, table):
    dist = {}

    N = len(string)

    for char in table:
        dist[char] = string.count(char)

    dist = dict(sorted(dist.items(), key=lambda item: item[1], reverse=True))

    return dist

def get_frequency(string, table):

    freq = {}

    N = len(string)

    for char in table:
        freq[char] = string.count(char) / N

    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    return freq 


def get_conditional_dist(plaintext_dist, cipher_dist):
    conditional_dist = {}

    Total_counts = sum(plaintext_dist.values())

    for key in plaintext_dist.keys():
        conditional_dist[key] = plaintext_dist[key] / (Total_counts + cipher_dist[key]) 

    return dict(sorted(conditional_dist.items(), key=lambda item: item[1], reverse=True))

def plot_conditional_distribution(keys, items):
    plt.figure(figsize=(10, 5))
    plt.bar(keys, items, color='skyblue', edgecolor='black')
    plt.xlabel("Characters")
    plt.ylabel("Conditional Probability")
    plt.title("Conditional Distribution of Plaintext Based on Cipher Distribution")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    


def get_count_average(cipher_dist, current_cipher_dist, k):
    for char, count in current_cipher_dist.items():
        if char in cipher_dist:
            cipher_dist[char] += count  # Accumulate counts
        else:
            cipher_dist[char] = count  # Initialize count
    
    # Compute the average over all iterations
    return {char: total / k for char, total in cipher_dist.items()}

def entropy(p_arr):
    H = 0
    for p in p_arr:
        if p != 0:
            Hi = p * np.log2(p)
        else:
            Hi = 0
        H += Hi
    return -H

def conditionial_entropy(p_plain, p_ciph):
    H = 0 
    for p_p in p_plain:
        Hi = 0
        for p_c in p_ciph:
            if p_p != 0 and p_c != 0:
                Hi += p_p * p_c * np.log2(p_p)
            else:
                Hi = Hi
        H += Hi

    return -H

    
def main():
    filename = r"OTP_passage.txt"
    file_string = read_file_to_string(filename)
    ascii_string = r"ascii_table_clean.xlsx"
    ascii_table = pd.read_excel(ascii_string)
    ascii_table =  ascii_table.reset_index(drop = True)
    symbol_list = ascii_table['symbol'].tolist()
    symbol_list.append(" ")
    key = []
    cipher = ""

    N = int(len(file_string))

    iters = 400

    cipher_dist = {}

    # print(f"{random_string_from_list(symbol_list, N) = }")

    for k in range(iters):
        print(f"{k = }")
        for char in file_string:
            new_index, new_symbol = get_shift(char, ascii_table)
            key.append(new_index)
            cipher = cipher + new_symbol 
        current_cipher_dist = get_distribution(cipher, symbol_list)
        cipher_dist = get_count_average(cipher_dist, current_cipher_dist, k+1)
    plt.plot(cipher_dist.values())

    plaintext_dist = get_distribution(file_string, symbol_list)

    plaintext_freq = get_frequency(file_string, symbol_list)

    cipher_freq = get_frequency(cipher, symbol_list)

    conditional_dist = get_conditional_dist(plaintext_dist, cipher_dist)

    plot_symbol_distribution(plaintext_freq.keys(), plaintext_freq.values())
    plot_symbol_distribution(cipher_freq.keys(), cipher_freq.values())
    plot_conditional_distribution(conditional_dist.keys(), conditional_dist.values())

    H_plain = entropy(plaintext_freq.values())
    H_conditional = conditionial_entropy(plaintext_freq.values(), cipher_freq.values())

    print(f"{H_plain = }")
    print(f"{H_conditional = }")



    plt.show()
    







    

if __name__ == "__main__":
    main()