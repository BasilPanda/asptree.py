class Node:
    def __init__(self, val):
        self.val = val
        self.children = []
        self.count = 0

    def value(self):
        return self.value

    def children(self):
        return [child for child in self.children]

    def cnt(self):
        return self.count

    def seen_again(self):
        self.count += 1
        return self.count

    def __str__(self):
        string = ''
        for child in self.children:
            string += child.val + ' '
        return string
            

    def insert(self, item_list):
        # makes sure that there is at least one item in list
        if not item_list:
            return "Finished/Empty List"
        
        root_node = self
        val = item_list[0]
        new_node = Node(val)
        
        # if root node has no children then add it to the root node's kids
        # this if/else statement only handles the root's children
        if not root_node.children:
            root_node.children.append(new_node)
            new_node.seen_again()
        else:
            child_not_found = True
            for child in root_node.children:
                if child.val == new_node.val:
                    child.seen_again()
                    child_not_found = False
                    break
                
            if child_not_found:
                root_node.children.append(new_node)
                new_node.seen_again()

        # if true, gets to the next item in list and adds it under the previous item
        if len(item_list) > 1:
            item_list.pop(0)
            new_node._insert(item_list,new_node)
        else:
            return "Finished"
                

    def _insert(self,item_list, prev_node):
        if not item_list:
            return "Finished/Empty List"

        val = item_list[0]
        new_node = Node(val)
        prev_node.children.append(new_node)
        new_node.seen_again()
        if len(item_list) > 1:
                item_list.pop(0)
                new_node._insert(item_list,new_node)
        else:
            return "Finished"

    # NOT DONE
    def find(self, item):
        node = root
        if not node.children:
            return False
        for child in node.children:
            char_not_found = True
            if child.val == item:
                char_not_found = False
                break
            

class Tree:
    def __init__(self):
        self.root = Node(None)

    def insert(self, item_list):
        self.root.insert(item_list)

    def __str__(self):
        string = self.all()
        return str(string)

    # INCOMPLETE, JUST PRINTS EVERYTHING
    def all(self):
        string = ''
        for child in self.root.children:
            string += child.val + '|'
            if not child.children:
                continue
            else:
                string += self._all(child) + ' '
        return string
    
    def _all(self, node):
        string = ''
        for child in node.children:
            string += child.val + ' '
            if not child.children:
                continue
            else:
                string += self._all(child)
        return string

    # not my code. doesn't work here.
    def bfs(self):
        nodes = []
        stack = [self.root.children]
        while stack:
            cur_node = stack[0]
            stack = stack[1:]
            nodes.append(cur_node[0].val)
            for child in cur_node:
                stack.append(child.val)
                return nodes
    
if __name__ == "__main__":
    t = Tree()
    ts1 = ['1','2','3','4']
    ts2 = ['2','3','4','5']
    ts3 = ['1','5']
    
    t.insert(ts1)
    t.insert(ts2)
    t.insert(ts3)
    print(t)


    
