class Node:
    def __init__(self, val):
        self.val = val
        self.children = []
        self.count = 0
        self.parent = None

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
                
    # handles all the children
    def insert(self,item_list, prev_node):
        if not item_list:
            return "Finished/Empty List"

        val = item_list[0]
        new_node = Node(val)
        if not prev_node.children:
            prev_node.children.append(new_node)
            new_node.seen_again()
            new_node.parent = prev_node
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
                new_node.parent = prev_node
        if len(item_list) > 1:
                item_list.pop(0)
                new_node.insert(item_list,new_node)
        else:
            return "Finished"

    def flatten(self):
        lst = []
        for child in self.children:
            lst.append(child)
            if child.children:
                lst += child.flatten()
        return lst

    def traverse(self):
        lst = []
        for child in self.children:
            lst.append(child)
            if child.children: 
                lst.append(child.traverse())
        return lst

    def restruct(self, SFD):
        for child in self.children:
            if child.children:
                child.restruct(SFD)

            if SFD[child.val] > SFD[child.parent.val]:
                
                # print('Before:')
                # print('child: '+child.val+' parent: ' + child.parent.val + ' grandparent: ' + child.parent.parent.val)
                # print('grandchildren: ' + str(child.children))
                
                if child.children:
                    for grandchild in child.children:
                        grandchild.parent = child.parent
                        child.parent.children.append(grandchild)
                        
                child.children.clear()
                child.children.append(child.parent)
                child.parent.parent.children.append(child)
                
                if child.parent in child.parent.parent.children:
                    child.parent.parent.children.remove(child.parent)
                child.parent.children.remove(child)

                # These two lines don't make any sense as it would set the parent and the
                # grandparent both to the child BUT it makes the function output the tree
                # correctly after restructuring so if there's a problem later I'll fix it.
                child.parent.parent = child
                child.parent = child.parent.parent
                
                # print('After:')
                # print('child: '+child.val+' parent: ' + child.parent.val+ ' grandparent: ' + child.parent.parent.val)
                # print('grandchildren: ' + str(child.children))
        return self

    # NOT DONE
    def compress(self):
        temp = []
        for child in self.children:
            if not child in temp:
                temp.append(child)
            else:
                

class Tree:
    def __init__(self):
        self.root = Node(None)
        self.SFD = {}

    def update_SFD(self):
        self.SFD = self.sfd()
        return self.SFD
    
    def insert(self, item_list):
        # makes sure that there is at least one item in list
        if not item_list:
            return "Finished/Empty List"
        
        val = item_list[0]
        new_node = Node(val)
        
        # if root node has no children then add it to the root node's kids
        # this if/else statement only handles the tree root's children
        if not self.root.children:
            self.root.children.append(new_node)
            new_node.seen_again()
        else:
            child_not_found = True
            for child in self.root.children:
                if child.val == new_node.val:
                    new_node = child
                    child.seen_again()
                    child_not_found = False
                    break
                
            if child_not_found:
                self.root.children.append(new_node)
                new_node.seen_again()

        # if true, gets to the next item in list and adds it under the previous item
        if len(item_list) > 1:
            item_list.pop(0)
            new_node.insert(item_list,new_node)
        else:
            self.update_SFD()
            return "Finished"

    def __str__(self):
        string = self.traverse()
        return str(string)

    # Creates a dict "list" in frequency-descending order (SFD)
    def sfd(self):
        l = self.traverse()
        flat = self.flatten()
        temp = self.sfd_merge(flat)
        #temp = sorted(temp.items(), key=lambda x: (-x[1],x[0]))
        return temp

    def sfd_merge(self, lst):
        temp = {}
        for i in lst:
            if not i.val in temp:
                temp[i.val] = i.count
            else:
                temp[i.val] = temp[i.val] + i.count
        return temp

    # Restructures tree using SFD list.
    def restruct(self):
        SFD = self.SFD
        print(SFD)
        for child in self.root.children:
            if child.children:
                child.restruct(SFD)
            if child.parent != None:
                if SFD[child.val] > SFD[child.parent.val]:
                    if child.children:
                        for grandchild in child.children:
                                grandchild.parent = child.parent
                                child.parent.children.append(grandchild)
                                
                    child.children.clear()
                    child.children.append(child.parent) 
                    child.parent.parent.children.append(child)
                    child.parent.children.remove(child)
                    child.parent = child.parent.parent
        return self

    def compress(self):
        self.root.compress()
        
        
    # gives a flattened dfs list 
    def flatten(self):
        lst = []
        for child in self.root.children:
            lst.append(child)
            if child.children:
                lst += child.flatten()
        return lst

    # does a dfs iteratively on the tree and returns it
    def traverse(self):
        lst = []
        for child in self.root.children:
            lst.append(child)
            if child.children:
                lst.append(child.traverse())
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
    print(t)
    t.update_SFD()
    t.restruct()
    print(t)
    #print(t)
    # t.delete()
    #print(t.sfd())

    
