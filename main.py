# The following code is written for Assignment 1 of IR
# The Assignment is based on Uni-gram Inverted Index querying

import glob
import os
import re

from nltk.corpus import stopwords
from nltk import word_tokenize

stop_words = set(stopwords.words('english'))

# inverted index
index = {}
# doc_id to doc_name
doc_info = {}
power_set = []
_1 = 1
_2 = 2

wind = "\\"
ubuntu = "/"
active = wind

def or_query(x, y):
    x, y = sorted(x), sorted(y)
    or_array = []
    comparisons = 0
    i, j = 0, 0
    while i < len(x) and j < len(y):
        if x[i] == y[j]:
            or_array.append(y[j])
            j += 1
            i += 1
            comparisons += _1
        else:
            comparisons += _2
            if x[i] < y[j]:
                or_array.append(x[i])
                i += 1
            else:
                or_array.append(y[j])
                j += 1

    while i < len(x):
        or_array.append(x[i])
        i += 1

    while j < len(y):
        or_array.append(y[j])
        j += 1

    return or_array, comparisons


def and_query(x, y):
    x, y = sorted(x), sorted(y)
    and_array = []
    comparisons = 0
    i, j = 0, 0
    while i < len(x) and j < len(y):
        if x[i] == y[j]:
            and_array.append(y[j])
            j += 1
            i += 1
            comparisons += _1
        else:
            comparisons += _2
            if x[i] < y[j]:
                i += 1
            else:
                j += 1
    return and_array, comparisons


def set_diff_query(x, y):
    # y-x
    x = sorted(x)
    i, j = 0, 0
    not_array = []
    comparisons = 0
    while i < len(x) and j < len(y):
        if x[i] == y[j]:
            comparisons += _1
            i += 1
            j += 1
        else:
            comparisons += _2
            if x[i] > y[j]:
                not_array.append(y[j])
                j += 1
            else:
                i += 1

    while j < len(y):
        not_array.append(y[j])
        j += 1

    return not_array, comparisons

# x or not y = p - (y-x)

def or_not_query(x, y):
    not_x, comp1 = set_diff_query(x, y)
    not_not_x, comp2 = set_diff_query(not_x, power_set)
    return not_not_x, comp1 + comp2


def and_not_query(x, y):
    x_and_not_y, comp2 = set_diff_query(y, x)
    return x_and_not_y, comp2


def get_doc_list_for_word(word):
    if word in index:
        return index[word]
    else:
        var = []
        return var


def get_name_for_doc_id(doc_id):
    if doc_id in doc_info:
        return doc_info[doc_id]
    else:
        return ""


def evaluate_cluster(doc_lists, operation=or_query):
    list_copy = doc_lists[:]
    sum_list = {}
    comparisons = 0
    while len(list_copy) != 1:
        sum_list = {}
        for i in range(len(list_copy) - 1):
            sum_list[i] = len(list_copy[i]) + len(list_copy[i + 1])

        min_i = min(sum_list, key=sum_list.get)

        list_copy[min_i], opr = operation(list_copy[min_i], list_copy[min_i + 1])
        comparisons += opr
        del list_copy[min_i + 1]

    final_list = list_copy[:][0]
    return final_list, comparisons


def create_clusters(query_doc_list, operations):
    # && >>> ||
    operations_func = {'OR': or_query, 'AND': and_query}
    opers = operations[:]
    doc_list = query_doc_list[:]
    comparisons = 0

    if 'AND' in opers:
        # Finding AND Clusters
        clust = []
        is_continued = False
        i = 0
        while i < len(opers):
            if opers[i] == 'AND':
                if not is_continued:
                    is_continued = True
                clust.append(doc_list[i])
                del doc_list[i]
                del opers[i]
            else:
                if is_continued:
                    clust.append(doc_list[i])
                    l, comp = evaluate_cluster(clust, operation=operations_func['AND'])
                    clust = []
                    doc_list[i] = l
                    comparisons += comp
                is_continued = False
                i += 1
        if is_continued:
            clust.append(doc_list[-1])
            l, comp = evaluate_cluster(clust, operation=operations_func['AND'])
            clust = []
            doc_list[i] = l
            comparisons += comp

    l, comp = evaluate_cluster(doc_list, operation=operations_func['OR'])

    return l, comparisons + comp


def perform_query(query_words, operations):
    comparisons = 0
    if len(query_words) == 1:
        if len(operations) > 0:
            print('Operations ignored.')
        ids = get_doc_list_for_word(query_words[0])
        return ids, 0, [get_name_for_doc_id(d_id) for d_id in ids]

    if not (len(query_words) == len(operations) + 1):
        raise ValueError('Size mismatch, expected len(query_sentence) = {len_sent} and len(operations) = {len_opr}.'
                         .format(len_sent=len(query_words), len_opr=len(operations)))

    query_doc_list = [0] * len(query_words)
    for i in range(len(query_words)):
        query_doc_list[i] = get_doc_list_for_word(query_words[i])

    doc_list = query_doc_list[0]
    comp = 0
    for i in range(len(operations)):
        if operations[i] == 'OR':
            doc_list, comp = or_query(doc_list, query_doc_list[i + 1])
        elif operations[i] == 'AND':
            doc_list, comp = and_query(doc_list, query_doc_list[i + 1])
        elif operations[i] == 'OR NOT':
            doc_list, comp = or_not_query(doc_list, query_doc_list[i + 1])
        elif operations[i] == 'AND NOT':
            doc_list, comp = and_not_query(doc_list, query_doc_list[i + 1])

        comparisons += comp

    print(comparisons)

    # Uncomment the below code for the following optimization
    # No need for LTR, only merge with optimal conditions
    # Precedence NOT > AND > OR

    # comparisons = 0
    # for i in range(len(operations)):
    #     if operations[i][-3:] == "NOT":
    #         operations[i] = operations[i][:-4]
    #         query_doc_list[i + 1], opr = set_diff_query(query_doc_list[i + 1], power_set)
    #         comparisons += opr
    #
    # doc_id_list, opr = create_clusters(query_doc_list, operations)
    # comparisons += opr

    return doc_list, comparisons, [get_name_for_doc_id(x) for x in doc_list]


def update_index(folder_name, filename, file_id):
    content = ""
    try:
        content = open(folder_name + filename, 'r').read()
    # except IOError:
    #     print("This file has some problem in reading ->", filename)
    except UnicodeDecodeError:
        content = str(open(folder_name + filename, 'rb').read())

    content_preprocesed = preprocess(content)  # list form.

    for token in content_preprocesed:
        if token in index:
            if index[token][-1] < file_id:
                index[token].append(file_id)
        else:
            index[token] = [file_id]


def prepare_dataset():
    # Get files under stories folder.
    cwd = os.getcwd()
    filename_with_path = glob.glob(cwd + active + "stories" + active + "*")
    filenames_stories = [i.split(active)[-1] for i in filename_with_path if
                         i.split(active)[-1] not in ["FARNON", "SRE", 'index.html']]

    # Get files under stories/FARNON folder.
    filename_with_path = glob.glob(cwd + active + "stories"  + active + "FARNON"  + active + "*")
    filenames_farnon = [i.split(active)[-1] for i in filename_with_path if i.split(active)[-1] not in ['index.html']]

    # # Get files under stories/SRE folder.
    filename_with_path = glob.glob(cwd + active + "stories" + active + "SRE" + active + "*")
    filenames_sre = [i.split(active)[-1] for i in filename_with_path if i.split(active)[-1] not in ['index.html']]

    # Indexing each filename.
    i = 0
    # Pre-Processing and updating 'index' dictionary.
    for filename in filenames_stories:
        update_index(cwd + active + "stories"  + active , filename, i)
        doc_info[i] = filename
        i += 1

    for filename in filenames_farnon:
        update_index(cwd + active + "stories"  + active +  "FARNON"  + active, filename, i)
        doc_info[i] = filename
        i += 1

    for filename in filenames_sre:
        update_index(cwd + active + "stories"  + active +  "SRE"  + active, filename, i)
        doc_info[i] = filename
        i += 1

    global power_set
    power_set = sorted(list(doc_info.keys()))	# [0, 1, 2, ...., 467]
    # Observation: max length of doc ids list is 40.


def remove_stop_words(query_sentence):
    return [w for w in query_sentence if w not in stop_words]


def preprocess(content):
    content = content.lower()
    content = re.sub(r'[+*/\\\-?.>,<\"\';:!@#$%^&()_`~]', ' ', content)
    content = word_tokenize(content)
    content = [word for word in content if word.isalpha()]
    content = remove_stop_words(content)
    return content


def main():
    T = int(input('Enter no of queries : ').strip())
    if T == 0:
        return
    print('========== Preparing Dataset ==========', end=' ')
    prepare_dataset()  # index is updated.
    print('[Done]')
    print("Vocab :", len(index.keys()), 'Documents :', len(power_set))
    for i in range(T):
        query_sentence = preprocess(input('\nEnter query sentence : '))
        if len(query_sentence) > 0:
            n = len(query_sentence) - 1
            operations = input('Enter operation sequence (Only ' + str(n) + ' operations is needed) : ').split(",")
            operations = [x.strip().upper() for x in operations]

            print('Running query : ', end=' ')
            for j in range(len(operations)):
                print(query_sentence[j], end=' ')
                print(operations[j], end=' ')
            print(query_sentence[-1])

            doc_id, min_operations, doc_names = perform_query(query_sentence, operations)
            print("Document ID : ", doc_id)
            print("Document Names (10 max) : ", doc_names[:10])
            print("Number of documents matched: ", len(doc_id))
            print("Minimum Operation : ", min_operations)
        else:
            print('Nothing to process')


if "__main__":
    main()
