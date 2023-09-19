import os
import itertools
import statistics
import json
import shutil

from API_Getcharlist import get_API
from raid import Raid
from character import Character
from party import Party
from selectraid import SelectRaid


def get_synergy(job):
    synergies = {
        "치확": ["배틀마스터", "건슬링어", "아르카나", "데빌헌터", "스트라이커", "기상술사"],
        "치피증": ["창술사"],
        "공증": ["기공사", "스카우터"],
        "받피증": ["소울이터", "소서리스", "버서커", "데모닉", "호크아이", "인파이터", "슬레이어"],
        "방감": ["워로드", "서머너", "블래스터", "디스트로이어", "리퍼"],
        "사멸": ["디스트로이어", "워로드", "블레이드", "인파이터", "스트라이커", "데빌헌터", "블레이드", "리퍼", "창술사", "슬레이어"],
        "백헤드": ["워로드", "블레이드"],
    }

    char_synergies = [k for k, v in synergies.items() if job in v]
    return char_synergies


def form_party(characters, raid_party_name, party_size=4):
    sup_characters = []
    unused_characters = {}
    possible_parties = []

    # 레이드 조건 불러오기
    raid = Raid.load(raid_party_name)

    # 서폿 캐릭터 분리
    # 레벨 제한 확인
    remained_characters = []
    unused_characters["레벨제한"] = []
    for character in characters:
        if character.is_supporter():
            sup_characters.append(character)
        elif raid.check_limit_level(character.item_level):
            remained_characters.append(character)
        else:
            unused_characters["레벨제한"].append(character)

    # 추후 서폿과 분리해서 조합할것
    # 현재는 일단 합쳐놓기
    remained_characters += sup_characters

    # 가능한 파티 조합 찾기
    while remained_characters:
        valid_parties = []

        # 모든 조합 고려
        # 문제점: 최대한 많은 캐릭터를 사용해서 조합하지 않음
        for party_characters in itertools.combinations(remained_characters, party_size):
            party = Party(party_characters)

            # 서폿이 하나만 있어야함
            # -> 조합 고려할 때 서폿 제외하고 party_size - 1만큼만 고려해서 복잡도 줄이기
            support_count = sum(1 for char in party.characters if char.is_supporter())
            if support_count != 1:
                continue

            # 중복 제거 위한 코드같음
            # 조합 고려할 때 서로 다른 유저의 캐릭으로 조합하기
            if (
                len(set(char.user_name for char in party.characters)) != party.get_num_characters()
                or len(set(char.char_name for char in party.characters)) != party.get_num_characters()
                or len(set(char.char_class for char in party.characters)) != party.get_num_characters()
            ):
                continue

            valid_parties.append(party)

        # 더 이상 가능한 파티가 없으면 while 종료
        if not valid_parties:
            break

        # 파티들 평균 레벨
        avg_levels = [party.avg_level for party in valid_parties]
        # 파티들 평균 레벨의 평균
        target_level = statistics.mean(avg_levels)
        # 파티를 평균 레벨 순으로 정렬(오름차순)
        valid_parties.sort(key=lambda x: abs(x.avg_level - target_level))
        # 가장 레벨이낮은 파티를 선택해서 가능한 파티에 추가
        chosen_party = valid_parties[0]
        possible_parties.append(chosen_party)

        # 선택한 파티의 멤버를 더 이상 조합 고려하지 않음
        for char in chosen_party.characters:
            remained_characters.remove(char)

    unused_characters["조합실패"] = remained_characters

    return possible_parties, unused_characters


def get_character_data(member_dir_path: str):
    member_file_list = os.listdir(member_dir_path)

    member_data_dict = {}
    characters = []

    for member_file in member_file_list:
        name = os.path.splitext(member_file)[0]
        with open(os.path.join(member_dir_path, member_file), "r", encoding="UTF-8") as f:
            member_data_dict[name] = json.load(f)

    for name, member_data in member_data_dict.items():
        for character_data in member_data:
            character_data["Name"] = name
            character = Character.load(character_data)
            characters.append(character)

    return characters


def main():
    # if __debug__:
    #     raid_party_name = "쿠크세이튼"
    # else:
    #     get_API()
    #     raid_party_name = input("어떤 파티를 구성하실 건가요? (예: 발탄, 비아키스, 쿠크세이튼, 아브렐슈드, 일리아칸, 카양갤, 상아탑, 카멘): ")

    get_API()
    raid_party_name = SelectRaid()

    # 캐릭터 정보 불러오기
    member_dir_path = "./members"
    characters = get_character_data(member_dir_path)

    parties, unused_characters = form_party(characters, raid_party_name)

    for idx, party in enumerate(parties, 1):
        print(f"\n{raid_party_name} 파티 {idx} (파티 시너지 : {', '.join(party.synergies)}):")
        for char in party.characters:
            print(char)
        print(f"전체 평균 레벨: {party.avg_level:.2f}")
        print(f"서폿 제외 평균 레벨: {party.avg_level_without_sup:.2f}")

    if unused_characters:
        print("\n사용되지 않은 캐릭터:")

        if len(unused_characters["레벨제한"]) > 0:
            print("\n사유 : 권장 레벨 범위 벗어남:")
            for char in unused_characters["레벨제한"]:
                print(char)

        no_combination = [char for char in unused_characters["조합실패"]]

        if no_combination:
            print("\n사유 : 적절한 조합을 찾지 못함:")
            for char in no_combination:
                print(char)

    if not __debug__:
        shutil.rmtree(member_dir_path)


if __name__ == "__main__":
    main()
