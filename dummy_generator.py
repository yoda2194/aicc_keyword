from get_keyword_textrank import df
import random
from datetime import datetime, timedelta
import pandas as pd
from scipy.stats import norm

data_len = len(df)
import numpy as np

# def generate_random_index(count):
#     return [
#         max(0, int(norm.rvs(loc=4, scale=0.3)))
#         for _ in range(count)
#     ]
# df['고객만족도'] = np.array(generate_random_index(len(df)))
# df['고객만족도'].mean()
# df['고객만족도'] = random.choices([1,2,3,4,5], weights=[0.1,0.03,0.4,0.13,0.34], k=data_len)
def generate_random_dates(count):
    start_date = datetime(2024, 1, 1, 0, 0, 0)
    end_date = datetime(2024, 12, 31, 23, 59, 59)
    random_dates = [
        start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        for _ in range(count)
    ]
    return random_dates

def generate_random_timedeltas(count):
    return [
        max(0, int(norm.rvs(loc=160, scale=20)))
        for _ in range(count)
    ]

def end_time_generator(date_list, timedelta_list):
    return [date + timedelta(seconds=delta) for date, delta in zip(date_list, timedelta_list)]

def generate_random_phonenum(count):
    return [
        f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
        for _ in range(count)
    ]

counsellors = ['강진모', '강이삭', '남궁진', '최창성', '박소엽', '유다은']
customers = ['성채린', '김수현', '곽은빈', '박승균', '배지빈', '장은별', '이유송', '이용우', '정지민', '정수빈',
             '송우선', '박지민', '이재민', '하지원', '박기범', '황연우', '한민규', '김태하', '류경문', '서정동',
             '한철규', '김진성', '유상범', '김찬유']

counsellors_list = random.choices(counsellors, k=data_len)
customers_list = random.choices(customers, k=data_len)

call_start = generate_random_dates(data_len)
seconds = generate_random_timedeltas(data_len)
call_end = end_time_generator(call_start, seconds)
phone_number = generate_random_phonenum(data_len)
call_type = random.choices(['IB', 'OB'], weights=[0.75,0.25], k=data_len)

dummy_data = pd.DataFrame({
    "통화시작" : call_start,
    "통화종료" : call_end,
    "통화시간" : seconds,
    "고객명" : customers_list,
    "전화번호" : phone_number,
    "상담사" : counsellors_list,
    "발신유형" : call_type
})

df.columns = ['카테고리', '상담내용', '키워드', '상담유형']
df.drop(columns=['카테고리'], inplace=True)
full_data = pd.concat([dummy_data, df], axis=1).reset_index(drop=True)

