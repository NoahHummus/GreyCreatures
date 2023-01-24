from pickle import TRUE
import random
import math

class GreyCreature:
    def __init__(self,age=10, health=40, defense=10, sex="male", attack=10,size="medium", speed=10,name="droop",grade="C",level=1):
        self.age = age
        self.health = health
        self.defense = defense
        self.sex = sex
        self.attack = attack
        self.size = size
        self.speed = speed
        self.name = name
        self.grade = grade 
        self.level = level
  #     self.sexuality = sexuality


    def formatcreature(self):
        info = {}
        info.update({"age": self.age})
        info.update({"health": self.health})
        info.update({"defense" : self.defense})
        info.update({"sex" : self.sex})
        info.update({"attack" : self.attack})
        info.update({"size" : self.size})
        info.update({"speed" : self.speed})
        info.update({"name" : self.name})
        info.update({"grade" : self.grade})
        info.update({"level" : self.level})
        return info
    
    def randomizecreature(self):
        sexoption = ["male","female"]
        sizeoptions = ["small", "medium", "large"]
        nameoptions = ["joe", "plum", "ryan", "matt","poop","noah","jack","droop","christian","will","mya"]
        gradeoptions = ["S","A","B","C","D"]
        info = self.formatcreature()
        for key, value in info.items():
            if key == "sex":
                selection = random.choice(sexoption)
                self.sex = selection
                continue
            if key == "size":
                selection = random.choice(sizeoptions)
                self.size = selection
                continue
            if key == "name":
                selection = random.choice(nameoptions)
                self.name = selection
                continue
            if key == "age":
                age = random.randint(3,80)
                self.age = age
                continue
            if key == "health":
                modifier = random.randint(-10,5)
                self.health = value + modifier
            if key == "attack":
                modifier = random.randint(-9,0)
                self.attack = value + modifier
            if key == "defense":
                modifier = random.randint(-9,0)
                self.defense = value + modifier    
            if key == "speed":
                modifier = random.randint(-9,0)
                self.speed = value + modifier   
            if key == "grade":
                selection = random.choice(gradeoptions)
                self.grade = selection     
            if key == "level":
                continue                      
        return self

    def levelupcreature(self):
        info = self.formatcreature()
        for key, value in info.items():
            if key == "sex":
                continue
            if key == "size":
                continue
            if key == "name":
                continue
            if key == "age":
                continue
            if key == "health":
                modifier = random.randint(0,5)
                self.health = value + modifier
            if key == "attack":
                modifier = random.randint(0,1)
                self.attack = value + modifier
            if key == "defense":
                modifier = random.randint(0,1)
                self.defense = value + modifier    
            if key == "speed":
                modifier = random.randint(0,1)
                self.speed = value + modifier       
        info = self.formatcreature()                            
        return info
    

def creatureattack(attacker,target,combatlog):
    defstat = target.defense + 10
    attstat = attacker.attack + 10
    defpercentage = .4 * defstat / (defstat + 8)
    attpercentage = .4 * attstat / (attstat + 8)
    hitroll = random.randint(0,60) 
    attack = math.ceil(random.randint(1,10) * (1+attpercentage))
    if hitroll > 30:
        target.health = target.health - math.trunc((attack - attack*defpercentage))    
        combatstring = f"{attacker.name} did {math.trunc(attack - attack*defpercentage)} damage! {target.name}'s new health : {target.health}"
    else:
        combatstring=  f"{attacker.name} rolled {hitroll} and missed!"
    combatlog.append(combatstring)


        


def creatureduel(g1,g2):
    returndic = {}
    contesters = {}
    combatlog = []
    if g1.speed > g2.speed:
        g1first = True
    if g1.speed < g2.speed:
        g1first = False
    else:
        selection = [1,2]
        choice = random.choice(selection)
        if choice == 1:
            g1first = True
        else:
            g1first = False
    while g1.health > 0 and g2.health > 0:        
        if g1first == True:
            creatureattack(g1,g2,combatlog)
            if g1.health <= 0 or g2.health <= 0:
                break
            creatureattack(g2,g1,combatlog)
        else:
            creatureattack(g2,g1,combatlog)
            if g1.health <= 0 or g2.health <= 0:
                break
            creatureattack(g1,g2,combatlog)
    if g1.health < g2.health:
        contesters.update({"winner" : g2})
        contesters.update({"loser" : g1})
    if g2.health < g1.health:
        contesters.update({"winner" : g1})
        contesters.update({"loser" : g2})
    returndic.update({"contesters" : contesters})
    returndic.update({"combatlog" : combatlog})
    return returndic



            


    
""""

grey1 = GreyCreature(10, 100, 10, "male", 20,"medium",10,"coop","C",1)
grey1info = grey1.formatcreature()






grey2 = GreyCreature(10, 100, 10, "male", 3,"medium",3,"plum","C",1)
grey2info = grey2.formatcreature()



g1wins = 0
g2wins = 0
for i in range(0,1000):
    grey1.health = 40
    grey2.health = 30
    whowon = creatureduel(grey1,grey2)
    if whowon == "g1":
        g1wins += 1
    if whowon == "g2":
        g2wins += 1
for key, value in grey2info.items():
    print(f"{key} : {value}")
print("--------------------------------------------------")
for key, value in grey1info.items():
    print(f"{key} : {value}")

print(f"{grey1.name} : {g1wins} ---- {grey2.name} : {g2wins}")

""""
    










        