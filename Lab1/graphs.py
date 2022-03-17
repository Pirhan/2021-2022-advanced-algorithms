import os
def load_graph(filename):
        """ load the graph from the txt file """
        graph = {}
        nodes = set()
        with open(filename) as f:
            lines = f.readlines()
            for line in lines[1:]:
                v1 = int(line.split()[0])
                v2 = int(line.split()[1])
                c = int(line.split()[2])
                graph[(v1, v2)] = c
                nodes.add(v1)
                nodes.add(v2)
        
        return graph, nodes, lines

def test_graph(graph, lines, nodes):
    """
    This is only a test function on the load_graphs() correctness
    """
    discovered = []
    for (n1, n2) in graph:
        if n1 != n2:
            if n1 not in discovered:
                discovered.append(n1)
            if n2 not in discovered:
                discovered.append(n2)
    if len(nodes) != len(discovered) or len(lines)-1 != len(graph):
        return "Failed"
    return "Passed"

def main():
    
    foldername = "mst_dataset"
    for filename in os.listdir(foldername):
        graph, nodes, lines = load_graph(foldername + '\\' + filename)
        print(filename, " => ", test_graph(graph, lines, nodes))

if __name__ == '__main__':
    main()
        
                