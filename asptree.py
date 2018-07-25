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

    def new_p(self,node):
        self.parent = node
        return self.parent

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
            if child.parent != None:
                if SFD[child.val] > SFD[child.parent.val]:
                    
                    #print('Before:')
                    #print('child: '+child.val+' parent: ' + child.parent.val + ' grandparent: ' + child.parent.parent.val)
                    #print('grandchildren: ' + str(child.children))
                    
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

                    temp_p = child.parent.parent
                    child.parent.new_p(child)
                    child.new_p(temp_p)
                    
                    #print('After:')
                    #print('child: '+child.val+' parent: ' + child.parent.val+ ' grandparent: ' + child.parent.parent.val)
                    #print('grandchildren: ' + str(child.children))
        return self

    def compress(self):
        temp = {}
        for child in self.children:
            if child.val not in temp:
                temp[child.val] = child
            else:
                dup_node = temp[child.val]
                child.count += dup_node.count
                child.children += (dup_node.children)
                self.children.remove(dup_node)
            if child.children:
                child.compress()

    # This is inefficient for the large scale data mining but it works and took me forever to figure out
    def mine(self, SFD, min_sup, min_all_conf):
        lst = []
        for key in SFD:
            if SFD[key] >= min_sup:
                temp = self.find(key)
                if temp:
                    lst.append(temp)            
        return lst

    def find(self, key):
        temp = {}
        for child in self.children:
            if key not in temp:
                temp[key] = []
            if child.children:
                temp2 = (child.find(key))
                for key in (temp.keys() | temp2.keys()):
                    if key in temp2:
                        temp[key] += (temp2[key])            
            if child.val == key and child.parent != None:
                lst = [child.check_p() + ":" + str(child.count)]
                temp[key].append(lst)
            if temp[key] == []:
                del temp[key]
        return temp
                
    def check_p(self):
        string = ''
        if self.parent != None:
            string = self.parent.val
            string = self.parent.check_p() + string
        return string
                
class Tree:
    # root is always null
    def __init__(self):
        self.root = Node(None)
        self.SFD = {}

    def update_SFD(self):
        self.SFD = self.sfd()
        # return self.SFD

    def insert(self, item_list):
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
        self.update_SFD()

    def __str__(self):
        return str(self.traverse())

    # Creates a dict "list" in frequency-descending order (SFD)
    def sfd(self):
        flat = self.flatten()
        temp = self.sfd_merge(flat)

# Uncomment the line below for it to be a list sorted in frequency-descending order. Will break other functions though.
        # temp = sorted(temp.items(), key=lambda x: (-x[1],x[0]))
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
        return self.root.restruct(self.SFD)

    # After restructuring, all similar nodes should have the same parent. This allows for easy compression
    def compress(self):
        return self.root.compress()

    def phase2(self):
        self.restruct()
        self.restruct()
        self.compress()
        return self
        
    # Gives a flattened dfs list 
    def flatten(self):
        return self.root.flatten()

    # Does a dfs iteratively on the tree and returns it
    def traverse(self):
        return self.root.traverse()

    def mine(self, min_sup, min_all_conf):
        return self.root.mine(self.SFD, min_sup, min_all_conf)
    
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
    print(t.sfd())
    # print("\nAfter inserting into tree:")
    # print(t)
    t.phase2()
    print("\nAfter restructuring-compression:")
    print(t)
    print("\nConditional Pattern Base:")
    print(t.mine(3,0))
