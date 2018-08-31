import random

class RandomBag():
    def __init__(self):
        self.item_to_position = {}
        self.items = []

    def __repr__(self):
        return f"RandomBag({self.items})"
        
    def __contains__(self,item):
        return item in self.item_to_position

    def __len__(self):
        return len(self.items)
        
    def print_contents(self):
        print(self.items)
        
    def add(self, item):
        if item in self:
            print("Item already in ", self)
            return
        self.items.append(item)
        self.item_to_position[item] = len(self)-1

    def remove(self, item):
        if not item in self:
            print("Item not in ", self)
            return
        position = self.item_to_position.pop(item)
        last_item = self.items.pop()
        if position != len(self):
            self.items[position] = last_item
            self.item_to_position[last_item] = position

    def random(self):
        return random.choice(self.items)
