import itertools
from datetime import time, timedelta, datetime

def build_pairings(list_of_pariticipants_names):
    create_pairings = list(itertools.combinations(participants, 2))
    return [list(pair) for pair in create_pairings]

def is_not_in_iteration(participant, iteration):
    hasnt_yet_given_feedback = True
    for pair in iteration:
        if participant in pair:
            hasnt_yet_given_feedback = False
    return hasnt_yet_given_feedback

def matrix_append(m, peeps1, peeps2):
    l = []
    for index in range(len(peeps1)):
        l.append([str(peeps1[index]), str(peeps2[index])])
    m.append(l)


def rotate_members(half_part1, half_part2, non_mover):
    new_mem_1 = []
    new_mem_2 = []
    new_mem_1.append(non_mover)
    new_mem_1.append(half_part2[0])

    for member in half_part1[1:-1]:
        new_index_1 = half_part1.index(member) + 1

        new_mem_1.insert(new_index_1, member)
    for member in half_part2[1:]:
        new_index_2 = half_part2.index(member) - 1
        new_mem_2.insert(new_index_2, member)

    new_mem_2.append(half_part1[-1])

    return new_mem_1, new_mem_2

def pairing_matrix(member):
    non_mover = member[0]
    matrix = []

    if (len(member) % 2) != 0:
        member.append("self-reflection")

    int_half_members = int(len(member)/2)

    half_members1 = [i for i in member[:int_half_members]]
    print(half_members1)
    half_members2 = [i for i in member[int_half_members:]]
    print(half_members2)

    matrix_append(matrix, half_members1, half_members2)

    # -1 because one person needs to have a session with every other person
    # -2 for fixing one off issue (last session would be the first)
    condition = len(member) - 2

    while condition != 0:
        half_members1, half_members2 = rotate_members(half_members1, half_members2, non_mover)
        matrix_append(matrix, half_members1, half_members2)
        condition -= 1

    return matrix

def assign_time(start_time, pairing_matrix):
    current_time = datetime.strptime(start_time, "%H%M")
    #add_time_list = [iteration.insert(0, new_time) for iteration in len(pairing_matrix)]

    for iteration in pairing_matrix:
        new_time = current_time + timedelta(minutes=4)
        string_time = "{} - {}".format(current_time.time(), new_time.time())
        iteration.insert(0, string_time)
        current_time = new_time + timedelta(minutes=2)

    return pairing_matrix

def self_reflection_correction(pair, dict_participants_links):
    #if dict_participants_links.get(pair[0]).contains("client") or dict_participants_links.get(pair[1]).contains("client"):
    person_a = dict_participants_links.get(pair[0], "self-reflection")
    person_b = dict_participants_links.get(pair[1], "self-reflection")

    if person_a == "self-reflection":
        pair[0] = pair[1]
        pair[1] = "self-reflection"

def find_correct_link(pair, dict_participants_links):
    #if dict_participants_links.get(pair[0]).contains("client") or dict_participants_links.get(pair[1]).contains("client"):
    person_a = dict_participants_links.get(pair[0], "self-reflection")
    person_b = dict_participants_links.get(pair[1], "self-reflection")
    person_a_is_client = "client" in person_a
    person_b_is_client = "client" in person_b

    if person_a == "self-reflection" or person_b == "self-reflection":
        return ""
    elif person_a_is_client:
        return person_a.rsplit("client; ")[1]
    elif person_b_is_client:
        return person_b.rsplit("client; ")[1]
    elif "zoom" in person_a:
        return person_a
    elif person_b == "no_room":
        return person_a
    else:
        return person_b

def assign_room(pairing_matrix, dict_participants_links):
    for iteration in pairing_matrix:
        for pair in iteration[1:]:
            print(pair)
            self_reflection_correction(pair, dict_participants_links)
            link_to_append = find_correct_link(pair, dict_participants_links)
            pair.append(link_to_append)

    return pairing_matrix

def formatting(ready_pairing_matrix):
    for iteration in ready_pairing_matrix:
        print(iteration[0], "\r\n")
        for item in iteration[1:]:
            if item[1] == "self-reflection":
                print("{} - {} ".format(item[0], item[1]))
            else:
                print("{}, {} - {}".format(item[0], item[1], item[2]))
        print("\r\n")

with open("speedback_participants.txt") as speedback_participants:
    list_of_participants = list(speedback_participants.readlines())
    speedback_participants = [line.rstrip('\n') for line in list_of_participants]

participants_mapped_to_links = { participant.split(",")[0] : participant.split(", ")[1] for participant in speedback_participants }

participants = list(participants_mapped_to_links.keys())

pairings = build_pairings(participants)

matrix = pairing_matrix(participants)

# debugging:
# print(matrix)

matrix = assign_time(input("Start Time: "), matrix)

matrix = assign_room(matrix, participants_mapped_to_links)

formatting(matrix)
