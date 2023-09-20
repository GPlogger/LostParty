from itertools import combinations
import statistics

class Character:
    def __init__(self, name, nickname, job, power, position, synergy):
        self.name = name
        self.nickname = nickname
        self.job = job
        self.power = power
        self.position = position
        self.synergy = synergy

def synergy_score(synergy):
    synergy_dict = {
        "치확": 1.074,
        "치피증": 1.07,
        "백헤드_1명": 1.09,
        "백헤드_2명": 1.1726,
        "방감_1명": 1.0638,
        "방감_2명": 1.1320,
        "방감_3명": 1.2145,
        "받피증_1명": 1.06,
        "받피증_2명": 1.1166,
        "받피증_3명": 1.1702,
        "공증_1명": 1.0566,
        "공증_2명": 1.1102,
        # ... 시너지 종류를 태그로 추가, 조건식을 통해 시너지 추가(방감1, 2, 등등) 
    }
    return synergy_dict.get(synergy, 1)

def party_score(party):
    dealer_scores = [char.power for char in party if char.position == '딜러']
    support = next(char for char in party if char.position == '서폿')
    avg_dealer_score = sum(dealer_scores) / len(dealer_scores)
    return avg_dealer_score * support.power * synergy_score(support.synergy)

def party_avg_power(party):
    powers = [char.power for char in party]
    return sum(powers) / len(powers)

def main():
    characters = [
        Character("스태프", "지성소서", "소서", 1473, "딜러", "B"),
        Character("스태프", "지성알카", "알카", 1462, "딜러", "B"),
        Character("현기", "현기창술", "창술", 1471, "딜러", "A"),
        Character("현기", "현기리퍼", "리퍼", 1451, "딜러", "B"),
        Character("그류", "그류건슬", "건슬", 1420, "딜러", "A"),
        Character("그류", "그류창술", "창술", 1430, "딜러", "A"),
        Character("성률", "성률모닉", "데모닉", 1440, "딜러", "A"),
        Character("성률", "성률도화", "도화", 1470, "서폿", "B"),
        Character("응애", "응애소서", "소서", 1420, "딜러", "B"),
        Character("응애", "응애바드", "바드", 1410, "서폿", "A"),
    ]

    valid_parties = []
    for comb in combinations(characters, 4):
        names, nicks, jobs, positions = zip(*[(c.name, c.nickname, c.job, c.position) for c in comb])
        if len(set(names)) == len(set(nicks)) == len(set(jobs)) == 4 and positions.count('딜러') == 3:
            valid_parties.append(comb)

    scored_parties = sorted([(party, party_score(party)) for party in valid_parties], key=lambda x: x[1], reverse=True)

    best_combination = []
    min_deviation = float('inf')

    for base_party, base_score in scored_parties:
        current_combination = [base_party]
        remaining_parties = [party for party, score in scored_parties if set(party).isdisjoint(base_party)]
        
        while remaining_parties and len(current_combination) * 4 + 4 <= len(characters):
            next_party = remaining_parties.pop(0)
            current_combination.append(next_party)
            scores = [party_score(party) for party in current_combination]
            avg = sum(scores) / len(scores)
            deviation = statistics.stdev(scores) if len(scores) > 1 else 0

            if deviation < min_deviation:
                min_deviation = deviation
                best_combination = current_combination

    for party in best_combination:
        for char in party:
            print(f"{char.name} ({char.nickname}, {char.job}) - 전투력: {char.power}")
        avg_power = party_avg_power(party)
        p_score = party_score(party)
        print(f"파티 평균 전투력: {avg_power:.2f}")
        print(f"파티 점수: {p_score:.2f}")
        print("-------------")
    print("편차:", min_deviation)

if __name__ == "__main__":
    main()
