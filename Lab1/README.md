#CyberPhysicalSystemsLabs
##ADVANCED ALGORITHMS 2021-2022 - Labs exercise - UNIPD 2022

###Assignment 1 - Minimum Spanning Trees

Algorithms
In the first assigment you will compare three algorithms for the Minimum Spanning Tree problem:

Prim's Algorithm implemented with a Heap
Naive Kruskal's Algorithm with O(mn) complexity
Efficient Kruskal's Algorithm based on Union-Find
Dataset
The dataset contains 68 example graphs, ranging in size from 10 to 100,000 vertices, generated randomly with stanford-algs' TestCaseGenerator. Each file describes an undirected graph with integer weights using the following format:

[number_of_nodes] [number_of_edges] 
[one_node_edge_1] [other_node_edge_1] [weight_edge_1] 
[one_node_edge_2] [other_node_edge_2] [weight_edge_2] 
[one_node_edge_3] [other_node_edge_3] [weight_edge_3] 
...

For example, a row "2 3 -8874" indicates that there is an edge connecting vertex 2 to vertex 3 with weight -8874. Weights should NOT be assumed to be positive nor distinct.

•	###Question 1

Run the three algorithms you have implemented (Prim, Kruskal naive and Kruskal efficient) on the graphs of the dataset. Measure the execution times of the three algorithms and create a graph showing the increase of execution times as the number of vertices in the graph increases. Compare the measured times with the asymptotic complexity of the algorithms. For each problem instance, report the weight of the minimum spanning tree obtained by your code.

•	###Question 2

Comment on the results you have obtained: how do the algorithms behave with respect to the various instances? There is an algorithm that is always better than the others? Which of the three algorithms you have implemented is more efficient? 

What to deliver
A brief report on your project. The report must contain: 
an introductory section with a description of the algorithms and implementation choices you have made;
explanatory graphs of the results with the answers to the two questions; 
any originality you introduced in the implementation; 
a concluding section with your comments and your conclusions on results. 
The source code of the implementation in a single archive file (.zip, .tar.gz, etc.).
How to submit the assigment
You can do the assigment either on your own or in a group of up to three people. 
Create the group before submitting the assigment using the "Assigments: Groups self-selection" activity on moodle. 
You have to create a group even if you do the assigment on your own.
The first assigment must be delivered by Monday 25 April, 11:55 pm. Late submissions get a penalty.
Final remarks
You can implement the algorithms with any programming language you like. Basic data structures such as lists, queues, stacks, sets, dictionaries or maps, provided by the standard libraries of the language, can be used without restrictions. It is not allowed to use libraries that directly provide data structures and algorithms to represent and manipulate graphs, such as NetworkX, JGraphT or similar. 
Comment the essential parts of the code so that the reader can grasp the ideas that led you to write the code in that way. Comments help to clarify whether a bug is a conceptual error or just a small mistake. 
