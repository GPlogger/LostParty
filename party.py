import numpy as np
import itertools

from character import Character
from character import CharacterType
from typing import List


class Party:
    synergies = {
        "치확": ["배틀마스터", "건슬링어", "아르카나", "데빌헌터", "스트라이커", "기상술사"],
        "치피증": ["창술사"],
        "공증": ["기공사", "스카우터"],
        "받피증": ["소울이터", "소서리스", "버서커", "데모닉", "호크아이", "인파이터", "슬레이어"],
        "방감": ["워로드", "서머너", "블래스터", "디스트로이어", "리퍼"],
        "사멸": ["디스트로이어", "워로드", "블레이드", "인파이터", "스트라이커", "데빌헌터", "블레이드", "리퍼", "창술사", "슬레이어"],
        "백헤드": ["워로드", "블레이드"],
    }

    def __init__(self, characters: List[Character]):
        self.characters = characters

        self.avg_level = np.mean([character.item_level for character in characters])

        # 서폿이 아닌 캐릭의 레벨 평균 계산
        # 모든 캐릭이 서폿인 경우 리스트가 비는 것을 방지
        self.avg_level_without_sup = 0
        non_sup_characters = [character for character in characters if not character.is_supporter()]
        if len(non_sup_characters) > 0:
            self.avg_level_without_sup = np.mean([character.item_level for character in non_sup_characters])

        self.synergies = list(
            set(itertools.chain(*[self.get_synergy(char.char_class) for char in characters]))
        )

    def get_num_characters(self):
        return len(self.characters)

    def get_synergy(self, class_name):
        char_synergies = [k for k, v in self.synergies.items() if class_name in v]
        return char_synergies
