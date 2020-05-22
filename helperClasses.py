import json

class Skill:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id

class RatedSkill:
    def __init__(self, skill, rating):
        self.skill = skill
        self.rating = rating

    def __str__(self):
        return self.skill.name
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.skill.id == other.skill.id and self.rating == other.rating

class Profile:
    def __init__(self, id, name, profileSkills):
        self.id = id
        self.name = name
        self.skills = profileSkills
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id


class Member:
    def __init__(self, id, name, profile, memberSkills):
        self.id = id
        self.name = name
        self.profile = profile
        self.skills = memberSkills

    def __str__(self):
        return self.profile.name + " " + self.name
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.id == other.id and self.name == other.name
