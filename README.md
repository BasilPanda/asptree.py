# asptree.py
This code is an attempt at making the proposed ASP-tree and SWASP-Tree structure from Mining Associated Patterns from Wireless Sensor Networks research paper.

The goal of these tree structures is to be able to represent sensor data in a very compressed form when different epochs (tuples) have many sensors in common. This kind of path overlapping is referred as prefix-sharing and will be accomplished in two phases, the insertion phase and the restructuring-compression phase. Then the information will be mined and we can gather certin rules from it.

