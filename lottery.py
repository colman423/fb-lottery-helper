from random import shuffle

def run(prize, people):
    shuffle(people)
    winner = []
    total = 0
    for d in prize:
        start, end = total, total+int(d['count'])
        print(start, end)
        for person in people[start: end]:
            tmp = dict(person)
            tmp['prize'] = d['name']
            winner.append(tmp)
        total = end
    print(winner)
    return winner