from suffix_trees import STree
import sys

class MatchingStatistics:
    def __init__(self, input_string):
        """
        Initializes the MatchingStatistics with the input string and constructs the suffix tree.
        
        Parameters:
            input_string (str): The string on which the suffix tree will be constructed.
        """
        self.set_max_recursion_depth(2500)
        self.input_string = input_string
        self.st = STree.STree(input_string)
        self.precomputed_leaf_nodes = self.compute_leaf_nodes()
    
    def set_max_recursion_depth(self, depth):
        """
        Sets the maximum recursion depth for the Python interpreter.
        
        Parameters:
            depth (int): The maximum depth of the Python interpreter stack.
        """
        sys.setrecursionlimit(depth)

    def compute_leaf_nodes(self):
        """
        Precomputes the leaf node values for each node in the suffix tree using BFS.
        
        Returns:
            dict: A dictionary {node: min_leaf_node} representing the first occurrence in the input text.
        """
        leaf_nodes = {}
        q = [self.st.root]
        while q:
            n = q.pop(0)
            leaf_nodes[n] = min(i.idx for i in n._get_leaves())
            q.extend(n.transition_links.values())
        return leaf_nodes

    def get_matching_statistics_table(self, input_pattern):
        """
        Computes the Matching Statistics using the Suffix Tree in linear time.
        
        Parameters:
            input_pattern (str): The string for which matching statistics is to be calculated.
        
        Returns:
            dict: Matching statistics table containing the first occurrence & length of the maximal-exact-match of each suffix in the pattern.
        """
        MS_TABLE = {}
        pattern_len = len(input_pattern)
        
        # Phase 1 : Initial Slow Match
        curr_match_length = 0
        traverse_tree_node = self.st.root
        slow_match_flag = 1

        while slow_match_flag and curr_match_length < pattern_len:
            if input_pattern[curr_match_length] in traverse_tree_node.transition_links:
                traverse_tree_node = traverse_tree_node.transition_links[input_pattern[curr_match_length]]
                edge_label = self.st._edgeLabel(traverse_tree_node, traverse_tree_node.parent)
                for c in edge_label:
                    if curr_match_length < pattern_len and c == input_pattern[curr_match_length]:
                        curr_match_length += 1
                    else:
                        slow_match_flag = 0
                        break
            else:
                slow_match_flag = 0

        if curr_match_length > 0:
            match_index = self.precomputed_leaf_nodes[traverse_tree_node]
        else:
            match_index = None
        MS_TABLE[0] = (match_index, curr_match_length)
        
        # Begin Phase 2 & Phase 3
        for i in range(1, pattern_len):
            slow_match_flag = 1

            # Phase 2: Fast Match
            if traverse_tree_node != self.st.root:
                if (traverse_tree_node.is_leaf() and traverse_tree_node.depth == curr_match_length - 1) or (traverse_tree_node.depth == curr_match_length):
                    traverse_tree_node = traverse_tree_node._get_suffix_link()
                    curr_match_length -= 1
                else:
                    curr_match_length -= 1
                    traverse_tree_node = traverse_tree_node.parent._get_suffix_link()

                    catch_up_to_curr_match_length = traverse_tree_node.depth
                    while catch_up_to_curr_match_length < curr_match_length:
                        traverse_tree_node = traverse_tree_node.transition_links[input_pattern[i + catch_up_to_curr_match_length]]
                        catch_up_to_curr_match_length = traverse_tree_node.depth
            
                # Phase 3: Slow Match - Match remaining characters in the edge_label
                edge_label = self.st._edgeLabel(traverse_tree_node, traverse_tree_node.parent)
                for c in range(curr_match_length - traverse_tree_node.parent.depth, len(edge_label)):
                    if i + curr_match_length < pattern_len and edge_label[c] == input_pattern[i + curr_match_length]:
                        curr_match_length += 1
                    else:
                        slow_match_flag = 0
                        break
            
            # Phase 3: Slow Match
            while slow_match_flag and i + curr_match_length < pattern_len:
                if input_pattern[i + curr_match_length] in traverse_tree_node.transition_links:
                    traverse_tree_node = traverse_tree_node.transition_links[input_pattern[i + curr_match_length]]
                    edge_label = self.st._edgeLabel(traverse_tree_node, traverse_tree_node.parent)
                    for c in edge_label:
                        if i + curr_match_length < pattern_len and c == input_pattern[i + curr_match_length]:
                            curr_match_length += 1
                        else:
                            slow_match_flag = 0
                            break
                else:
                    slow_match_flag = 0
            
            if curr_match_length > 0:
                match_index = self.precomputed_leaf_nodes[traverse_tree_node]
            else:
                match_index = None
            MS_TABLE[i] = (match_index, curr_match_length)
        
        return MS_TABLE