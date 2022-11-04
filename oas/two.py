# Nima Dastmalchi
# 2022-11-01

from numpy import true_divide

# @param input_str - A space-separated string of parent-child pairs in the form:
#                    (parent1,child1) (parent2,child2) ...
# This function prints an error (E1,...,E5) and returns None in case of an error
# Otherwise, it will return a tuple of form (root, adj_list) where root is the
# root node of the tree and adj_list is an adjacency list, mapping each node to
# a list of its children.
def parse_input(input_str):
    pairs = input_str.split(' ')
    adj_list = {}
    num_parents = {}

    # Keep track of e5 error to print it out at the end
    e5_error = False
    for pair in pairs:
        if len(pair) != 5:
            print('E1')
            return None
        if pair[0] != '(' or\
           pair[2] != ',' or\
           pair[4] != ')':
           print('E1')
           return None
        parent = pair[1]
        child = pair[3]
        if parent not in adj_list:
            adj_list[parent] = []
        if parent not in num_parents:
            num_parents[parent] = 0
        if child not in adj_list:
            adj_list[child] = []
        if child not in num_parents:
            num_parents[child] = 0
        # Check duplicates (E2)
        for other_child in adj_list[parent]:
            if other_child == child:
                print('E2')
                return None
        # Check binary tree violations (E3)
        if len(adj_list[parent]) >= 2:
            print('E3')
            return None
        # Check for multiple parents violation (E5)
        num_parents[child] += 1
        if num_parents[child] >= 2:
            e5_error = True
        adj_list[parent].append(child)
    # Check for multiple roots (E4)
    num_roots = 0
    root = None
    for node, parents in num_parents.items():
        if parents == 0:
            root = node
            num_roots += 1
        if num_roots >= 2:
            print('E4')
            return None
    if root is None:
        e5_error = True
    # We have checked for all other errors. Check if we previously hit an E5 error:
    if e5_error:
        print('E5')
        return None
    # Return all structures we created:
    return root, adj_list


# @param root     - The root of the binary tree represented by adj_list
# @param adj_list - An adjacency list representing a binary tree
# This function prints the s expression of the tree and returns None
def print_s_expression(root, adj_list):
    print('(', root, sep='', end='')
    # Extract children of root:
    children = adj_list[root]
    if len(children) == 1:
        print_s_expression(children[0], adj_list) 
    elif len(children) == 2:
        smaller = min(children[0], children[1])
        larger = max(children[0], children[1])
        print_s_expression(smaller, adj_list)
        print_s_expression(larger, adj_list)
    print(')', end='')


# Main driver
# Take input. Check for errors. Print s-expression if no errors are found.
def main():
    result = parse_input(input())
    # If result is None, the parser printed errors with the input
    if result is None:
        return
    root, adj_list = result

    # At this point, no errors were detected, so print s_expression
    print_s_expression(root, adj_list)

main()
