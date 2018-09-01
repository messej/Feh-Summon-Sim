from RandBag import RandomBag
import RandBag
import numpy as np
class Game():
    def __init__(self):
        self.orb_count = 1000
        self.banners = []
        self.hero_pool = []
    def add_banner(self, banner):
        self.banners.append(banner)

class Banner():
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
        self.free = True
        self.five_star_failed = 0
        self.pools = {"five_focus_bag" : RarityBag(5),
                      "four_focus_bag" : RarityBag(4)}
        
    def fill_bags(self, fname):
        #for loc, rar in zip(locs,rars):
        loc = fname + r"\5.txt"
        bag =  RarityBag(5, loc)
        self.pools["five_bag"] = bag
        loc = fname + r"\4.txt"
        bag =  RarityBag(4, loc)
        self.pools["four_bag"] = bag
        loc = fname + r"\3.txt"
        bag =  RarityBag(3, loc)
        self.pools["three_bag"] = bag
    #def get_pool(self,key):
    #    return self.pools[key]
    def set_base_rates(self, focus, five, four, three, *args):
        """rates should be ints ex: 5 is 5%
        #types of banners "fest" "legendary" "regular" "4 and 5" """
        self.pools["five_focus_bag"].base_rate = focus
        self.pools["five_bag"].base_rate = five
        self.pools["four_bag"].base_rate = four
        self.pools["three_bag"].base_rate = three
        #self.pools["four_focus_bag"].base_rate = args[0]
        self.total_base_five_rate = focus + five
    def generate_rates(self):
        pity = self.five_star_failed//5
        #this is such a rare case that I don't think it's documented how it actually works
        #I've considered it negligible
        #if pity > 24:
        #    f = _ratehelper(self.pools["five_focus_bag"].base_rate, self.pools["five_bag"].base_rate, 100, 1)
        #    return (f[0], f[1], 0, 0)#not correct
        #    return [self.pools["five_focus_bag"].base_rate/(2*self.pools["five_bag"].base_rate), self.pools["five_bag"].base_rate/(2*self.pools["five_focus_bag"].base_rate),0,0]
        four, three = self._ratehelper(self.pools["four_bag"].base_rate, self.pools["three_bag"].base_rate, pity, -1)
        focus, five = self._ratehelper(self.pools["five_focus_bag"].base_rate, self.pools["five_bag"].base_rate, pity, 1)
        return (focus, five, four, three)
    def _ratehelper(self, base_rate1, base_rate2, pity, sign):#self?
        total = base_rate1 + base_rate2
        rate1 = base_rate1 + sign * pity * 0.5 * base_rate1/total
        rate2 = base_rate2 + sign * pity * 0.5 * base_rate2/total
        return rate1, rate2
    #for futureproofing
    def _rh(self, pity, sign, *base_rates):#self?
        total = 0
        rates = []
        for base_rate in base_rates:
            total += base_rate
        for base_rate in base_rates:
            rate = base_rate + sign * pity * 0.5 * base_rate/total
            rates.append(rate)
        return rates
    def generate(self,p2):
        p = []
        heroes = []
        #pools = self.kind
        for pool in self.kind:
            p.append(self.pools[pool].current_rate)
        chosen_pools = np.random.choice(len(self.kind), 5, p=p2)
        print(p2,chosen_pools,len(self.kind))
        for pool_pos in chosen_pools:
            pool = self.kind[pool_pos]
            heroes.append(self.pools[pool].random())
        self.five_session = heroes

class FiveSession():
    def __init__(self, banner):
        self.banner = banner
        self.heroes = self.generate()
    def generate(self):
        p = self.banner.generate_rates()
        #pools = [self.

class Hero():
    def __init__(self, name, color, rarity = None):
        self.color = color.strip()
        self.name = name
        self.rarity = rarity
    def __repr__(self):
        return f"Hero({self.name}, {self.color}, {self.rarity})"
        #return self.name

class RarityBag(RandBag.RandomBag):
    def __init__(self, rarity, fname = None):
        super().__init__()
        self.rarity = rarity
        self.base_rate = None########
        self.current_rate = None
        self.pity_increses = None
        if fname:
            self.fill(fname)
    def __repr__(self):
        return f"RarityBag{self.items}"
    
    def fill(self,fname):
        infile = open(fname,"r")
        for line in infile:
            hero = Hero(*line.split(sep="\t"), self.rarity)
            self.add(hero)
"""def read_banner_no_focus(fname):
    five_star_pool = []
    four_star_pool = []
    three_star_pool = []
    all_heroes = []
    infile = open(fname,"r")
    for line in infile:
        name, color, rarity3, rarity4, rarity5 = line.split()
        all_heroes.append((name, rarity3, rarity4, rarity5, color))
        if (int(rarity3)):
            three_star_pool.append((name,color))
        if (int(rarity4)):
            four_star_pool.append((name,color))
        if (int(rarity5)):
            five_star_pool.append((name,color))
    return three_star_pool, four_star_pool, five_star_pool, all_heroes"""
a = Banner("a","fest")
print(bool(a.pools['five_focus_bag']))
a.pools['five_focus_bag'].add("a")
print(bool(a.pools['five_focus_bag']))
def main():
    folder = r"D:\programs\feh\banner cyl2"
    focus = folder + r"\5f.txt"
    regular = ("five_focus_bag", "five_bag", "four_bag", "three_bag")
    cyl2 = Banner("cyl2", regular)
    cyl2.pools["five_focus_bag"] = RarityBag(5,focus)
    cyl2.fill_bags(folder)
    #print(cyl2.pools)
    cyl2.set_base_rates(3/100,3/100,58/100,36/100)
    cyl2.five_star_failed = 0
    s = cyl2.generate_rates()
    cyl2.generate(s)
    print(cyl2.five_session)
    
main()
    


    
