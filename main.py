from itertools import combinations
from datetime import datetime
import time

FIRST_COLUMN_HEADER = ''

def ila(table, decision_index, attributes):
    rules = []
    subdicts = divide_table(table, decision_index)
    for decision in subdicts:
        sub_table = subdicts[decision]
        j = 1
        while not check_row_classification(sub_table):
            if(j > len(attributes)):
                break
            combinations = create_combinations(sub_table, j, attributes)
            max_combination = None
            max_count = 0
            for combination in combinations:
                count = check_occurence(sub_table, table, combination)
                if count > max_count:
                    max_count = count
                    max_combination = combination
            if max_combination == None:
                j += 1
                continue
            add_classification_to_all(sub_table, max_combination)
            index = find_index(table, max_combination[0])
            rule = 'IF ' + table[0][index] + ' = ' + max_combination[0]
            for i in range(1, len(max_combination)):
                index = find_index(table, max_combination[i])
                rule += ' AND ' + table[0][index] + ' = ' + max_combination[i]
            rule += ' THEN decision = ' + decision
            rules.append( rule)
        for i in sub_table:
            if 'classified' in i:
                i.remove('classified')
    return rules


def find_index(table, value):
    """
    This function finds index in which the value is placed. It helps to get the header for specific attribute

    Parameters
    table: 
    """
    for i in table:
        if value in i:
            return i.index(value)

def add_classification_to_all(table, combination):
    for i in table:
        if any(value in combination for value in i): 
            i.append("classified")
    return table


def check_occurence(sub_table, table, combination):
    """
    This function returns number of occurence of specific combination: It only checks if the combination is in one sub table

    Parameters
    sub_table: table created for only one decision
    table: the whole table
    combination: attribute combination 
    """
    count_sub_table = count_occurence(sub_table, combination)
    count_main_table = count_occurence(table, combination)
    if count_sub_table == count_main_table:
        return count_sub_table
    return 0

def count_occurence(table, combination):
    """
    This function counts how many times specific combination occurence in a table

    Parameters
    table: the table which wil be iterated for specific combination
    combination: the combination which we will try to find in this specific table
    """
    count = 0
    for i in table:
        not_found = False
        for combine in combination:
            if combine not in i:
                not_found = True
        if not_found:
            continue
        if 'classified' not in i:
            count += 1
    return count

def create_combinations(table, j, indexes):
    """
    Creates combination for specific attributes. It uses <i>combinations</i> function from itertools which helps us to create combinations.
    For each row we are creating combination and we are choosing specific attributes from each row.

    Parameters
    table: the table from which we will make combinations
    j: number of attributes in one combination
    indexes: list of indexes which contain place of attributes
    """
    combine = []
    for row in table:
        attributes = []
        for i in indexes:
            attributes.append(row[i])
        if(j > len(attributes)):
            break
        for attribute_combination in combinations(attributes, j):
            combine.append(attribute_combination)
    return combine

def check_row_classification(table):
    """
    Checks if all rows are classified.

    Parameters
    table: it will be iterated to check if all rows are classified
    """
    for i in table:
        if "classified" not in i:
            return False
    return True

def divide_table(table, decision_index):
    """
    Divides a table depending on the decision

    Parameters
    table: the table which contains rows with different decisions
    decision_index: the index in the array which we can find the decision
    """
    subdicts = {}
    for row in table:
        if row[0] == FIRST_COLUMN_HEADER:
            continue
        decision = row[decision_index]
        if decision not in subdicts:
            subdicts[decision] = [row]
        else:
            subdicts[decision].append(row)
    return subdicts


def read_file(file_path):
    """
    Reads data from file

    Parameters
    file_name: the file name from which the data will be read
    """
    result = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in lines:
            result.append(i.split(";"))
    return result

def write_data(tab, file_name):
    """
    Writes file with specific data

    Parameters
    tab: array of data which will be saved
    file_name: the file name in which the data will be saved
    """
    f = open(file_name, "w", encoding="utf-8")
    for i in tab:
        f.write(i)
        f.write('\n')
    f.close()

import sys

if __name__ == "__main__":
    file_path = sys.argv[1]
    avoid_headers = sys.argv[2] == 'yes'
    attributes = sys.argv[3].split(",")
    attributes = [int(s) for s in attributes]
    decision = int(sys.argv[4])

    data = read_file(file_path)
    if avoid_headers:
        FIRST_COLUMN_HEADER = data[0][0]

    timestamps = []
    start_timestamp = time.time()
    formatted_time = datetime.fromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
    timestamps.append(formatted_time)
    results = ila(data, decision, attributes)

    end_timestamp = time.time()
    formatted_time = datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
    timestamps.append(formatted_time)

    write_data(results, "reguły.txt")
    write_data(timestamps, "timestamps.txt")

