# asptree.py
This code is an attempt at making the proposed ASP-tree structure from Mining Associated Patterns from Wireless Sensor Networks research paper.

The goal of this program is to be able to represent sesnor data in a very compressed form when different epochs (tuples) have many sensors in common. This kind of path overlapping is referred as prefix-sharing and will be accomplished in two phases, the insertion phase and the restructuring-compression phase.

I inserted the tree with lists of data where each list contains epochs that have occured within the same time slot. 
