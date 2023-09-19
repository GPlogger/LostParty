import os
import requests
import json


def get_user_data():
    # 디렉터리 경로 생성 (./members/)
    token_path = "token.txt"
    if not os.path.exists(token_path):
        # 토큰 생성
        token = input("API 토큰을 입력하세요: ")
        with open("token.txt", "w") as f:
            f.write(token)
    else:
        # 토큰 읽기
        with open("token.txt", "r") as f:
            token = f.readline()

    directory = "./members/"
    os.makedirs(directory, exist_ok=True)

    headers = {
        "accept": "application/json",
        "authorization": token,
    }
    # token이 잘못 입력된 경우에 대한 처리 필요

    while True:
        # 사용자로부터 이름과 캐릭터 이름을 입력 받음
        name = input('이름을 입력하세요 (입력 종료하려면 "x"를 입력하세요): ')

        if name.lower() == "x":
            break  # "x" 입력 시 입력 종료

        character_name = input("캐릭터 이름을 입력하세요: ")

        # URL 생성
        url = f"https://developer-lostark.game.onstove.com/characters/{character_name}/siblings"

        response = requests.get(url, headers=headers)

        # 올바른 방법으로 HTTP 응답 상태 코드를 확인
        if response.status_code == 200:
            print("요청 상태: 정상 작동")
            data = response.json()

            if data:
                file_name = f"{name}.json"
                with open(os.path.join(directory, file_name), "w", encoding="utf-8") as file:
                    file.write(json.dumps(data, ensure_ascii=False, indent=4))

                print(f"데이터를 {file_name} 파일로 저장했습니다.")
            else:
                print("데이터가 없습니다.")
        else:
            print("요청 상태: 기타 오류")
            continue
