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

    def __iter__(self):
        return iter(self.children)

    def seen_again(self):
        self.count += 1
        return self.count

    def __repr__(self):
        return '{}:{}'.format(self.val, self.count)
            
    def insert(self, item_list):
        # makes sure that there is at least one item in list
        if not item_list:
            return "Finished/Empty List"
        
        root_node = self
        val = item_list[0]
        new_node = Node(val)
        
        # if root node has no children then add it to the root node's kids
        # this if/else statement only handles the tree root's children
        if not root_node.children:
            root_node.children.append(new_node)
            new_node.seen_again()
        else:
            child_not_found = True
            for child in root_node.children:
                if child.val == new_node.val:
                    new_node = child
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
                
    # handles all the children
    def _insert(self,item_list, prev_node):
        if not item_list:
            return "Finished/Empty List"

        val = item_list[0]
        new_node = Node(val)
        if not prev_node.children:
            prev_node.children.append(new_node)
            new_node.seen_again()
        else:
            child_not_found = True
            for child in prev_node.children:
                if child.val == new_node.val:
                    new_node = child
                    child.seen_again()
                    child_not_found = False
                    break
            if child_not_found:
                prev_node.children.append(new_node)
                new_node.seen_again()
                
        if len(item_list) > 1:
                item_list.pop(0)
                new_node._insert(item_list,new_node)
        else:
            return "Finished"

class Tree:
    def __init__(self):
        self.root = Node(None)
        #self.sFD = self.sfd()

    def insert(self, item_list):
        self.root.insert(item_list)

    def __str__(self):
        string = self.traverse()
        return str(string)

    # Creates a dict "list" in frequency-descending order (SFD)
    def sfd(self):
        l = self.traverse()
        flat = self.flatten()
        # flat = sorted(flat, key = lambda x: x.val)
        temp = self.merge(flat)
        temp = sorted(temp.items(), key=lambda x: (-x[1],x[0]))
        return temp

    def merge(self, lst):
        temp = {}
        for i in lst:
            if not i.val in temp:
                temp[i.val] = i.count
            else:
                temp[i.val] = temp[i.val] + i.count
        return temp
        
    # gives a flattened dfs list 
    def flatten(self):
        lst = []
        for child in self.root.children:
            lst.append(child)
            if child.children:
                lst += self._flatten(child)
        return lst

    def _flatten(self, node):
        lst = []
        for child in node.children:
            lst.append(child)
            if child.children:
                lst += self._flatten(child)
        return lst

    # does a dfs iteratively on the tree and returns it
    def traverse(self):
        lst = []
        for child in self.root.children:
            lst.append(child)
            if child.children:
                lst.append(self._traverse(child))
        return lst
    
    def _traverse(self, node):
        lst = []
        for child in node.children:
            lst.append(child)
            if child.children: 
                lst.append(self._traverse(child))
        return lst

    
if __name__ == "__main__":
    t = Tree()
    ts1 = ['s1','s2','s3','s4','s7','s8']
    ts2 = ['s1','s5','s6']
    ts3 = ['s2','s5','s6','s7','s8']
    ts4 = ['s1','s2','s4','s7']
    ts5 = ['s1','s2','s4','s5']
    ts6 = ['s1','s2','s3','s4','s7']
    
    t.insert(ts1)
    t.insert(ts2)
    t.insert(ts3)
    t.insert(ts4)
    t.insert(ts5)
    t.insert(ts6)
    #print(t)
    print(t.sfd())

    
