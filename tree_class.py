class Node:

    def __init__(self, evaluation, gamestate):
        self.gamestate = gamestate
        self.evaluation = evaluation
        self.child = []


# Utility function to create a new tree node
def newNode(evaluation, gamestate):
    temp = Node(evaluation, gamestate)
    return temp


def getEvalutionListofChildren(node):
    output = list()
    for x in node.child:
        output.append(x.evaluation)
    return output


# Prints the n-ary tree level wise
def levelOrderTraversal(root):
    if (root == None):
        return;

    # Standard level order traversal code
    # using queue
    q = []  # Create a queue
    q.append(root);  # Enqueue root
    while (len(q) != 0):

        n = len(q);

        # If this node has children
        while (n > 0):

            # Dequeue an item from queue and print it
            p = q[0]
            q.pop(0);
            print(p.evaluation, end=' ')

            # Enqueue all children of the dequeued item
            for i in range(len(p.child)):
                q.append(p.child[i]);
            n -= 1

        print()  # Print new line between two levels