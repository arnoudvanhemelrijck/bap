import json
from helperClasses import *
from random import randint

# Gets JSON
with open("skills.json") as f:
    jsonskills = json.load(f)
    f.close()
with open("profiles.json") as f:
    jsonprofiles = json.load(f)
    f.close()
names = [line.rstrip() for line in open('names.txt')]

# Some arrays we'll be using
skills = []
profiles = []
members = []

# Turn JSON into classes
## Skills
for skill in jsonskills:
    skills.append(Skill(skill['id'], skill['name']))

## Profiles, with ProfileSkills
for profile in jsonprofiles:
    pskillids = [x['id'] for x in profile['skills']]
    pratings = [x['rating'] for x in profile['skills']]
    pskills = [x for x in skills if x.id in pskillids]
    profileskills = []
    for i in range(len(pratings)):
        profileskills.append(RatedSkill(pskills[i], pratings[i]))
    profiles.append(Profile(profile['id'], profile['name'], profileskills))

# Generate Members, with MemberSkills
for i in range(0, 100):
    #Get random name
    memberName = names[randint(0, len(names) - 1)]
    #Get Profile
    memberProfile = profiles[randint(0, len(profiles) - 1)]
    #Get ProfileSkills and ratings, and turn them into a MemberSkill with rating at or above ProfileSkill rating
    pskills = [x for x in skills if x in [y.skill for y in memberProfile.skills]]
    pratings = [x.rating for x in memberProfile.skills]
    memberSkills = []
    for j in range(len(pskills)):
        memberSkills.append(RatedSkill(pskills[j], randint(pratings[j], 5)))
    #Get random skill that member doesn't have yet, add to member with random rating
    randomskill = skills[randint(0, len(skills) - 1)]
    while(randomskill in [y.skill for y in memberSkills]):
        randomskill = skills[randint(0, len(skills) - 1)]
    memberSkills.append(RatedSkill(randomskill, randint(1, 5)))
    members.append(Member(i, memberName, memberProfile, memberSkills))

#Write members to JSON, makes file if it doesn't exist
with open("members.json", "w+") as fmembers:
    json.dump([x for x in members], fmembers, default=lambda o: o.__dict__, 
                sort_keys=True, indent=4, separators=(',', ':'))

print("Finished generating members! You can find them in members.json, in the same directory as this python script.")