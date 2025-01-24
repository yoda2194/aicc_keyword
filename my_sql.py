import pymysql as db

import pandas as pd
import re
from dummy_generator import full_data

conn = db.connect(host= "192.168.101.213", user="jin", password='1234', db='conversation', charset='utf8')

cursor = conn.cursor()

# cursor.execute("use conversation")
# cursor.execute("select * from 상담이력;")
#
# print(cursor.fetchall())
# insert into 상담이력 values('서비스명', '통화시작', '통화종료', '통화시간', '고객명', '전화번호', '상담유형', '상담사', '상담내용')


def validation_data(data):
    def validate_datetime(date_str):
        try:
            date_regex = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
            return bool(date_regex.match(str(date_str)))
        except ValueError:
            return False

    # 보조 함수: 전화번호 검증
    def validate_phone(phone):
        phone_regex = re.compile(r"^\d{2,4}-\d{3,4}-\d{4}$")  # 한국 전화번호 형식
        return bool(phone_regex.match(phone))

    required_fields = {
        "상담유형": lambda x: isinstance(x, str) and 1 <= len(x) <= 255,
        "통화시작": lambda x: validate_datetime(x),
        "통화종료": lambda x: validate_datetime(x),
        "통화시간": lambda x: isinstance(x, int) and x > 0,
        "고객명": lambda x: isinstance(x, str) and 1 <= len(x) <= 100,
        "전화번호": lambda x: validate_phone(x),
        "키워드": lambda x: isinstance(x, str) and 1 <= len(x) <= 255,
        "상담사": lambda x: isinstance(x, str) and 1 <= len(x) <= 100,
        "상담내용": lambda x: isinstance(x, str) and len(x) > 0,
        "발신유형": lambda x: isinstance(x, str) and 1 <= len(x) <= 2

    }

    # 필수 필드가 모두 있는지 확인
    for field in required_fields:
        if field not in data:
            print(f"필수 필드가 누락되었습니다: {field}")
            return False

        # 각 필드 값 검증
        if not required_fields[field](data[field]):
            print(f"유효하지 않은 값입니다: {field} ({data[field]})")
            return False


    return True


def insert_data(data):
    if not validation_data(data):
        return

    with conn.cursor() as cur:
        query = "insert into 상담이력 (상담유형, 통화시작, 통화종료, 통화시간, 고객명, 전화번호, 키워드, 상담사, 상담내용, 발신유형) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cur.execute("use conversation")

        cur.execute(query, (data['상담유형'],
                            data['통화시작'],
                            data['통화종료'],
                            data['통화시간'],
                            data['고객명'],
                            data['전화번호'],
                            data['키워드'],
                            data['상담사'],
                            data['상담내용'],
                            data['발신유형']
                            ))

        conn.commit()

def db_to_df():
    cursor = conn.cursor()
    cursor.execute("select * from 상담이력;")
    result = cursor.fetchall()

    df = pd.DataFrame(result)
    df.columns = ['No','상담유형','통화시작','통화종료','통화시간','고객명','전화번호','키워드','상담사','상담내용','발신유형']
    return df


# for idx, instance in full_data.iterrows():
#     insert_data(instance)
#     print(idx)

conn.close()