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
        self.five_session = None
        
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
    #def _fill_bags(self,

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
        rate1 = base_rate1 + sign * pity * 0.5 * base_rate1/total/100
        rate2 = base_rate2 + sign * pity * 0.5 * base_rate2/total/100
        return rate1, rate2
    #for futureproofing
    def _rh(self, pity, sign, *base_rates):#self?
        total = 0
        rates = []
        for base_rate in base_rates:
            total += base_rate
        for base_rate in base_rates:
            rate = base_rate + sign * pity * 0.5 * base_rate/(total*100)
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
    cyl2.pools["five_focus_bag"] = RarityBag(5,focus)
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
    


    
