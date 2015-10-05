
class Character(object):
    def __init__(self):
        pass


    def getSkills(self):
        return self.skills
#{'type': 'player', 'name':'TankTwo', 'position' : 2, 'initiative': 6},

class PlayerCharacter(Character):
    def __init__(self):
        super(PlayerCharacter, self).__init__()
        self.type = 'player'

class MonsterCharacter(Character):
    def __init__(self):
        super(MonsterCharacter, self).__init__()
        self.type = 'monster'

class PlayerMage(PlayerCharacter):
    def __init__(self):
        super(PlayerMage, self).__init__()
        self.skills = [
            MagicMissile(2),
            Fireball(1),
        ]

class MonsterZombie(MonsterCharacter):
    def __init__(self):
        super(MonsterZombie, self).__init__()
        self.skills = [
            HitWithAnArm(1)
        ]

class Skill(object):
    def __init__(self):
        self.duration = 0

    def appliesTo(self):
        raise NotImplementedError
    def maxTargets(self):
        raise NotImplementedError
    def getName(self):
        return self.name
    def getEffect(self):
        return self.effect
    def getCost(self):
        return self.cost
    def getDuration(self):
        return self.duration
    def getLevel(self):
        return self.lvl

class SingleTargetSkill(Skill):
    def __init__(self):
        super(SingleTargetSkill, self).__init__()
        pass
    def appliesTo(self):
        return 'monster'
    def maxTargets(self):
        return 1

class AoeSkill(Skill):
    def __init__(self):
        super(AoeSkill, self).__init__()
        pass

    def appliesTo(self):
        return 'monster'
    def maxTargets(self):
        return 100

class MagicMissile(SingleTargetSkill):
    def __init__(self, lvl):
        super(MagicMissile, self).__init__()
        self.lvl = lvl
        self.cost = 10
        self.effect = "Damage"
        self.name = "Magic Missile"
        self.duration = 0


class Fireball(AoeSkill):
    def __init__(self, lvl):
        super(Fireball, self).__init__()
        self.lvl = lvl
        self.cost = 20
        self.effect = "Damage"
        self.name = "Fireball"
        self.duration = 0

class HitWithAnArm(SingleTargetSkill):
    def __init__(self, lvl):
        super(HitWithAnArm, self).__init__()
        self.lvl = lvl
        self.cost = 10
        self.effect = "Damage"
        self.name = "Hit"
        self.duartion = 0