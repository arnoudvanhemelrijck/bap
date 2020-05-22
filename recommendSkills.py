from helperClasses import *
from scipy.sparse import lil_matrix
from sklearn.decomposition import IncrementalPCA
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import json
import numpy as np

# Loads all members
with open("members.json") as f:
    jsonMembers = json.load(f)
    f.close()

# Turns members into usable objects
members = []
num_skills = 20
skill_dict = {}
collab_matrix = lil_matrix((num_skills, len(jsonMembers)))
for j, jsonmember in enumerate(jsonMembers):
    profile_skills = [RatedSkill(Skill(x['skill']['id'], x['skill']['name']), x['rating'])
                      for x in jsonmember['profile']['skills']]

    profile = Profile(jsonmember['profile']['id'],
                      jsonmember['profile']['name'], profile_skills)

    skills = [RatedSkill(Skill(x['skill']['id'], x['skill']
                               ['name']), x['rating']) for x in jsonmember['skills']]

    member = Member(jsonmember['id'], jsonmember['name'], profile, skills)
    members.append(member)

    # Adds all skills to a matrix and a dictionary for filtering later
    for ratedSkill in member.skills + member.profile.skills:
        collab_matrix[ratedSkill.skill.id, j] = ratedSkill.rating
        skill_dict[ratedSkill.skill.id] = ratedSkill.skill.name

# Tuning 2D Principal Component Analysis, converting data into PCA
latent_dim = 2
pca = IncrementalPCA(n_components=latent_dim)
latent_matrix = pca.fit_transform(collab_matrix)

# Function that recommends skill(s)
def recommendSkill(skill_id, amount):
    recSkills = []

    # Goes over all skills a member has and gets the most similar skills
    # Then stores those for later use
    for memberSkills in (x.skills for x in members if x.id == skill_id):
        for skill in memberSkills:
            top = 5
            scores = np.squeeze(cosine_similarity(
                latent_matrix, latent_matrix[skill.skill.id].reshape(1, -1)))

            top_skills = np.argpartition(scores, -top)[-top:]
            recSkills.extend(top_skills)

    # Counts all skill occurences in the recommended skills list
    # Then sorts from high to low, and returns the highest skill(s)
    occurences = Counter(recSkills)
    occurences.most_common()
    curAmount = 0
    for key in occurences:
        if (key not in [x.skill.id for x in memberSkills]):
            print(f'Most recommended skill: {skill_dict[key]}')
            curAmount += 1
            if curAmount == amount:
                break


def getMember(id):
    [print(x) for x in members if x.id == id]

# Input loop, for demonstration and usability purposes
inputPrompt = "Member ID (-1 to stop): "
n = int(input(inputPrompt))
while(n != -1):
    getMember(n)
    recommendSkill(n, 1)
    n = int(input(inputPrompt))
