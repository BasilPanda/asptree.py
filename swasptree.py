class Node:
    def __init__(self, val):
        self.val = val
        self.children = []
        self.count = [0,0,0]
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

    def seen_again(self, batch_counter):
        if batch_counter >= 3:
            batch_counter = 2
        i = batch_counter % 3
        num = self.count[i] if i < len(self.count) else None
        num += 1
        self.count[i] = num
        return self.count

    def __repr__(self):
        return '{}:{}'.format(self.val, self.count)  
                
    # handles all the children
    def insert(self,item_list, batch_counter):
        if not item_list:
            return "Finished/Empty List"

        val = item_list[0]
        new_node = Node(val)
        if not self.children:
            self.children.append(new_node)
            new_node.seen_again(batch_counter)
            new_node.parent = self
        else:
            child_not_found = True
            for child in self.children:

                if child.val == new_node.val:
                    new_node = child
                    child.seen_again(batch_counter)
                    child_not_found = False
                    break

            if child_not_found:
                self.children.append(new_node)
                new_node.seen_again(batch_counter)
                new_node.parent = self

        if len(item_list) > 1:
                item_list.pop(0)
                new_node.insert(item_list,batch_counter)

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
                
                    temp_p = child.parent.parent
                    child.parent.new_p(child)
                    child.new_p(temp_p)
                    
                    # print('After:')
                    # print('child: '+child.val+' parent: ' + child.parent.val+ ' grandparent: ' + child.parent.parent.val)
                    # print('grandchildren: ' + str(child.children))
        return self

    def compress(self):
        temp = {}
        for child in self.children:
            if child.val not in temp:
                temp[child.val] = child
            else:
                dup_node = temp[child.val]
                for i in range(len(child.count)):
                    num = child.count[i] if i < len(child.count) else None
                    dup_num = dup_node.count[i] if i < len(dup_node.count) else None
                    child.count[i] = num + dup_num
                child.children += (dup_node.children)
                self.children.remove(dup_node)
            if child.children:
                child.compress()

    def update(self):
        for child in self.children:
            child.update()
            child.count.pop(0)
            child.count.append(0)
            i = 0
            if child.count[i] == 0 and child.count[i+1] == 0:
                self.children.remove(child)
                
class Tree:
    # root is always null
    def __init__(self):
        self.root = Node(None)
        self.SFD = {}
        self.list_counter = 0    # counts lists inserted into tree
        self.batch_counter = 0   # counts number of batches(when list_counter = 2 then +1 to batch_counter) inserted into tree

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
            new_node.seen_again(self.batch_counter)
        else:
            child_not_found = True
            for child in self.root.children:
                if child.val == new_node.val:
                    new_node = child
                    child.seen_again(self.batch_counter)
                    child_not_found = False
                    break
                
            if child_not_found:
                self.root.children.append(new_node)
                new_node.seen_again(self.batch_counter)

        # if true, gets to the next item in list and adds it under the previous item
        if len(item_list) > 1:
            item_list.pop(0)
            new_node.insert(item_list,self.batch_counter)
        self.list_counter += 1
        if self.list_counter % 2 == 0:
            self.batch_counter += 1
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

    def update(self):
        return self.root.update()

    def phase2(self):
        self.restruct()
        self.restruct()
        self.compress()
        self.update()
        return self
    
    # Gives a flattened dfs list 
    def flatten(self):
        return self.root.flatten()

    # Does a dfs iteratively on the tree and returns it
    def traverse(self):
        return self.root.traverse()
    
if __name__ == "__main__":
    t = Tree()
    ts1 = ['s1','s2','s3','s4','s7','s8']
    ts2 = ['s1','s5','s6']
    ts3 = ['s2','s5','s6','s7','s8']
    ts4 = ['s1','s2','s4','s7']
    ts5 = ['s1','s2','s4','s5']
    ts6 = ['s1','s2','s3','s4','s7']

    ts7 = ['s1','s2','s7']
    ts8 = ['s1','s3']
    
    t.insert(ts1)
    t.insert(ts2)
    t.insert(ts3)
    t.insert(ts4)
    t.insert(ts5)
    t.insert(ts6)
    
    
    print("\nAfter inserting batches 1-3 into tree:")
    print(t)
    t.phase2()
    print("\nAfter restructuring-compression and update:")
    print(t)
    
    t.insert(ts7)
    t.insert(ts8)

    print("\nAfter inserting batch 4:")
    print(t)
