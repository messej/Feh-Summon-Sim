import random
#from random
def read_banner_no_focus(fname):
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
    return three_star_pool, four_star_pool, five_star_pool, all_heroes

def generate_hero_orb(rate, three_pool, four_pool, five_pool, focus_pool, pity): #returns a tuple (hero name, color, rarity
    three_rate, four_rate, five_rate, focus_rate = rate[0], rate[1], rate[2], rate[3]
    pity_multiplier = pity//5
    total_five_rate = five_rate + focus_rate
    add_focus = focus_rate * pity_multiplier * 0.5/total_five_rate
    add_five = five_rate * pity_multiplier * 0.5/total_five_rate
    three = three_rate - add_five
    four = three + four_rate - add_focus
    five = four + five_rate + add_five
    rn = 100 * (random.random())
    #generate rn
    if rn < three:
       a = len(three_pool)
       index = random.randrange(a)
       heroname_color_rarity = (three_pool[index][0], three_pool[index][1], 3)
       return heroname_color_rarity
    if rn < four:
       a = len(four_pool)
       index = random.randrange(a)
       heroname_color_rarity = (four_pool[index][0], four_pool[index][1], 4)
       return heroname_color_rarity
    if rn < five:
       a = len(five_pool)
       index = random.randrange(a)
       heroname_color_rarity = (five_pool[index][0], five_pool[index][1], 5)
       return heroname_color_rarity
    else:
        a = len(focus_pool)
        index = random.randrange(a)
        heroname_color_rarity = (focus_pool[index][0], focus_pool[index][1], 'focus')
        return heroname_color_rarity
def generate_summon_session(rate, three_pool, four_pool, five_pool, focus_pool, pity):
    summon_session=[]
    for i in range(5):
        summon_session.append(generate_hero_orb(rate, three_pool, four_pool, five_pool, focus_pool, pity))
    return summon_session

def count_colors(summon_set):
    colors = { "Red":0, "Blue":0, "Green":0, "Colorless":0}
    for horb in summon_set:
        colors[horb[1]] += 1
    return colors

def set_pull(summon_set, number_to_pull, order, list_summoned, cumulative_orbs_spent, pity, targets, target_check):
    cost = {5:5, 4:4, 3:4, 2:4, 1:3}
    while number_to_pull>0:
        for color in order:
            for i in range(len(summon_set)):#could be 5 if I didn't remove revealed h_orbs from summon session
                if color == summon_set[i][1]:
                    spent = cost[len(summon_set)]
                    cumulative_orbs_spent+=spent
                    hero = summon_set[i]
                    summon_set[i] = (False,False)
                    list_summoned.append((hero, cumulative_orbs_spent))
                    if hero[2] == 5 or hero[2] == 'focus':
                        pity = 0
                    else:
                        pity+=1
                    #targets[hero[0]] = (hero[0] in targets)
                    if (hero[0] in targets):
                        targets[hero[0]] = True
                        targets["Orb Cost"] = cumulative_orbs_spent
                    success = target_check(targets)
                    number_to_pull-=1
    summon_set = [x for x in summon_set if not(x == (False,False))]
    return list_summoned, targets, pity, summon_set, success#, cumulative_orbs_spent # c_orbs_spent is in summon set


def summon(summon_set, list_summoned, targets, late_five_order, wanted_colors, wanted_order, pity, color_value, target_check): # targs is a dict
    if list_summoned:
        cumulative_orbs_spent = list_summoned[-1][1]
    else:
        cumulative_orbs_spent = 0
    cost = [15, 12, 8, 4]
    temp_pity = pity
    color_count = count_colors(summon_set)
    amount=0
    for color in wanted_colors:
        amount += color_count[color]
    if(amount == 0):
        print("0 in this session")
        list_summoned, targets, pity, summon_set, success = set_pull(summon_set, 1, late_five_order, list_summoned, cumulative_orbs_spent, pity, targets, target_check)
        return list_summoned, targets, pity
    list_summoned, targets, pity, summon_set, success = set_pull(summon_set, amount, wanted_colors, list_summoned, cumulative_orbs_spent, pity, targets, target_check)
    #need to do a target check
    if (success):
        return list_summoned, targets, pity
    cumulative_value=0
    for i in range(len(summon_set)):
        cumulative_value += color_value[summon_set[i][1]]
    if cumulative_value > cost[len(summon_set)]:
        cumulative_orbs_spent = list_summoned[-1][1]
        list_summoned, targets, pity, summon_set, success = set_pull(summon_set, len(summon_set), wanted_order, list_summoned, cumulative_orbs_spent, pity, targets, target_check)
    return list_summoned, targets, pity

def summon_until(rate, three_pool, four_pool, five_pool, focus_pool, list_summoned, targets, late_five_order, wanted_colors, wanted_order, pity, color_value, target_check):
    while (not target_check(targets)):
        #print()
        summon_session = generate_summon_session(rate, three_pool, four_pool, five_pool, focus_pool, pity)
        list_summoned, targets, pity = summon(summon_session, list_summoned, targets, late_five_order, wanted_colors, wanted_order, pity, color_value, target_check)
    return list_summoned, targets, pity



def one_brave_hero(targets):
    return (targets["Lyn_(Brave_Heroes)"] or targets["Ike_(Brave_Heroes)"] or targets["Lucina_(Brave_Heroes)"] or targets["Roy_(Brave_Heroes)"])

def main():
    fname =r"C:\Users\blah\Desktop\python\fe heroes\banner 9 2 17.txt"
    three_pool, four_pool, five_pool, all_heroes = read_banner_no_focus(fname)
    focus_pool = [("Roy_(Brave_Heroes)", "Red"),("Lucina_(Brave_Heroes)", "Blue"),("Ike_(Brave_Heroes)", "Green"),("Lyn_(Brave_Heroes)", "Colorless")]
    normal_banner_rates = [36,58,3,3]
    #normal_banner_rates = [34,58,3,5]
    #summon_session = generate_summon_session(normal_banner_rates, three_pool, four_pool, five_pool, focus_pool)
    #print(summon_session)
    #print(count_colors(summon_session))
    
    list_summoned = []
    targets = {"Roy_(Brave_Heroes)":False,"Lucina_(Brave_Heroes)":False,"Ike_(Brave_Heroes)":False,"Lyn_(Brave_Heroes)":False, "Orb Cost":0}
    late_five_order = ["Colorless", "Blue", "Red", "Green"] 
    wanted_colors = ["Green", "Blue", "Colorless", "Red"]#blue and colorless might be in the wrong order
    wanted_order = late_five_order.reverse()
    pity = 0
    color_value = {"Green":4, "Blue":4, "Colorless":4, "Red":4}
    x = 200
    cumulative_orb_cost = 0
    #loop
    for i in range(x):
        list_summoned, targets, pity = summon_until(normal_banner_rates, three_pool, four_pool, five_pool, focus_pool, list_summoned, targets, late_five_order, wanted_colors, wanted_order, pity, color_value, one_brave_hero)
        
        
        
        
        #get_total_cost
        cumulative_orb_cost += targets["Orb Cost"]
        #reset
        targets = {"Roy_(Brave_Heroes)":False,"Lucina_(Brave_Heroes)":False,"Ike_(Brave_Heroes)":False,"Lyn_(Brave_Heroes)":False, "Orb Cost":0}
        pity = 0
        list_summoned = []

        
    print(cumulative_orb_cost/x," loops ", x)
        
    list_summoned, targets, pity = summon_until(normal_banner_rates, three_pool, four_pool, five_pool, focus_pool, list_summoned, targets, late_five_order, wanted_colors, wanted_order, pity, color_value, one_brave_hero)
    #print(list_summoned)
    #print("Orb Cost ", targets["Orb Cost"])
    
main()

