Overview
========
This is a script for training object relative position patterns.

Data Structure
==============
Rod
---
Rod is the relative position between a specified pair of objects.

Rod: {T1, T2, vec}

T1:	type of obj1, string
T2:	type of obj2, string
vec:	vector describing the relative position of obj1 and obj2, array[float]

Frame
-----
List of objs
obj: {type, position(x,y,z)}

