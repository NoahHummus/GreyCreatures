from pickle import NONE, TRUE
#from readline import insert_text
from urllib import response
import sqlite3
import random
import datetime
import math
import logging
from creature import *
import lightbulb
import hikari


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='main.log', encoding='utf-8', level=logging.DEBUG)


class Database:
    def __init__(self):
        self.connect()
        
        

        self.query_insert_user = "INSERT INTO users ('USER_NAME','GREY_FLAKES','lastworked', levelxp) VALUES (?, ?, ?, ?)"

        self.query_select_user_gf = "SELECT GREY_FLAKES FROM users WHERE USER_NAME=?"

        self.query_select_one_user = "SELECT GREY_FLAKES, lastworked, levelxp, bank, lastslot, lastdaily, lastrob FROM users WHERE USER_NAME=?"

        self.query_select_user_xp = "SELECT levelxp FROM users WHERE USER_NAME=?"

        self.query_select_lastworked = "SELECT lastworked FROM users WHERE USER_NAME=?"

        self.query_select_jackpot = "Select VALUE from jackpot WHERE NAME='jackpot'"

        self.query_select_flake_leaderboard = "SELECT USER_NAME, GREY_FLAKES FROM users ORDER BY GREY_FLAKES DESC"

        self.query_select_xp_leaderboard = "SELECT USER_NAME, levelxp FROM users ORDER BY levelxp DESC"

        self.query_transfer_bank = "UPDATE users SET GREY_FLAKES=?, bank=? WHERE USER_NAME=?"

        self.query_update_slot = "UPDATE users SET GREY_FLAKES=?, lastslot=? WHERE USER_NAME=?"

        self.query_update_user_2 = "UPDATE users SET GREY_FLAKES=?, levelxp=? WHERE USER_NAME=?"

        self.query_update_user_f = "UPDATE users SET GREY_FLAKES=? WHERE USER_NAME=?"

        self.query_update_jackpot = "UPDATE jackpot set VALUE=? WHERE NAME='jackpot'"

        self.query_update_user = "UPDATE users SET GREY_FLAKES=?, lastworked=?, levelxp=? WHERE USER_NAME=?"

        self.query_update_lastrob = "UPDATE users SET lastrob=? WHERE USER_NAME=?"

        self.query_update_lastdaily = "UPDATE users SET lastdaily=? WHERE USER_NAME=?"

        self.query_update_single_flakes = "UPDATE users SET GREY_FLAKES=? WHERE USER_NAME=?" 

        self.query_update_single_xp = "UPDATE users SET levelxp=? WHERE USER_NAME=?" 


        #-----------------------------------------------------------------CREATURES-----------------------------------------------------------

        self.query_insert_creature = "INSERT INTO creatures (USER_NAME, C_NAME, AGE, SEX, SIZE, HEALTH, DEFENSE, SPEED, ATTACK, ALIVE, MAIN, GRADE, LASTYIELD, LEVEL, KILLS) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

        self.query_update_creaturedeath = "UPDATE users SET lastcreaturedeath=? WHERE USER_NAME=?"

        self.query_update_lastattack = "UPDATE users SET lastattack=? WHERE USER_NAME=?"

        self.query_select_users_main_creature = "SELECT USER_NAME, C_NAME, AGE, SEX, SIZE, HEALTH, DEFENSE, SPEED, ATTACK, ALIVE, MAIN, GRADE, LASTYIELD, CREATURE_ID, LEVEL FROM creatures WHERE USER_NAME = ? and ALIVE ='Y' and MAIN ='Y'"

        self.query_select_creature = "SELECT USER_NAME, C_NAME, AGE, SEX, SIZE, HEALTH, DEFENSE, SPEED, ATTACK, ALIVE, MAIN, GRADE, LASTYIELD, CREATURE_ID, LEVEL, KILLS FROM creatures WHERE c_name = ?"

        self.query_select_alive_creatures = "SELECT USER_NAME, C_NAME, AGE, SEX, SIZE, HEALTH, DEFENSE, SPEED, ATTACK, ALIVE, MAIN, GRADE, LASTYIELD, CREATURE_ID, LEVEL FROM creatures where ALIVE = 'Y'"

        self.query_select_creature_list = "SELECT USER_NAME, C_NAME, KILLS FROM creatures where ALIVE = 'Y' ORDER BY KILLS DESC"

        self.query_select_creaturedeath = "SELECT lastcreaturedeath from users WHERE USER_NAME=?"

        self.query_select_lastattack = "SELECT lastattack from users WHERE USER_NAME=?"

        self.query_select_username = "SELECT user_name from creatures where c_name = ?"

        self.query_select_creature_name = "Select c_name from creatures where c_name =?"

        self.query_update_creaturelastyield = "UPDATE creatures SET LASTYIELD=? WHERE USER_NAME = ? and ALIVE='Y' and MAIN='Y'"

        self.query_update_kill_creature = "UPDATE creatures SET ALIVE='N', MAIN='N' WHERE c_name = ?"

        self.query_select_creature_kill_count = "SELECT KILLS from creatures WHERE c_name = ?"

        self.query_update_creature_kill_count = "UPDATE creatures SET KILLS=? WHERE c_name = ?"



        self.query_select_top_10_creatures = "SELECT USER_NAME, C_NAME, KILLS, ALIVE FROM creatures ORDER BY KILLS DESC LIMIT 10"
        
    #--------------------------------------------------------------flake history----------------------------------------

        self.query_select_max_flakes = "SELECT USER_NAME, MAX(Grey_flakes) from users"

        self.query_select_flake_highscore = "SELECT USER_NAME, MAX(GREY_FLAKES), Entrydate from flakehistory"

        self.query_insert_flake_highscore = "insert into flakehistory (user_name, Grey_flakes, Entrydate) VALUES (?,?,?)"

    #--------------------------------------------------------------combatlog----------------------------------------   

        self.query_update_creature_killedby = "UPDATE creatures SET KILLEDBY=?, DEATHLOG= ? WHERE c_name = ?"
        
    def get_flake_highscore(self):
        info = []
        query = self.query_select_flake_highscore
        self.cur.execute(query)
        result = self.cur.fetchone() 
        if result :
            info.update({"user" : result[0]})
            info.update({"flakes" : result[1]})
            info.update({"entrydate": result[2]})
        return result


    def get_max_currentflakes(self):
        info = []        
        query = self.query_select_max_flakes
        self.cur.execute(query)
        result = self.cur.fetchone() 
        if result :
            info.update({"user" : result[0]})
            info.update({"flakes" : result[1]})
            info.update({"entrydate": result[2]}) 

    def insert_into_flakehistory(self,user,flakes):
        query = self.query_insert_flake_highscore
        self.cur.execute(query, (str(user), flakes, datetime.datetime.now()))

    def check_highscore(self):
        currentresult = self.get_max_currentflakes
        highscoreresult = self.get_flake_highscore
        highscore = highscoreresult.get("flakes")
        currentflakes = currentresult.get("flakes")
        if currentflakes > highscore:
            self.insert_into_flakehistory(currentresult.get("user"), currentflakes)




    


    #----------------------------------------    ---------------creature--------    ----------------------------------------    
    def select_creature_kill_count(self,name):
        query = self.query_select_creature_kill_count
        self.cur.execute(query, [name.upper()])
        count = self.cur.fetchone()
        return count[0]

    def modify_creature_kill_count(self,name,amount):
        currentcount = self.select_creature_kill_count(name)
        newcount = currentcount + amount
        query = self.query_update_creature_kill_count
        self.cur.execute(query, (newcount, name.upper()))
        self.con.commit()      

    def select_lastattack(self,user):
        query = self.query_select_lastattack
        self.cur.execute(query, [str(user)])
        return self.cur.fetchone() 
          
    def update_lastattack(self,user):
        query = self.query_update_lastattack
        self.cur.execute(query, (datetime.datetime.now(), str(user)))
        self.con.commit()

    def select_creature_name(self,name):
        query = self.query_select_creature_name
        self.cur.execute(query, [str(name)])
        return self.cur.fetchone() 


    def get_creature_owner(self,name):
        query = self.query_select_username
        self.cur.execute(query, [str(name)])
        owner = self.cur.fetchone() 
        return owner[0]


    def select_all_creatures(self):
        query = self.query_select_alive_creatures
        self.cur.execute(query)
        return self.cur.fetchall()

    def select_creaturedeath(self,user):
        query = self.query_select_creaturedeath
        self.cur.execute(query, [str(user)])
        return self.cur.fetchone() 
    
    def update_creaturedeath(self,user):
        query = self.query_update_creaturedeath
        self.cur.execute(query, (datetime.datetime.now(), str(user)))
        self.con.commit()

    def update_creaturelastyield(self,user):
        query = self.query_update_creaturelastyield
        self.cur.execute(query, (datetime.datetime.now(), str(user)))
        self.con.commit()

    def killcreature(self,name):
        query = self.query_update_kill_creature
        self.cur.execute(query, [str(name)])
        self.con.commit()

    def get_alive_creatures(self):
        self.select_all_creatures_A()
        
    def euthanize_creature(self,user,name):
        message = {}
        creatureinfo = self.select_creature(name)
        creaturename = creatureinfo.get("name") 
        if creatureinfo:
            if creatureinfo.get("user_name") != str(user):
                response = f"{name} dosn't belong to you!"
                message.update({"notowner" : response})
                return message
            if creatureinfo.get("Alive") == "N":
                response = f"{creaturename} is already dead. RIP."
                message.update({"notalive" : response})
                return message
            self.killcreature(name)
            response = f"{creaturename} has been unalived. SHEESH"
            message.update({"success" : response})
            return message
        else:
            response = f"{name} does not exist!"
            message.update({"notexist" : response})        
            return message

        
            


    def farmcreature(self,user):
        message = {}
        record = self.select_main_creature(user)     
        if record:
            lastyield = record.get("lastyield")
            timetill = datetime.datetime.now() - datetime.datetime.fromisoformat(lastyield)
            if timetill.total_seconds() >= 600:
                numberofcycles = math.trunc(timetill.total_seconds() / 600)
                if numberofcycles > 48:
                    numberofcycles = 48
                numberofloops = 0
                harvest = 0
                while numberofloops < numberofcycles:
                    numberofloops += 1
                    tempyield = random.randint(50, 200)
                    harvest += tempyield
                self.update_creaturelastyield(user)
                userrecord = self.select_one_user(user)
                currentflakes = userrecord[0]
                currentxp = userrecord[2]
                newflakes = currentflakes + harvest
                newxp = currentxp + 5
                self.update_user2(newflakes, newxp, user)
                response = f"You just scraped {harvest} flakes from your Grey Creature. It's all good tho, we're pretty sure they don't feel pain."
                message.update({"success" : response})
            else:
                remainingseconds = 600 - timetill.total_seconds()
                cooldown = math.trunc(remainingseconds / 60)
                response = f"You'll need to wait {int(cooldown)} minutes before you can harvest (Grey creatures can be harvested every 10 minutes. Stacks up to 8 hours)."
                message.update({"tooearly" : response})  
        else:
            response = f"You need to get your hands on a creature first! /plant"
            message.update({"nocreature" : response})
        return message

                


    def plantcreature(self,user,name):
        cost = -2500
        check = 2500
        message = {}
        userinfo = self.get_user_info(user)
        if userinfo:
            record = self.select_main_creature(user)
            if record:
                response = "You can only have one creature alive at a time dawg (for now)"
                message.update({"limitreached" : response})
                return message
            else:
                result = self.select_creaturedeath(user)
                lastdeath = result[0]
                if lastdeath is None:
                    lastdeath = '2022-05-31 18:42:47.032430'
                timetilllastdeath = datetime.datetime.now() - datetime.datetime.fromisoformat(lastdeath)
                if userinfo.get("grey_flakes") < check:
                    flakesremaining = check - userinfo.get("grey_flakes") 
                    response = f"You need {flakesremaining} more flakes to grow a creature"
                    message.update({"insufficientfunds" : response})
                    return message
                if timetilllastdeath.total_seconds() >= 300:            
                    self.insertnewcreaturedb(user,name)
                    self.modify_flakes(user,cost)
                    response = f"{name.upper()} has been birthed into this world. /creatureinfo to check your creature out. (costed ya 2500 flakes)"
                    message.update({"spawned" : response})
                    return message
                else:
                    secondsremaining = 300 - timetilllastdeath.total_seconds()
                    cooldown = secondsremaining / 60
                    response = f"You'll need to wait {int(cooldown)} minutes before you can get your shiny new goober."
                    message.update({"oncooldown" : response})
                    return message
        else:
            response = "you gotta /work first!"
            message.update({"nowork" : response})
        return message


    def insertnewcreaturedb(self,user,name):
        query = self.query_insert_creature
        creature = self.createcreature()
        info = creature.formatcreature()
        info.update({"MAIN" : "Y"})
        info.update({"lastyield" : datetime.datetime.now()})
        info.update({"alive" : "Y"})
        info.update({"name" : name})
        self.cur.execute(query, (str(user), info.get("name"),info.get("age"), info.get("sex"), info.get("size"), info.get("health"), info.get("defense"), info.get("speed"), info.get("attack"), info.get("alive"), info.get("MAIN"), info.get("grade"), info.get("lastyield"),info.get("level"),0))
        self.con.commit()


    def createcreature(self):
        default = GreyCreature()
        return default.randomizecreature()  

    def select_main_creature(self,user):
        info = {}
        query = self.query_select_users_main_creature
        self.cur.execute(query, [str(user)])
        result = self.cur.fetchone()
        if result :
            info.update({"user_name" : result[0]})
            info.update({"name" : result[1]})
            info.update({"age": result[2]})
            info.update({"sex" : result[3]})    
            info.update({"size" : result[4]})
            info.update({"health": result[5]})
            info.update({"defense" : result[6]})
            info.update({"speed" : result[7]})
            info.update({"attack" : result[8]})     
            info.update({"alive" : result[9]})   
            info.update({"MAIN" : result[10]}) 
            info.update({"grade" : result[11]})
            info.update({"lastyield" : result[12]})
            info.update({"creatureid" : result[13]})
            info.update({"level" : result[14]})
        return info

    def select_creature(self,name):
        info = {}
        query = self.query_select_creature
        self.cur.execute(query, [str(name)])
        result = self.cur.fetchone()
        if result :
            info.update({"user_name" : result[0]})
            info.update({"name" : result[1]})
            info.update({"age": result[2]})
            info.update({"sex" : result[3]})    
            info.update({"size" : result[4]})
            info.update({"health": result[5]})
            info.update({"defense" : result[6]})
            info.update({"speed" : result[7]})
            info.update({"attack" : result[8]})     
            info.update({"alive" : result[9]})   
            info.update({"MAIN" : result[10]}) 
            info.update({"grade" : result[11]})
            info.update({"lastyield" : result[12]})
            info.update({"creatureid" : result[13]})
            info.update({"level" : result[14]})
            info.update({"kills" : result[15]})
        return info

    def retrieve_creature(self,user):
        info = self.select_main_creature(user)
        return GreyCreature(info.get("age"), info.get("health"), info.get("defense"), info.get("sex"), info.get("attack"), info.get("size"), info.get("speed"),info.get("name"),info.get("grade"),info.get("level"))

    def retrieve_creature_byname(self,name):
        info = self.select_creature(name)
        return GreyCreature(info.get("age"), info.get("health"), info.get("defense"), info.get("sex"), info.get("attack"), info.get("size"), info.get("speed"),info.get("name"),info.get("grade"),info.get("level"))


    def creature_dueldb(self,user,target):
        bountyreward = 1000
        returndic = {}
        message = {}
        usercheck = self.select_main_creature(user)
        targetcheck = self.select_main_creature(target)
        result = self.select_lastattack(user)
        lastattack = result[0]
        if lastattack is None:
            lastattack = '2022-05-31 18:42:47.032430'
        timetilllastattack = datetime.datetime.now() - datetime.datetime.fromisoformat(lastattack)
        if timetilllastattack.total_seconds() < 900:   
            secondsremaining = 900 - timetilllastattack.total_seconds()
            cooldown = secondsremaining / 60
            response = f"You'll need to wait {int(cooldown)} minutes until you can attack again."
            message.update({"oncooldown" : response})
            returndic.update({"message" : message})
            return returndic        
        if str(user) == str(target):
            response = "You can't make your creature fight itself you monster! (/Euthanize them)"
            message.update({"targetself" : response})
            returndic.update({"message" : message})
            return returndic
        if not usercheck:
            response = f"You don't have a creature that can fight!"
            message.update({"nousercreature" : response})
            returndic.update({"message" : message})
            return returndic
        if not targetcheck:
            response = f"{target} does not have a creature that can fight!"
            message.update({"notargetcreature" : response})
            returndic.update({"message" : message})
            return returndic  
        usercreature = self.retrieve_creature(user)
        targetcreature = self.retrieve_creature(target)      
        duelresults = creatureduel(usercreature,targetcreature)
        contesters = duelresults.get("contesters")
        combatlog = duelresults.get("combatlog")
        combattext = '\n'.join(combatlog)
        winner = contesters.get("winner")
        loser = contesters.get("loser")
        loserusername = self.get_creature_owner(loser.name)
        winnerusername = self.get_creature_owner(winner.name)
        self.killcreature(loser.name)
        self.modify_creature_kill_count(winner.name,1)
        bountystacks = self.select_creature_kill_count(loser.name)
        bounty = bountystacks * bountyreward
        reward = 2500 + bounty
        response = f"{winner.name} just fucking MURDERED {loser.name}. {winnerusername} butchered the living fuck out of {loser.name} and got 2500 flakes! {loser.name} had {bountystacks} confirmed kills, thats a {bounty} flake bounty!"
        message.update({"success" : response})
        self.update_creaturedeath(loserusername)
        self.update_lastattack(user)
        self.modify_flakes(winnerusername,reward)
        returndic.update({"message" : message})
        returndic.update({"combattext" : combattext})
        return returndic

        

        
   #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def modify_flakes(self,user,amount):
        info = self.get_user_info(user)
        currentflakes = info.get("grey_flakes")
        newflakes = currentflakes + amount
        query = self.query_update_single_flakes
        self.cur.execute(query, (newflakes, str(user)))
        self.con.commit()   


    def modify_xp(self,user,amount):
        info = self.get_user_info(user)
        currentxp = info.get("levelxp")
        newxp = currentxp + amount
        query = self.query_update_single_xp
        self.cur.execute(query, (newxp, str(user)))
        self.con.commit()   

    def get_user_info(self,user):
        info = {}
        query = self.query_select_one_user
        self.cur.execute(query, (str(user),))
        results = self.cur.fetchone()      
        grey_flakes = results[0]
        lastworked = results[1]
        levelxp = results[2]
        bank = results[3]
        lastslot = results[4]
        lastdaily = results[5]
        lastrob = results[6]
        info.update({"grey_flakes": grey_flakes})
        info.update({"lastworked": lastworked})
        info.update({"levelxp": levelxp})
        info.update({"bank": bank})
        info.update({"lastslot": lastslot})
        info.update({"lastdaily": lastdaily})
        info.update({"lastrob": lastrob})
        return info
        
           


    def connect(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()

    def update_lastrob(self,user):
        query = self.query_update_lastrob
        self.cur.execute(query, (datetime.datetime.now(), str(user)))
        self.con.commit()

    def update_lastdaily(self,user):
        query = self.query_update_lastdaily
        self.cur.execute(query, (datetime.datetime.now(),str(user)))
        self.con.commit()

    def select_jackpot(self):
        query = self.query_select_jackpot
        self.cur.execute(query)
        results = self.cur.fetchone()
        return results

    def clear_jackpot(self):
        query = self.query_update_jackpot
        self.cur.execute(query, 0)
        self.con.commit()

    def update_jackpot(self,amount):
        currentvalue = self.select_jackpot()
        newvalue = int(currentvalue[0]) + amount
        query = self.query_update_jackpot
        self.cur.execute(query, newvalue)
        self.con.commit()

    def select_one_user(self, user):
        query = self.query_select_one_user

        self.cur.execute(query, (str(user),))

        results = self.cur.fetchone()
        return results

    def update_user(self, flakes, xp, user):
        query = self.query_update_user
        self.cur.execute(
        query, (flakes, datetime.datetime.now(), xp, str(user)))
        self.con.commit()

    def update_user2(self, flakes, xp, user):
        query = self.query_update_user_2
        self.cur.execute(query, (flakes, xp, str(user)))
        self.con.commit()

    def update_user_f(self, flakes, user):
        query = self.query_update_user_f
        self.cur.execute(query, (flakes, str(user)))
        self.con.commit()    

    def insert_user(self, user, flakes,):
        query = self.query_insert_user
        self.cur.execute(
            query, (str(user), flakes, datetime.datetime.now(), 5))
        self.con.commit()

    def transfer_bank(self, user, flakes, bank):
        query = self.query_transfer_bank
        self.cur.execute(query, (flakes, bank, user))

    def update_slot(self, flakes, user):
        query = self.query_update_slot
        self.cur.execute(query, (flakes, datetime.datetime.now(), str(user)))

    def workdb(self, user):
        workyield = random.randint(1, 350)
        result = self.select_one_user(user)
        if result:
            currentflakes = result[0]
            lastworked = result[1]
            currentxp = result[2]
            newflakevalue = workyield+currentflakes
            newxpvalue = currentxp + 5
            logging.debug(f'[workdb] user {user} results from select_one_user - current flakes : {currentflakes}, last worked: {lastworked}, currentxp : {currentxp}.')
            if lastworked is None:
                lastworked = '2022-05-31 18:42:47.032430'
            timetilllastworked = datetime.datetime.now(
            ) - datetime.datetime.fromisoformat(lastworked)
            if timetilllastworked.total_seconds() >= 300:
                self.update_user(newflakevalue, newxpvalue, user)
                response = f"You've recieved {workyield} Grey Flakes!"
                return response
            else:
                cooldown = 300 - timetilllastworked.total_seconds()
                response = f"You'll need to wait {int(cooldown)} more seconds before you can get more flakes."
                return response
        else:
            self.insert_user(user, workyield)
            response = f"You've recieved {workyield} Grey Flakes!"
            return response



    def slotdb(self, user,amount):
        result = self.select_one_user(user)
        if result:
            flakesinwallet = result[0]
            currentxp = result[2]
            newxpvalue = currentxp + 0
            newflakesinwallet = flakesinwallet - amount
            if amount > 0 :
                if newflakesinwallet >= 0:
                    slotresult = self.slotcalc(amount)
                    if slotresult.get("winresponse"):
                        reward = slotresult.get("reward")
                        newflakesinwallet = flakesinwallet + reward
                        self.update_user2(newflakesinwallet, newxpvalue, user)
                        return slotresult.get("winresponse")               
                    if slotresult.get("lossresponse"):
                        self.update_user2(newflakesinwallet, newxpvalue, user)
                        return slotresult.get("lossresponse")                    
                else:
                    remaining = amount - flakesinwallet
                    response = f"Sorry, you'd need {remaining} more flakes to bet that amount."
                    return response
            else :
                response = "you gotta bet something dawg."
                return response
        else:
            response = "you need to work first dawg."
            return response

    def slotcalc(self,amount):
        slotresult = {}
        slotselection = ["blue", "red", "red", "green", "green", "green", "yellow", "yellow", "yellow", "yellow"]
        row1 = random.choice(slotselection)
        row2 = random.choice(slotselection)
        row3 = random.choice(slotselection)
        roll = f"{row1} : {row2} : {row3}"
        slotresult.update({"roll" : roll})
        slotresult.update({"gate" : "gate"})
        emojikey = {"green" : ":green_square:", "red" : ":red_square:", "yellow" : ":yellow_square:", "blue" : ":blue_square:"}
        if row1 == row2 and row2 == row3:
            win = row1
            if win == "blue":
                multiplier = 20
                reward = amount * multiplier
                response = f"[{emojikey.get(row1)} : {emojikey.get(row2)} : {emojikey.get(row3)}] ---- ALL {win}, .01% chance! You won {reward} flakes (you bet {amount})"
                slotresult.update({"winresponse" : response})
                slotresult.update({"reward" : reward})
            if win == "red":
                multiplier = 16
                reward = amount * multiplier
                response = f"[{emojikey.get(row1)} : {emojikey.get(row2)} : {emojikey.get(row3)}] ---- ALL {win}, .08% chance! You won {reward} flakes (you bet {amount})"
                slotresult.update({"winresponse" : response})
                slotresult.update({"reward" : reward})
            if win == "green":
                multiplier = 12
                reward = amount * multiplier
                response = f"[{emojikey.get(row1)} : {emojikey.get(row2)} : {emojikey.get(row3)}] ---- ALL {win}, 2.7% chance! You won {reward} flakes (you bet {amount})"
                slotresult.update({"winresponse" : response})
                slotresult.update({"reward" : reward})
            if win == "yellow":
                multiplier = 6.6875
                reward = amount * multiplier
                rewardflattened = math.trunc(reward)
                response = f"[{emojikey.get(row1)} : {emojikey.get(row2)} : {emojikey.get(row3)}] ---- ALL {win}, 6.4% chance! You won {rewardflattened} flakes (you bet {amount})"
                slotresult.update({"winresponse" : response})
                slotresult.update({"reward" : rewardflattened})
        else:
            response = f"[{emojikey.get(row1)} : {emojikey.get(row2)} : {emojikey.get(row3)}] ---- You just lost {amount} grey flakes"
            slotresult.update({"lossresponse" : response})
        return slotresult

    def doubleornothingdb(self,user):
        result = self.select_one_user(user)
        if result:
            flakesinwallet = result[0]
            currentxp = result[2]
            newflakevalue = flakesinwallet * 2
            newxpvalue = currentxp + 5
            if flakesinwallet > 0:
                percentage = random.randint(0,100)
                logging.debug(f"[doubleornothingdb] {user} rolled {percentage} on doubleornothing")
                logging.debug(f"[doubleornothingdb] user {user} results from select_one_user - current flakes : {flakesinwallet}, currentxp : {currentxp}.")
                if percentage >= 50:
                    self.update_user2(newflakevalue, newxpvalue, user)
                    response = f"{user} just doubled their flakes!!! up to {newflakevalue} flakes."
                    return response
                else: 
                    self.update_user2(0, newxpvalue, user)
                    response = f"{user} just LOST all of their precious fucking GREY FLAKES. {flakesinwallet} flakes."
                    return response
            else:
             response = "0 * 2 is 0, i think."
            return response
        else:
            response = "you need to work first dawg."
            return response
    
    def dailydb(self,user):
        daily_yield = random.randint(2500,3000)
        result = self.select_one_user(user)
        if result:
            currentflakes= result[0]
            currentxp = result[2]
            lastdaily = result[5]
            newflakevalue = currentflakes + daily_yield
            newxpvalue = currentxp + 25
            if lastdaily is None:
                lastdaily = '2022-05-31 18:42:47.032430'
            timetilllastdaily = datetime.datetime.now(
            ) - datetime.datetime.fromisoformat(lastdaily)
            if timetilllastdaily.total_seconds() >= 86400 :
                self.update_user2(newflakevalue, newxpvalue, user)
                self.update_lastdaily(user)
                response = f"You've recieved {daily_yield} Grey Flakes!"
                return response
            else:
                secondsremaining = 86400 - timetilllastdaily.total_seconds()
                cooldown = secondsremaining / 3600
                if cooldown <= 1:
                    cooldown = secondsremaining / 60
                    return f"You'll need to wait {int(cooldown)} minutes before you can get your daily."
                response = f"You'll need to wait {int(cooldown)} hours before you can get your daily."
                return response

    def giveflakes(self,user,target,amount):
        user_r = self.select_one_user(user)
        if user_r:
            userflakes = user_r[0]
        else: 
            response = f"{user} needs to /work!"
            return response
        target_r = self.select_one_user(target)
        if target_r:
            targetflakes = target_r[0]
        else:
            response = f"{target} needs to /work!"
            return response
        if str(user) == str(target):
            response = "you can't target yourself"
            return response            
        if amount >= 1:
            if userflakes >= amount:
                newtargetflakes = targetflakes + amount
                newuserflakes = userflakes - amount
                self.update_user_f(newtargetflakes, target)
                self.update_user_f(newuserflakes, user)
                response = f"{user} has given {target} {amount} flakes"
                return response
            else:
                response = "You ain't got enough flakes."
                return response
        else:
            response = "/rob if you wanna steal"   
            return response 



    def robdb(self,user,target):
        user_r = self.select_one_user(user)
        if user_r:
            userflakes = user_r[0]
            userlastrob = user_r[6]
        else: 
            response = f"{user} needs to /work!"
            return response
        target_r = self.select_one_user(target)
        if target_r:
            targetflakes = target_r[0]
        else:
            response = f"{target} needs to /work!"
            return response      
        if userlastrob is None:
            userlastrob = '2022-05-31 18:42:47.032430'
        timetilllastrob = datetime.datetime.now() - datetime.datetime.fromisoformat(userlastrob)
        if str(user) == str(target):
            response = "you can't target yourself"
            return response
        if timetilllastrob.total_seconds() >= 7200 :
            if targetflakes >= 100:
                self.update_lastrob(user)
                firstroll = random.randint(0,100)
                logging.debug(f"[robdb] {user} rolled {firstroll} to rob")
                print(firstroll)
                if firstroll <= 20:
                    secondroll = random.randint(10,15)
                    multstr = f"0.{secondroll}"
                    multiplier = float(multstr)
                    robbed = math.trunc((targetflakes * multiplier)/2)
                    newtargetflakes = targetflakes - robbed
                    newuserflakes = userflakes + robbed
                    self.update_user_f(newtargetflakes, target)
                    self.update_user_f(newuserflakes, user)
                    response = f"{user} just stole {robbed} flakes from <@{target.id}>"
                    print(multiplier)
                    print(robbed)
                    return response
                else:
                    newuserflakes = userflakes - 250
                    self.update_user_f(newuserflakes, user)
                    response = f"The fuzz caught you slippin! You've coughed up 250 grey backs to keep your a$$ out the slammer"
                    return response 
            else:              
                response = f"The target needs to have at least 100 flakes to be robbed."
                return response
        else:
            secondsremaining = 7200 - timetilllastrob.total_seconds()
            cooldown = secondsremaining / 60
            response = f"You'll need to wait {int(cooldown)} minutes before you can rob again."
            return response
        

    def slotinfo(self):
        info = [
        "Blue   : Payouts -> x20 , Odds - > 0.1%",
        "Red    : Payouts -> x16 , Odds - > 0.8%",
        "Green  : Payouts -> x12 , Odds - > 2.7%",
        "Yellow : Payouts -> x6.6875 , Odds - > 6.4%"
        ]
        text = '\n'.join(info)
        return text

    def creatureinfodb(self,name):
        rowlist = []
        check = self.select_creature(name)
        if not check:
            return "fail"
        kills = check.get("kills")
        alive = check.get("alive")
        creature = self.retrieve_creature_byname(name)
        info = creature.formatcreature()
        info.update({"confirmed kills" : kills})
        info.update({"alive" : alive})
        for key, value in info.items():
            if key == "name":
                name = value
                continue
            rowlist.append(f"{key} : {value}")
        text = '\n'.join(rowlist)
        return text, name

    def creaturelistdb(self):
        rowlist = []
        for row in self.cur.execute(self.query_select_creature_list):
            rowlist.append(f"{row[1].upper()} : {row[0]} : {row[2]}")
        text = '\n'.join(rowlist)
        return text

    def creaturelist_top10_db(self):
        rowlist = []
        for row in self.cur.execute(self.query_select_top_10_creatures):
            rowlist.append(f"{row[1].upper()} ({row[3]}) : {row[0]} : {row[2]} ")
        text = '\n'.join(rowlist)
        return text

    def flakeleaderboard(self):
        rowlist = []
        for row in self.cur.execute(self.query_select_flake_leaderboard):
            rowlist.append(f"{row[0]} : {(format (row[1], ',d'))}")
        text = '\n'.join(rowlist)
        return text

    def xpleaderboard(self):
        rowlist = []
        for row in self.cur.execute(self.query_select_xp_leaderboard):
            rowlist.append(f"{row[0]} : {row[1]}")
        text = '\n'.join(rowlist)
        return text

