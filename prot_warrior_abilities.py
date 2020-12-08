# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 02:09:45 2020

@author: Andrew

Contains all the abilities and the stat percentage calculations for a prot warrior.
Resources and cooldowns are calculated in the sim script itself

Current as of PRE-NATHRIA 9.0.2 (2020-12-07)
"""

def rating_to_percent(rating,scale_factor):
    # check if the rating by itself is higher under the first breakpoint
    
    if rating <= 30*scale_factor:
        return rating/scale_factor
    
    elif rating <= 39*scale_factor:
        t_rating = (rating - 30*scale_factor)/scale_factor
        t_rating *= 0.9
        
        return t_rating + 30
    
    elif rating <= 47*scale_factor:
        t_rating = (rating - 39*scale_factor)/scale_factor
        t_rating *= 0.8
        
        return t_rating + 39
    
    elif rating <= 54*scale_factor:
        t_rating = (rating - 47*scale_factor)/scale_factor
        t_rating *= 0.7
        
        return t_rating + 47
    
    elif rating <= 66*scale_factor:
        t_rating = (rating - 54*scale_factor)/scale_factor
        t_rating *= 0.6
        
        return t_rating + 54
    
    elif rating <= 126*scale_factor:
        t_rating = (rating - 66*scale_factor)/scale_factor
        t_rating *= 0.5
        
        return t_rating + 66
    
    else:
        # 126 is the max percent value of secondaries you can have in SL
        return 126
    
class warrior:
    
    def __init__(self,stats=None):
        if stats is not None:
            self.haste = stats['haste']
            self.crit = stats['crit']
            self.mastery = stats['mastery']
            self.vers = stats['vers']
            self.strength = stats['strength']
            self.wdps = stats['wdps']
            self.spec=stats['spec']
        else:
            print('Bad initialization')
            
    def get_haste_percent(self,scale_factor=33):
        return rating_to_percent(self.haste,scale_factor)
    
    def get_crit_percent(self,scale_factor=35):
        return rating_to_percent(self.crit,scale_factor)
    
    def get_mastery_percent(self,scale_factor=35):
#        mastery_scales = {'prot':23.33,'arms':31.82,'fury':24}
        return 8 + rating_to_percent(self.mastery,scale_factor)
    
    def get_vers_percent(self,scale_factor=40):
        return rating_to_percent(self.vers,scale_factor)
    
    def get_attack_power(self):
        if self.spec=='prot':
            return self.strength * ( 1 + (warrior.get_mastery_percent(self))/100 ) * 1.05
        else:
            return self.strength * 1.05 #battle shout
        
    def get_ability_power(self):
        t_power = self.wdps*6
        
        if self.spec=='prot':
            t_power *= ( 1 + (warrior.get_mastery_percent(self))/100 )
        
        t_power *= 1.05 # add in battleshout
        
        return t_power + warrior.get_attack_power(self)
    
    # these are the prot warrior abilities that do damage
    def shield_slam(self):
        
        return round(0.851*warrior.get_ability_power(self)*1.20*(1 + warrior.get_vers_percent(self)/100))
    
    def revenge(self):
        
        return round(0.63*warrior.get_ability_power(self)*(1 + warrior.get_vers_percent(self)/100))
    
    def thunder_clap(self):
        
        return round(0.42*warrior.get_ability_power(self)*(1 + warrior.get_vers_percent(self)/100))
    
    def condemn_damage(self,rage):
        
        return round(1.035*warrior.get_ability_power(self)*(1 + warrior.get_vers_percent(self)/100)*(min(20,rage)/20 ))
    
    def condemn_shield(self,rage):
        
        return round(0.6*warrior.get_ability_power(self)*(1 + warrior.get_vers_percent(self)/100)*(min(20,rage)/20 ))
    
    def devastator(self):
        
        return round(0.221*warrior.get_ability_power(self)*(1 + warrior.get_vers_percent(self)/100))
    
    # ravager will always tick 6 times regardless of haste level
    # we will just add a counter to show this in the actual sim
    def ravager_tick(self):
        
        return round(0.424*warrior.get_ability_power(self)*(1 + warrior.get_vers_percent(self)/100))
    
    def dragon_roar(self):
        
        return round(1.7*warrior.get_ability_power(self)*(1 + warrior.get_vers_percent(self)/100))
    
    def ignore_pain(self):
        
        return round(3.5*warrior.get_ability_power(self)*(1 + warrior.get_vers_percent(self)/100))
    
    
if __name__ == '__main__':
    
    stats = {
        'haste':368,
        'crit':201,
        'mastery':343,
        'vers':385,
        'strength':992,
        'wdps':31,
        'spec':'prot'
        }
    
    xorku = warrior(stats)