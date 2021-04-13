# IR-Assignment1-Team-12
This GitHub Repository is for IR Assignment 1 of our Group 12. <br><br>
Dataset is in the "stories" folder and "main.py" is our code file in python language. <br>
This Assignment is based on Unigram Inverted Index querying. <br><br>

### Provided support for the following queries:  <br>
i. x OR y <br>
ii.  x AND y <br>
iii. x AND NOT y <br>
iv. x OR NOT y <br>
 <br> <br>

#### Input format:<br>
The first line contains the number of queries, N. <br>
The next 2N lines would represent the queries. <br>
Each query would consist of two lines: <br>
a) line 1: Input sentence <br>
b) line 2: Input operation sequence <br>
<br><br>
Some example queries: <br><br>

1. Input query: lion stood thoughtfully for a moment <br>
Input operation sequence: [ OR, OR , OR ] <br>
Expected query after preprocessing: lion OR stood OR thoughtfully OR moment <br>
<br>
Output-<br>
Number of documents matched: 270 <br>
No. of comparisons required: 671 <br><br>
2. Input query: telephone,paved, roads <br>
Input operation sequence: [ OR NOT, AND NOT ] <br>
Expected query after preprocessing: telephone OR NOT paved AND NOT roads <br>
<br>
Output- <br>
Number of documents matched: 466 <br>
No. of comparisons required: 739 <br>


<br><br><br>

Group Members: <br>
* Anjali Singh    : MT20049 <br>
* Meet Maheshwari : MT20012 <br>
* Priya Mehta     : MT20033 <br>
* Shaney Waris    : 2018308 <br>
* Vaibhav Goswami : MT20018 <br>
