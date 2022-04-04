import os, math
from unittest import case
import matplotlib.pyplot as plt
from numpy import gradient
def main():
    lenGraphs= []
    foldername = "mst_dataset"
    for filename in os.listdir(foldername):
        with open(foldername + "//" + filename) as f:
            line = (f.readlines())[0]
            nodes = int(line.split()[0])
            edges = int(line.split()[1])
            lenGraphs.append((nodes, edges))    
    

    graphSizes = [v for (v,e) in lenGraphs]

    Kruskal_RT = []
    Prim_RT = []
    Kruskal_Eff_RT = []
    files= ["Prim.csv", "Kruskal.csv", "Kruskal_Eff.csv"]
    for filename in files:
        with open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    r = int(line.split()[0])   # RT
                    w = int(line.split()[1])   # Weight
                    if filename == "Prim.csv": Prim_RT.append(r)                #
                    if filename == "Kruskal.csv": Kruskal_RT.append(r)          # match pattern in python 3.10    
                    if filename == "Kruskal_Eff.csv": Kruskal_Eff_RT.append(r)  #
    
    pyplot_Prim(graphSizes, Prim_RT , lenGraphs)
    pyplot_Kruskal(graphSizes[:50], Kruskal_RT , lenGraphs[:50])
    pyplot_Kruskal_Efficient(graphSizes, Kruskal_Eff_RT , lenGraphs)
    pyplot_Complete(graphSizes[:50], Prim_RT[:50], Kruskal_RT[:50], Kruskal_Eff_RT[:50])
    print("Done")

def pyplot_Complete(graphs_sizes, run_times_Prim, run_times_Kruskal, run_times_Kruskal_Efficient):
   
    ############# pyplot Total ##############
    plt.plot(graphs_sizes, run_times_Prim)
    plt.plot(graphs_sizes, run_times_Kruskal)
    plt.plot(graphs_sizes, run_times_Kruskal_Efficient)
    plt.legend(["Prim","Kruscal", "Kruskal_Efficient"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.savefig('All.png')
    plt.close()


def pyplot_Prim(graphs_sizes, run_times_Prim, graph_data):
    ############# pyplot Prim ##############
    reference = [n_e * math.log(n_n) * 10 ** 6 for (n_n, n_e) in graph_data]
    plt.plot(graphs_sizes, reference)
    plt.plot(graphs_sizes, run_times_Prim)
    plt.title("Prim")
    plt.legend(["Reference O(m*log(n))", "Prim"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.savefig('Prim.png')
    plt.close()
    #####################################################

def pyplot_Kruskal_Efficient(graphs_sizes, run_times_Kruskal_Efficient, graph_data):
    ############# pyplot Efficient Kruskal ##############

    reference = [n_e * math.log(n_n) * 10 ** 6 for (n_n, n_e) in graph_data]
    plt.plot(graphs_sizes, reference)
    plt.plot(graphs_sizes, run_times_Kruskal_Efficient)
    plt.title("Kruscal Efficient")
    plt.legend(["Reference O(m*log(n))", "Kruskal_Efficient"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.savefig('Kruskal_Efficient.png')
    plt.close()

    #####################################################

def pyplot_Kruskal(graphs_sizes, run_times_Kruskal, graph_data):
    ################## pyplot Kruskal ##################

    reference = [n_n * n_e * 2.5 * 10**4 for (n_n, n_e) in graph_data]
    plt.plot(graphs_sizes, reference)
    plt.plot(graphs_sizes, run_times_Kruskal)
    plt.title("Kruscal")
    plt.legend(["Reference O(n*m)", "Kruskal"])
    plt.ylabel('run time (ns)')
    plt.xlabel('size')
    plt.savefig('Kruskal.png')
    plt.close()

    #####################################################


if __name__ == '__main__':
    main()

    #667315
    #133400000