import pandas as pd
from collections import Counter

# Read the CSV file
df = pd.read_csv("final_credits.csv")

# What percentage of crew members only have one role and for those crew members what are their roles most often?

# counter for crew that only do one role throughout their career
one_role_counter = 0

single_roles = []

tot_crew = df['Name'].nunique()
grouped_by_name = df.groupby('Name')

for name, group_df in grouped_by_name:
    # for each group
    # get the number of unique roles 
    num_roles = group_df['Role'].nunique()
    #print(num_roles)
    #print(group_df)
    # unique_roles == 1
    # update counter variable 
    # store what that role is in a list
    if num_roles == 1:
        one_role_counter += 1
        single_roles.append(group_df['Role'].iloc[0])

percentage = (one_role_counter/tot_crew * 100)

# perecentage of crew with one role
print(f"\n\nThe percentage of crew with one role is {percentage}%")

role_counts = Counter(single_roles)
total_roles = sum(role_counts.values())

role_percentage_breakdowns = {role: (count, count / total_roles * 100) for role, count in role_counts.items()}

print("Percentage breakdowns for each role:")
for role, (count, percentage) in role_percentage_breakdowns.items():
    print(f"{role}: {percentage:.2f}% (Count: {count})")



crew_roles = {}

for index, row in df.iterrows():
    name = row['Name']
    role = row['Role']
    if name in crew_roles:
        crew_roles[name].append(role)
    else:
        crew_roles[name] = [role]

# Analyze role changes for each crew member and calculate percentage of role changes
role_changes = {}
total_projects = len(df)
for name, roles in crew_roles.items():
    unique_roles = set(roles)
    num_changes = len(roles) - len(unique_roles)
    role_changes[name] = (num_changes / total_projects) * 100

# calculate the role frequencies for each role 
roles_frequency = {}
for roles in crew_roles.values():
    for role in roles:
        if role in roles_frequency:
            roles_frequency[role] += 1
        else:
            roles_frequency[role] = 1

# Calculate the average number of role changes among all crew members
average_role_changes = sum(role_changes.values()) / len(role_changes)
print("\nAverage number of role changes among all crew members:", average_role_changes)

# saw that this was really low, most crew are pretty static in their roles

#roles_aaron_covington = df[df['Name'] == 'Aaron Covington']['Role']
#roles_aaron_covington_df = pd.DataFrame(roles_aaron_covington, columns=['Role'])
#print(roles_aaron_covington_df)

crew_roles = df.groupby(['Name', 'Role']).size().unstack(fill_value=0)

#print(crew_roles)

# Filter crew members who have worked in any role
crew_with_roles = crew_roles[crew_roles.sum(axis=1) > 0]

#print(crew_with_roles.head())

# Calculate the likelihood of each role
role_likelihood = {}
for role in crew_with_roles.columns:
    num_crew_with_role = (crew_with_roles[role] > 0).sum()
    num_crew_only_role = ((crew_with_roles[role] > 0) & (crew_with_roles.sum(axis=1) == crew_with_roles[role])).sum()
    if num_crew_with_role > 0:
        role_likelihood[role] = num_crew_only_role / num_crew_with_role


sorted_roles_likelihood = sorted(role_likelihood.items(), key=lambda x: x[1], reverse=True)

print("Likelihood of crew members exclusively doing each role:")
for role, likelihood in sorted_roles_likelihood:
    print(f"{role}: {likelihood:.2%}")

# for each role if a crew member does switch roles what are they most likely to switch to
# for each role what role are crew members most likely to switch from to change to that role
# attempting to map career moves of each crew member that had more than one role
# most static roles, most dynamic roles?


role_transition_to = {role: {} for role in roles_frequency}
role_transition_from = {role: {} for role in roles_frequency}
total_transitions_to = {role: 0 for role in roles_frequency}
total_transitions_from = {role: 0 for role in roles_frequency}

multi_roles_crew = 0

for name, group_df in grouped_by_name:
    # If a crew member had more than one role throughout their career
    # Iterate through the dataframe to record transitions for those crew members
    num_roles = group_df['Role'].nunique()

    if num_roles > 1:
        for i in range(len(group_df) - 1):
            current_row = group_df.iloc[i]
            next_row = group_df.iloc[i + 1]
            current_role = current_row['Role']
            next_role = next_row['Role']
            #print(current_role)
            #print(next_role)
            if current_role != next_role:
                total_transitions_to[current_role] += 1
                total_transitions_from[next_role] += 1
                if next_role in role_transition_to[current_role]:
                    role_transition_to[current_role][next_role] += 1
                else:
                    role_transition_to[current_role][next_role] = 1

                if current_role in role_transition_from[next_role]:
                    role_transition_from[next_role][current_role] += 1
                else:
                    role_transition_from[next_role][current_role] = 1

# Calculate probabilities for transitions to other roles and percentages
role_transition_to_probabilities = {}
for current_role, transitions in role_transition_to.items():
    total_transitions = total_transitions_to[current_role]
    role_transition_to_probabilities[current_role] = {next_role: (count, count / total_transitions * 100) for next_role, count in transitions.items()}

# Calculate probabilities for transitions from other roles and percentages
role_transition_from_probabilities = {}
for next_role, transitions in role_transition_from.items():
    total_transitions = total_transitions_from[next_role]
    role_transition_from_probabilities[next_role] = {current_role: (count, count / total_transitions * 100) for current_role, count in transitions.items()}


print(f"\nMost likely role transitions for each role:")
for current_role, transitions in role_transition_to_probabilities.items():
    sorted_transitions = sorted(transitions.items(), key=lambda x: x[1][1], reverse=True)
    print(f"\nFor {current_role}:")
    total = sum([count for count, _ in transitions.values()])
    for next_role, (count, percentage) in sorted_transitions:
        print(f"\tMost likely to transition to {next_role} with {count} transitions ({percentage:.2f}% of total transitions)")

print("\nMost likely previous roles for each role:")
for next_role, transitions in role_transition_from_probabilities.items():
    sorted_transitions = sorted(transitions.items(), key=lambda x: x[1][1], reverse=True)
    print(f"\nFor {next_role}:")
    total = sum([count for count, _ in transitions.values()])
    for current_role, (count, percentage) in sorted_transitions:
        print(f"\tMost likely transitioned from {current_role} with {count} transitions ({percentage:.2f}% of total transitions)")





    