def SelectRaid():
    raids = ["발탄", "비아키스", "쿠크세이튼", "아브렐슈드", "일리아칸", "카양갤", "상아탑", "카멘"]
    difficulties = ["노말", "하드", "헬"]
    abrelshud_difficulties = ["노12", "노13", "노14", "하1노23", "하12노3", "하12노34", "하123노4", "하12", "하13", "하14", "헬"]

    # 사용자에게 레이드 목록 출력
    print("선택 가능한 레이드 목록:")
    print(", ".join(raids))

    # 사용자 레이드 입력
    raid_name = input("구성하려는 레이드를 입력하세요: ")
    raid_name = raid_name.strip()  # 입력값 앞뒤 공백 제거

    # 레이드 축약어 처리
    if raid_name == "비아" or raid_name == "비아키스":
        raid_name = "비아키스"
    elif raid_name == "아브" or raid_name == "아브렐슈드":
        raid_name = "아브렐슈드"
    elif raid_name == "일리" or raid_name == "일리아칸":
        raid_name = "일리아칸"

    # 쿠크세이튼을 선택한 경우 (난이도는 노말, 헬)
    elif raid_name == "쿠크" or raid_name == "쿠크세이튼":
        print(f"{raid_name}의 가능한 난이도: 노말, 헬")
        raid_name = "쿠크세이튼"

        # 선택 가능한 난이도 출력
        difficulty_input = input(f"{raid_name}의 난이도를 입력하세요 (노말, 헬): ")
        difficulty_input = difficulty_input.strip()  # 입력값 앞뒤 공백 제거

        # 공백 없이 return
        if difficulty_input in ["노말", "헬"]:
            return f"{raid_name}{difficulty_input}"
        else:
            return "잘못된 난이도 입력입니다."

    # 난이도가 노말, 하드만 있는 경우
    if raid_name == "일리아칸" or raid_name == "카양갤" or raid_name == "상아탑" or raid_name == "카멘":
        print(f"{raid_name}의 가능한 난이도: 노말, 하드")
        
        # 선택 가능한 난이도 출력
        difficulty_input = input(f"{raid_name}의 난이도를 입력하세요 (노말, 하드): ")
        difficulty_input = difficulty_input.strip()  # 입력값 앞뒤 공백 제거

        # 공백 없이 return
        if difficulty_input in ["노말", "하드"]:
            return f"{raid_name}{difficulty_input}"
        else:
            return "잘못된 난이도 입력입니다."

    # 아브렐슈드를 입력한 경우
    elif raid_name == "아브렐슈드":
        print("아브렐슈드의 가능한 난이도:")
        print(", ".join(abrelshud_difficulties))
        
        difficulty_input = input("아브렐슈드의 난이도를 입력하세요: ")
        difficulty_input = difficulty_input.strip()  # 입력값 앞뒤 공백 제거

        if difficulty_input in abrelshud_difficulties:
            return f"아브{difficulty_input}"
        else:
            return "잘못된 난이도 입력입니다."
    
    # 헬이 존재하는 레이드의 경우
    elif raid_name in raids:
        difficulty_input = input("난이도를 입력하세요 (노말, 하드, 헬): ")
        difficulty_input = difficulty_input.strip()  # 입력값 앞뒤 공백 제거

        if difficulty_input in difficulties:
            return f"{raid_name}{difficulty_input}"
        else:
            return "잘못된 난이도 입력입니다."
    else:
        return "잘못된 레이드 입력입니다."

# 함수 테스트
result = SelectRaid()
print(result)
