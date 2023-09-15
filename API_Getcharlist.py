import os
import requests
import json

def get_API():
    headers = {
        "accept": "application/json",
        "authorization": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDAzMjEyODgifQ.G2e5bMouPV4Nwnab1lPMnhJ25YNHwAMcDL9rNWEcxoN_Cn4o4QLVrtQg9ssXZoexaKXU4j_i9HDxV8_9sWUlfFysIDd16aGdU9xKetJMI4owzXPNX7A4SUTo-VhgUCUxT4PnNUXXEQyUW5T3Wce_0K1LuqzlSzgzYGAozHQG1Pb4Uf1gPKs6lbp5oxwNp1aquu7vcTBeVnV6MYN5G-efSyrs8J4kUaeScYjIThu3npu4ZUFpJAAOzHgVGySSkujdXNuvpB-aSA_dAqYP_7Cnl5gwzPUHwyx9C5A0gpNdclyZVFHSm-NIT4apXj29MCQBGpmTxMB5vOEUHsH44RrM6g",
    }

    # 디렉터리 경로 생성 (./members/)
    directory = "./members/"
    os.makedirs(directory, exist_ok=True)

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
