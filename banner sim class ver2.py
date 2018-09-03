from RandBag import RandomBag
from ast import literal_eval
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
    def __init__(self, name = None):
        self.name = name
        self.kind = None
        self.free = True
        self.five_star_failed = 0
        self.pools = dict()
        self.five_session = None
        if name:
            self.dir_name = "banner " + name +r"\"
            infile = open(self.dir_name,"r")
            x = literal_eval(infile.readline())
            infile.close()
            self.set_parts(**x)
    def set_parts(self, kind = None, **pools):
        self.kind = kind
        for blah in kind:
            #TODO
            pass
    def fill_bags(self, fname):
        #for loc, rar in zip(locs,rars):
        loc = fname + r"\5.txt"
        bag =  Pool(5, loc)
        self.pools["five_bag"] = bag
        loc = fname + r"\4.txt"
        bag =  Pool(4, loc)
        self.pools["four_bag"] = bag
        loc = fname + r"\3.txt"
        bag =  Pool(3, loc)
        self.pools["three_bag"] = bag
    #def _fill_bags(self,
    def pity(self):
        return self.five_star_failed//5
    def set_base_rates(self, *args):
        for kind, arg in zip(self.kind, args):
            self.pool[kind].base_rate = arg
            
    def generate_rates(self):
        pity = self.five_star_failed//5
        #old way preserved show high pity logic in comparison to normal stuff
        #this is such a rare case that I don't think it's documented how it actually works
        #I've considered it negligible
        #if pity > 24:
        #    f = _ratehelper(self.pools["five_focus_bag"].base_rate, self.pools["five_bag"].base_rate, 100, 1)
        #    return (f[0], f[1], 0, 0)#not correct
        #    return [self.pools["five_focus_bag"].base_rate/(2*self.pools["five_bag"].base_rate), self.pools["five_bag"].base_rate/(2*self.pools["five_focus_bag"].base_rate),0,0]
        #four, three = self._ratehelper(self.pools["four_bag"].base_rate, self.pools["three_bag"].base_rate, pity, -1)
        #focus, five = self._ratehelper(self.pools["five_focus_bag"].base_rate, self.pools["five_bag"].base_rate, pity, 1)
        pos = []
        neg = []
        for kind in self.kind:
            pool = self.pools[kind]
            if pool.increases(): #as of now could also test rarity
                pos.append(pool)
            else:
                neg.append(pool)
        self._rh(pity, 1, *pos)
        self._rh(pity, -1, *neg)
        
    def _ratehelper(self, base_rate1, base_rate2, pity, sign):#self?
        total = base_rate1 + base_rate2
        rate1 = base_rate1 + sign * pity * 0.5 * base_rate1/total/100
        rate2 = base_rate2 + sign * pity * 0.5 * base_rate2/total/100
        return rate1, rate2
    #for futureproofing
    def _rh(self, pity, sign, *pools):#self?
        total = 0
        rates = []
        for pool in pools:
            total += pool.base_rate
        for pool in pools:
            pool.current_rate = pool.base_rate + sign * pity * 0.5 * pool.base_rate/(total*100)
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
    def get_current_rates(self):
        p = []
        for pool in self.kind:
            p.append(self.pools[pool].current_rate)
        return p

class FiveSession():
    def __init__(self, banner, **colors):
        self.banner = banner
        #I'm assuming they won't add new colors for now
        self.colors = {"Red":[], "Blue":[], "Green":[], "Colorless":[]}
        self.size = 5
        self.cost = (5, 4, 4, 4, 3)
        self._generate()
    def _generate(self):
        p = self.banner.get_current_rates()
        chosen_pools = np.random.choice(len(self.banner.kind), 5, p=p)
        for pool_pos in chosen_pools:
            pool = self.banner.kind[pool_pos]
            hero = self.banner.pools[pool].random()
            self.colors[hero.color].append(hero)
    def summon(self, color):
        hero = self.colors[color].pop()
        cost = self.cost[5 - self.size]
        self.size -=1
        return hero, cost #change?

class Hero():
    def __init__(self, name, color, rarity = None):
        self.color = color.strip()
        self.name = name
        self.rarity = rarity
    def __repr__(self):
        return f"Hero({self.name}, {self.color}, {self.rarity})"
        #return self.name

class Pool(RandBag.RandomBag):
    def __init__(self, rarity, fname = None):
        super().__init__()
        self.rarity = rarity
        self.base_rate = None########
        self.current_rate = None
        self.pity_sign = None
        if fname:
            self.fill(fname)
    def __repr__(self):
        return f"Pool{self.items}"
    
    def fill(self,fname):
        infile = open(fname,"r")
        for line in infile:
            hero = Hero(*line.split(sep="\t"), self.rarity)
            self.add(hero)

class Pool2(RandBag.RandomBag):
    def __init__(self, fname = None, **kwargs):
        super().__init__()
        self.name = None
        self.rarity = None
        self.base_rate = None
        self.current_rate = None
        #self.pity_sign = None
        self.pity_effect = None
        if fname:
            self.fname = fname
            infile = open(fname,"r")
            x = literal_eval(infile.readline())
            self.set_parts(**kwargs)#decide gosh darn it
            self.fill(infile)
            infile.close()
    def __repr__(self):
        return f"Pool{self.fname}"
    def fill(self,infile):
        for line in infile:
            hero = Hero(*line.split(sep="\t"), self.rarity)
            self.add(hero)
    def set_parts(self, name, rarity, base_rate, sign = None, pity_effect = None):
        self.name = name
        self.rarity = rarity
        self.base_rate = base_rate
        #self.pity_sign = sign
        self.pity_effect = pity_effect
    def increases(self):
        return self.pity_effect > 0
    def update_rate(self):
        self.current_rate = self.base_rate + self.pity_effect * self.banner.pity()
    def add_to_file(self, fname = None):
        #TODO
        pass
    def remove_from_file(self, fname = None):
        #TODO
        pass

class Player(Game):
    #temp cls
    def __init__(self,targets,failed_order,orbs,banner):
        super().__init__()
        self.orb_count = orbs
        self.orbs_spent = []
        self.targets = targets
        self.failed_order = failed_order
        self.banner = banner
    def summon(self):
        s = self.banner.generate_rates()
        self.banner.generate(s)
        session_heroes = []
        for color in self.targets:
            for hero in self.banner.five_session:
                    if hero.color == color:
                        session_heroes.append(hero)
        if not session_heroes:
            for color in self.failed_order:
                for hero in self.banner.five_session:
                    if hero.color == color:
                        session_heroes.append(hero)
                        break
                if session_heroes:
                    break
        for hero in session_heroes:
            if not hero.rarity == 5:
                self.banner.five_star_failed += 1
            else:
                self.banner.five_star_failed = 0
        self.hero_pool.append(session_heroes)
            
                    
    

def main():
    folder = r"banner cyl2"
    focus = folder + r"\5f.txt"
    regular = ("five_focus_bag", "five_bag", "four_bag", "three_bag")
    cyl2 = Banner("cyl2", regular)
    cyl2.pools["five_focus_bag"] = Pool(5,focus)
    cyl2.fill_bags(folder)
    #print(cyl2.pools)
    cyl2.set_base_rates(3/100,3/100,58/100,36/100)
    cyl2.five_star_failed = 0
    high = ("Green", "Blue", "Colorless", "Red")
    high3 = (("Green", "Colorless", "Red"),("Green", "Blue", "Red"))
    high2 = ("Green", "Red")
    low = ("Red", "Colorless", "Blue", "Green")
    messej = Player(high, low, 1, cyl2)
    for i in range(100):
        messej.summon()
    print(messej.hero_pool)
    
main()
    


    
