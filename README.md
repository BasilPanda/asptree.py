# asptree.py
This code is an attempt at making the proposed ASP-tree and SWASP-Tree structure from Mining Associated Patterns from Wireless Sensor Networks research paper. This project was part of my Summer 2018 research internship and was also used to grow my Python skills.

The goal of these tree structures is to be able to represent sensor data in a very compressed form when different epochs (put into tuples) have many sensors in common. This kind of path overlapping is referred as prefix-sharing and will be accomplished in two phases, the insertion phase and the restructuring-compression phase. Then the information will be mined and we can gather certain rules from it. The rules will then be used to aid in detecting anomolies at a lower false positive rate.

The code will output the example tree as shown in figure 2 of the research paper.

It will also output the mined associated patterns of the example tree as shown in table 2.


After restructuring-compression:

[s1:5, [s2:4, [s4:4, [s7:3, [s3:2, [s8:1]], s5:1]], s5:1, [s6:1]], s2:1, [s7:1, [s5:1, [s6:1, [s8:1]]]]]

Associated Sensor Patterns:

{'s2': ['s1s2:4'], 's4': ['s1s4:4', 's2s4:4', 's1s2s4:4'], 's7': ['s1s7:3', 's2s7:4', 's4s7:3', 's1s2s7:3', 's1s4s7:3', 's2s4s7:3', 's1s2s4s7:3']}


# Bugs

The code does have bugs when given datasets in the millions. As a result, I learned to try to stay away from recursion when manipulating big data.
