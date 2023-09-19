import os
import yaml

from raid import Raid


short_name_dict = {
    "쿠크세이튼": ["쿠크"],
    "비아키스": ["비아"],
    "아브렐슈드": ["아브"],
    "일리아칸": ["일리"],
}

difficulty_dict = {"노말": "normal", "하드": "hard", "헬": "hell"}


def SelectRaid():
    raid_condition_dir = "./raid_conditions"
    abrelshud_difficulties = [
        "노12",
        "노13",
        "노14",
        "하1노23",
        "하12노3",
        "하12노34",
        "하123노4",
        "하12",
        "하13",
        "하14",
        "헬",
    ]

    raid_list = [os.path.splitext(raid)[0] for raid in os.listdir(raid_condition_dir)]

    while True:
        # 사용자에게 레이드 목록 출력
        print("선택 가능한 레이드 목록:")
        print(", ".join(raid_list))

        # 사용자 레이드 입력
        raid_name = input("구성하려는 레이드를 입력하세요: ")
        raid_name = raid_name.strip()  # 입력값 앞뒤 공백 제거

        # 레이드 축약어 처리
        for key, value in short_name_dict.items():
            if raid_name in value:
                raid_name = key
                break

        raid_condition_path = os.path.join(raid_condition_dir, raid_name + ".yaml")

        # 레이드 파일 존재 확인
        if not os.path.exists(raid_condition_path):
            print("해당 레이드는 존재하지 않습니다.")
        else:
            break

    # 레이드 파일 열기
    with open(raid_condition_path, "r") as f:
        raid_conditions = yaml.load(f, Loader=yaml.FullLoader)

    # 레이드 가능 난이도 확인
    keys = raid_conditions.keys()
    while True:
        difficulty_input = input(f"{raid_name}의 가능한 난이도를 입력하세요 ({', '.join(keys)}): ")
        difficulty_input = difficulty_input.replace(" ", "")

        if not difficulty_input in keys:
            print("해당 난이도는 존재하지 않습니다.")
        else:
            return Raid(name=raid_name, **raid_conditions[difficulty_input])
            break

    # 아브렐슈드를 입력한 경우
    # elif raid_name == "아브렐슈드":
    #     print("아브렐슈드의 가능한 난이도:")
    #     print(", ".join(abrelshud_difficulties))

    #     difficulty_input = input("아브렐슈드의 난이도를 입력하세요: ")
    #     difficulty_input = difficulty_input.strip()  # 입력값 앞뒤 공백 제거

    #     if difficulty_input in abrelshud_difficulties:
    #         return f"아브{difficulty_input}"
    #     else:
    #         return "잘못된 난이도 입력입니다."
