import itertools
import statistics

def get_position(job):
    support_jobs = ["바드", "도화가", "홀리나이트"]
    return "서폿" if job in support_jobs else "딜러"

def get_synergy(job):
    synergies = {
        "치확": ["배틀마스터", "건슬링어", "아르카나", "데빌헌터", "스트라이커", "기상술사"],
        "치피증": ["창술사"],
        "공증": ["기공사", "스카우터"],
        "받피증": ["소울이터", "소서리스", "버서커", "데모닉", "호크아이", "인파이터", "슬레이어"],
        "방감": ["워로드", "서머너", "블래스터", "디스트로이어", "리퍼"],
        "사멸": ["디스트로이어", "워로드", "블레이드", "인파이터", "스트라이커", "데빌헌터", "블레이드", "리퍼", "창술사", "슬레이어"],
        "백헤드": ["워로드", "블레이드"]
    }

    char_synergies = [k for k, v in synergies.items() if job in v]
    return char_synergies

def form_party(members, raid_party_name, party_size=4):
    if raid_party_name == "쿠크세이튼":
        members = [char for char in members if char[3] >= 1475 and char[3] < 1580]

    possible_parties = []
    used_characters = set()

    while members:
        valid_parties = []
        for party in itertools.combinations(members, party_size):
            support_count = sum(1 for char in party if get_position(char[2]) == "서폿")
            if support_count != 1:
                continue

            if len(set(char[0] for char in party)) != len(party) or \
               len(set(char[1] for char in party)) != len(party) or \
               len(set(char[2] for char in party)) != len(party):
                continue

            party_synergies = list(set(itertools.chain(*[get_synergy(char[2]) for char in party])))

            non_support_levels = [char[3] for char in party if get_position(char[2]) != "서폿"]
            average_level_non_support = sum(non_support_levels) / len(non_support_levels)
            
            total_average_level = sum(char[3] for char in party) / len(party)
            valid_parties.append((total_average_level, average_level_non_support, party_synergies, party))

        if not valid_parties:
            break

        avg_levels = [party[0] for party in valid_parties]
        target_level = statistics.mean(avg_levels)
        valid_parties.sort(key=lambda x: abs(x[0] - target_level))
        chosen_party = valid_parties[0]
        possible_parties.append(chosen_party)
        
        for char in chosen_party[3]:
            members.remove(list(char))
            used_characters.add(tuple(char))

    return possible_parties

def main():
    raid_party_name = input("어떤 파티를 구성하실 건가요? (예: 발탄, 비아키스, 쿠크세이튼, 아브렐슈드, 일리아칸, 카양갤, 상아탑, 카멘): ")
    input_data = input("\n캐릭터 정보를 한번에 입력하세요 ([이름, 닉네임, 전투력, 레벨] 형식으로 공백으로 구분): ")
    data_list = input_data.split(' ')
    characters = []

    for i in range(0, len(data_list), 4):
        name, nickname, job, level = data_list[i], data_list[i+1], data_list[i+2], int(data_list[i+3])
        characters.append([name, nickname, job, level])

    parties = form_party(characters, raid_party_name)
    
    for idx, (total_avg, non_support_avg, synergies, party) in enumerate(parties, 1):
        print(f"\n{raid_party_name} 파티 {idx} (파티 시너지 : {', '.join(synergies)}):")
        for char in party:
            print(char)
        print(f"전체 평균 레벨: {total_avg:.2f}")
        print(f"서폿 제외 평균 레벨: {non_support_avg:.2f}")

    unused_characters = [char for char in characters if tuple(char) not in set(tuple(item) for sublist in parties for item in sublist[3])]

    if unused_characters:
        print("\n사용되지 않은 캐릭터:")

        level_too_high = [char for char in unused_characters if raid_party_name == "쿠크세이튼" and char[3] >= 1580]
        level_too_low = [char for char in unused_characters if raid_party_name == "쿠크세이튼" and char[3] < 1475]
        no_combination = [char for char in unused_characters if char not in level_too_high and char not in level_too_low]

        if level_too_high:
            print("\n사유 : 권장 레벨 초과(골드 손해):")
            for char in level_too_high:
                print(char)

        if level_too_low:
            print("\n사유 : 권장 레벨 미만:")
            for char in level_too_low:
                print(char)

        if no_combination:
            print("\n사유 : 적절한 조합을 찾지 못함:")
            for char in no_combination:
                print(char)

if __name__ == "__main__":
    main()
