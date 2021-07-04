# -*- coding: utf-8 -*-
"""
@author: Xorku-Hyjal / KrakenWagon / Andrew Younger

Contains all the abilities and the stat percentage calculations for a prot warrior.
Resources and cooldowns are calculated in the sim script itself

Current as of PRE-CHAINS 9.0.2 (2021-07-04)
"""
from dataclasses import dataclass

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

@dataclass(init=False)
class warrior:
    
    def __init__(self,stats=None):
        if stats is not None:
            self.haste = stats['haste']
            self.crit = stats['crit']
            self.mastery = stats['mastery']
            self.vers = stats['vers']
            self.strength = stats['strength']
            self.wdps = stats['wdps']
            self.rage = stats['rage']
        else:
            raise Exception('Bad initialization - no stats given')
        
        self.haste_perc = rating_to_percent(self.haste,33)/100
        self.crit_perc = (5 + rating_to_percent(self.crit,35))/100
        self.mastery_perc = (8 + rating_to_percent(self.mastery,35))/100
        self.vers_perc = rating_to_percent(self.vers,40)/100

@dataclass(init=False)
class protection(warrior):
    
    def __init__(self,stats=None):
        if stats is None:
            raise Exception('Bad initialization - no stats given')
        else:
            warrior.__init__(self,stats=stats)
            
        patch_multiplier = 1.10 # 10% buff to abilities as a hidden aura in 9.0.5
        
        execute_rage = max(20,self.rage)
        execute_rage = min(40,execute_rage)
            
        self.attack_power = round(self.strength * (1 + self.mastery_perc) * 1.05)
        self.ability_power = round(self.wdps * 6 * (1 + self.mastery_perc) * 1.05) +  self.attack_power
        
        ability_mult = self.ability_power * (1 + self.vers_perc) * patch_multiplier
        
        self.shield_slam = round(1.2 * 0.851 * ability_mult)
        self.revenge = round(0.63 * ability_mult)
        self.thunderclap = round(0.462 * ability_mult)
        
        self.condemn_damage = round(1.035 * ability_mult * (execute_rage/20) )
        # shield does not have patch multiplier
        self.condemn_shield = round(0.6 * self.ability_power * (1 + self.vers_perc) * (execute_rage/20))
        
        # should always tick 6 times
        self.ravager_tick = round(0.424 * ability_mult)
        self.dragon_roar = round(1.7 * ability_mult)
        self.devastator = round(0.221 * ability_mult)
        
        self.ignore_pain = round(3.5 * self.ability_power * (1 + self.vers_perc))

@dataclass(init=False)
class fury(warrior):
    
    def __init__(self,stats=None):
        if stats is None:
            raise Exception('Bad initialization - no stats given')
        else:
            warrior.__init__(self,stats=stats)
            
        self.attack_power = self.strength * 1.05
        self.ability_power = self.attack_power + self.wdps * 6 * 1.05
      
if __name__ == '__main__':
    
    stats = {
        'haste':555,
        'crit':423,
        'mastery':190,
        'vers':667,
        'strength':1293,
        'wdps':46,
        'rage': 20
        }
    
    xorku = protection(stats)
    
    print(xorku.shield_slam)