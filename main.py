'''
Features:
-summon allies
-fix stealth
-magic types
-enemy types (beast, etc.) and ways to exploit this
-multi-targetting (all, x random, aoe)
-action granularity (ex. heal ally with most missing health, attack enemy prioritizing mages, buff attack on ally with most attack)
!!!!- convert certain functions to classes as necessary (battle handler)


Notes (for future projects):
- Consider the means by which objects will talk to each other. They should be able
to find each other by reference
'''

import random
import math
import time



class Char(object):
    def __init__(self, name, char_class, hp, atk, mag, defense, speed):
        self.name = name
        self.char_class = char_class
        self.atk = atk
        self.mag = mag
        self.hp = hp
        self.maxhp = hp
        self.defense = defense #percentage
        self.gains = [math.ceil(atk/10),math.ceil(mag/10),math.ceil(hp/10)]
        self.lvl = 1
        self.exp = 0
        self.isAlive = True
        self.speed = speed      #10 = max, 0 = min

    def gain_exp(self, xp):
        self.exp += xp
        needexp = self.lvl*100
        while(self.exp > (needexp)):
            self.exp -= needexp
            self.level_up()
            needexp = self.lvl*100

    def level_up(self):
        self.lvl += 1
        self.atk += self.gains[0]
        self.mag += self.gains[1]
        self.maxhp += self.gains[2]
        self.hp += self.gains[2]
        print(self.name+" leveled up!")
        self.show()
        time.sleep(.5)

    def show(self):
        print(self.name+"  lvl:"+str(self.lvl)+" hp:"+
              str(self.hp)+"/"+str(self.maxhp)+" atk:"+
              str(self.atk)+" mag:"+str(self.mag))


class Party(object):

    #putting array outside of init method means that multiple party objects will have references to the same array object
    
    def __init__(self):
        self.chars = []
    
    def add_char(self, char):
        self.chars.append(char)

    def show_party(self):
        for char in self.chars:
            char.show()

party = Party()
char = Char(name="Alistar", char_class="Knight", hp=200, atk=30, mag=10, defense=.7, speed=4)
party.add_char(char)
char = Char(name="Morrigan", char_class="Mage", hp=90, atk=10, mag=50, defense=.3, speed=6)
party.add_char(char)
char = Char(name="Zevran", char_class="Assassin", hp=80, atk=60, mag=20, defense=.2, speed=9)
party.add_char(char)
char = Char(name="Wynne", char_class="Mage", hp=110, atk=15, mag=45, defense=.4, speed=6)
party.add_char(char)
char = Char(name="Shale", char_class="Knight", hp=180, atk=25, mag=15, defense=.8, speed=3)
party.add_char(char)
char = Char(name="Leliana", char_class="Bard", hp=100, atk=25, mag=25, defense=.3, speed=6)
party.add_char(char)
char = Char(name="Edward", char_class="Hexer", hp=110, atk=15, mag=35, defense=.25, speed=7)
party.add_char(char)




class Enemy(object):
      def __init__(self, name, char_class, hp, atk, mag, defense, speed, exp):
        self.name = name
        self.char_class = char_class
        self.atk = atk
        self.mag = mag
        self.hp = hp
        self.maxhp = hp
        self.defense = defense #percentage
        self.speed = speed
        self.exp = exp
        self.isAlive = True
        

      def show(self):
          print(self.name+" hp:"+
                str(self.hp)+"/"+str(self.maxhp)+" atk:"+
                str(self.atk)+" mag:"+str(self.mag))

   

enemies = Party()


def attack_all(party,enemies):
    
    everyone = []

    for char in party:
        pos = 0
        inserted = False
        while(pos < len(everyone)):
            if (char.speed > everyone[pos].speed):
                everyone.insert(pos,char)
                inserted = True
                break
            pos+= 1
        if not inserted:
            everyone.insert(pos,char)

    
    for char in enemies:
        if char.has_taunt > 0:
            char.has_taunt -= 1
        pos = 0
        inserted = False
        while(pos < len(everyone)):
            if (char.speed > everyone[pos].speed):
                everyone.insert(pos,char)
                inserted = True
                break
            pos += 1
        if not inserted:
            everyone.insert(pos,char)

    for char in everyone:

        party_alive = list(filter((lambda x: x.isAlive == True),party))
        if len(party_alive) == 0:
            return "loss"

        enemies_alive = list(filter((lambda x: x.isAlive == True),enemies))
        if len(enemies_alive) == 0:
            return "win"

        
        if char.isAlive:
            decrement_status(char)
            print("\n"*26)
            
            action_chain[char.char_class][char.action_num](char, party_alive, enemies_alive)
            
            if (char.action_num == len(action_chain[char.char_class]) - 1):
                char.action_num = 0
            else:
                char.action_num += 1                    
                
            show_stats(party, enemies)
            time.sleep(1)
            
            
    return "continue"

def decrement_status(char):
    if char.has_stealth > 0:
        char.has_stealth -= 1
    if char.has_taunt > 0:
        char.has_taunt -= 1
    if char.is_poisoned > 0:
        damage = char.poison_damage
        print(char.name+ " is poisoned and takes "+str(damage)+" damage.")
        deal_damage(char, damage)
        char.is_poisoned -= 1
        
    decrement_stat_bonus(char.atk_time, char.atk_bonus)
    decrement_stat_bonus(char.mag_time, char.mag_bonus)
    decrement_stat_bonus(char.defense_time, char.defense_bonus)

def decrement_stat_bonus(time, bonus):
    if time > 0:
        time -= 1
        if time == 0:
            bonus = 0
    

def choose_enemy(char, party, enemies):
    if hasattr(char, "lvl"):
        group = enemies
    else:
        group = party
    return random.choice(apply_taunt(group))

def choose_ally(char, party, enemies):
    if hasattr(char, "lvl"):
        return random.choice(party)
    else:
        return random.choice(enemies)

def choose_enemies(char, party, enemies):
    if hasattr(char, "lvl"):
        return enemies
    else:
        return party

def choose_allies(char, party, enemies):
    if hasattr(char, "lvl"):
        return party
    else:
        return enemies

def apply_taunt(chars):
    result = []
    for char in chars:
        if char.has_taunt > 0:
            result.extend((char,char,char))
        elif char.has_stealth == 0:
            result.append(char)
    return result
                    
def magic(char, party, enemies):
    mag = char.mag + char.mag_bonus
    target = choose_enemy(char, party, enemies)
    damage = mag
    print(char.name+" uses magic on "+target.name+" dealing "+str(damage)+" damage.")
    deal_damage(target, damage)

def attack(char, party, enemies):
    atk = char.atk + char.atk_bonus
    target = choose_enemy(char, party, enemies)
    defense = target.defense + target.defense_bonus
    
    if (char.speed + 20 - target.speed) >= random.randint(0,30):
        damage = math.floor(char.atk*(1 - defense))
        print(char.name+" attacks "+target.name+" dealing "+str(damage)+" damage.")
        deal_damage(target, damage)
    else: print(char.name+" misses "+target.name+"!")


def heal_any(char, party, enemies):
    mag = char.mag + char.mag_bonus
    wounded = []
    allies = choose_allies(char, party, enemies)
    for ally in allies:
        if ally.hp < ally.maxhp:
            wounded.append(ally)
    if len(wounded) == 0:
        print("There was no one for "+char.name+" to heal")
    else:
        target = random.choice(wounded)
        healing = min(mag, target.maxhp - target.hp)
        target.hp += healing
        print(char.name+" heals "+target.name+" restoring "+str(healing)+" HP.")
        

def taunt(char, party, enemies):
    char.has_taunt = 3
    char.has_stealth = 0
    print(char.name+ " shouts, drawing attention.")

def stealth(char, party, enemies):
    char.has_stealth = 3
    char.has_taunt = 0
    print(char.name+ " hides in the shadows.")

def poison(char, party, enemies):
    atk = char.atk + char.atk_bonus
    mag = char.mag + char.mag_bonus
    target = choose_enemy(char, party, enemies)
    target.is_poisoned = 3
    damage = math.floor((atk+mag)/4)   
    target.poison_damage = damage
    print(char.name+ " poisons "+target.name+" dealing "+str(damage)+" damage.")
    deal_damage(target, damage)
        

def deal_damage(target, damage):
    target.hp -= damage
    if target.hp <= 0:
        target.hp = 0
        target.isAlive = False
        clear_status(target)
        print(target.name+ " was killed!")

def buff_mag(char, party, enemies):
    target = choose_ally(char, party, enemies)
    target.mag_time = 3
    target.mag_bonus = math.floor(target.mag*.5)
    print(char.name+ " enchants "+target.name+" improving their magical ability.")

def buff_atk(char, party, enemies):
    target = choose_ally(char, party, enemies)
    target.atk_time = 3
    target.atk_bonus = math.floor(target.atk*.5)
    print(char.name+ " enchants "+target.name+" improving their physical ability.")

def debuff_mag(char, party, enemies):
    target = choose_enemy(char, party, enemies)
    target.mag_time = 3
    target.mag_bonus = -1*math.floor(target.mag*.5)
    print(char.name+ " hexes "+target.name+" reducing their magical ability.")

def debuff_atk(char, party, enemies):
    target = choose_enemy(char, party, enemies)
    target.atk_time = 3
    target.atk_bonus = -1*math.floor(target.atk*.5)
    print(char.name+ " hexes "+target.name+" reducing their physical ability.")    

#characters follow a deterministic chain of actions, but we can start each at an offset
#ACTION CHAIN MUST BE BELOW ALL ACTION METHODS
action_chain = {"Knight": [attack, taunt, attack, heal_any, attack, attack],
                "Mage": [magic, attack, magic, heal_any, magic, attack],
                "Assassin": [attack, magic, poison, attack, poison, attack],
                "Bard": [attack, buff_atk, magic, buff_mag, attack, magic],
                "Hexer": [magic, debuff_mag, attack, debuff_atk, attack, magic]}


class Battle(object):
    def __init__(self, party, enemies):
        self.party = party
        self.enemies = enemies

    def start(self):
        battle_state = "continue"
        
        total_exp = 0
        for char in self.enemies:
            total_exp += char.exp

        while(battle_state == "continue"):
            show_stats(self.party, self.enemies)
            battle_state = attack_all(self.party, self.enemies)

        if battle_state == "loss":
            print("You lost!")
        elif battle_state == "win":
            print("You won and gained "+str(total_exp)+" exp!")
            time.sleep(2.5)
            print("")
            for char in self.party:
                char.hp = char.maxhp
                char.isAlive = True   #heal and revive everyone
                char.gain_exp(total_exp)


def show_stats(party, enemies):
    line_pos = 1
    array = []
    array.append("")
    title = " "*36
    title += "ALLIES"
    array.append(title)
    string = ""
    
    for char in party:
        string += (char.name+": ")
        if char.isAlive:
            string += (str(char.hp)+"/"+str(char.maxhp)+ " ")
        else:
            string += "DEAD"
        if char.has_stealth:
            string += "(_)"
        if char.has_taunt:
            string += "(!)"
        if char.is_poisoned > 0:
            string += "(P)"
        if char.atk_time > 0:
            if char.atk_bonus >0:
                string += "(A+)"
            else:
                string += "(A-)"
        if char.mag_time > 0:
            if char.mag_bonus > 0:
                string += "(M+)"
            else:
                string += "(M-)"
        if char.defense_time > 0:
            if char.defense_bonus > 0:
                string += "(D+)"
            else:
                string += "(D-)"
        string += " "*(line_pos*30 - len(string))
        line_pos += 1
        if line_pos > 3:
            line_pos = 1
            array.append(string)
            string = ""
    array.append(string)
    
    title = " "*36
    
    title += "ENEMIES"
    array.append(title)

    string = ""
    line_pos = 1
    for char in enemies:
        string += (char.name+": ")
        if char.isAlive:
            string += (str(char.hp)+"/"+str(char.maxhp)+ " ")
        else:
            string += "DEAD"
        if char.has_stealth:
            string += "(_)"
        if char.has_taunt:
            string += "(!)"
        if char.is_poisoned > 0:
            string += "(P)"
        if char.atk_time > 0:
            if char.atk_bonus >0:
                string += "(A+)"
            else:
                string += "(A-)"
        if char.mag_time > 0:
            if char.mag_bonus > 0:
                string += "(M+)"
            else:
                string += "(M-)"
        if char.defense_time > 0:
            if char.defense_bonus > 0:
                string += "(D+)"
            else:
                string += "(D-)"
            
        string += " "*(line_pos*30 - len(string))
        line_pos += 1
        if line_pos > 3:
            line_pos = 1
            array.append(string)
            string = ""
    array.append(string)
            
    print("\n".join(array))

    
        
     
        
def start(party, enemies):
    
    while(True):
        enemies.chars = []
        difficulty = party.chars[0].lvl*2
        #name, hp, atk, mag, defense, speed, exp
        for num in range(0,random.randint(difficulty,math.ceil(difficulty*1.5))):
            char = Enemy(name="Goblin", char_class = "Knight", hp=100, atk=10, mag=10, defense=.2, speed=7, exp=10)
            enemies.add_char(char)
        for num in range(0,random.randint(1,difficulty)):
            char = Enemy(name="Troll", char_class = "Hexer", hp=150, atk=35, mag=10, defense=.2, speed=3, exp=25)
            enemies.add_char(char)
        if difficulty > 1:
            char = Enemy(name="SteelGuard", char_class = "Knight", hp=80, atk=12, mag=10, defense=.8, speed=5, exp=30)
            enemies.add_char(char)

        #taunt is decremented every turn down to 0
        for char in party.chars:
            clear_status(char)
        for char in enemies.chars:
            clear_status(char)

        battle = Battle(party.chars,enemies.chars)
        battle.start()

def clear_status(char):
    char.has_taunt = 0
    char.has_stealth = 0
    char.is_poisoned = 0
    char.action_num = random.randint(0,3)
    char.atk_time = 0
    char.atk_bonus = 0
    char.mag_time = 0
    char.mag_bonus = 0
    char.defense_time = 0
    char.defense_bonus = 0
    
        
class Card(object):
    def __init__(self, name, cost, ability, can_target, power):
        self.name = name
        self.cost = cost
        self.ability = ability
        self.can_target = can_target
        self.power = power
        self.in_hand = False

    def use(self):
        if self.can_target == True:
            target_team = int(input("choose a target: 1 = allies 2 = enemies"))
            while(target_team != 1 or target_team != 2):
                target_team = int(input("Invalid selection: 1 = allies 2 = enemies"))
            
                
        print("You used "+self.name)

    def show(self):
        return "("+str(self.cost)+")"+self.name



class Hand(object):
    hand = []

    def show(self):
        cards = []
        num = 1
        for card in self.hand:
            line = str(num)+". "       
            line += card.show()
            cards.append(line)
            num +=1
        print("\n".join(cards))

    def add_card(self, card):
        self.hand.append(card)

    def choose_card(self):
        mana = 20
        while(True):
            self.show()
            print("mana: "+str(mana))
            num = int(input("Choose a card (enter 0 to end turn): "))
            while not(num > -1 and num <= len(self.hand)):
                num = int(input("Invalid selection. Choose a card: "))
            if num == 0:
                break
            else:
                card = self.hand[num-1]
                if card.cost <= mana:
                    mana -= card.cost
                    card.use()
                    card.in_hand = False
                    self.hand.remove(card)
                else:
                    print("Not enough mana")
        

        

class Deck(object):
    all_cards = []
    in_deck = []

    def __init__(self):
        self.hand = Hand()

    def draw(self, hand):
        pass

hand = Hand()
for i in range(0, 2):
    card = Card(name = "Fireball", cost = 5, ability = "spell", can_target = True, power = 50)
    hand.add_card(card)
for i in range(0, 2):
    card = Card(name = "Bomb", cost = 8, ability = "spell", can_target = True , power = 50)
    hand.add_card(card)
        
#hand.choose_card()



start(party, enemies)


    
  
    
