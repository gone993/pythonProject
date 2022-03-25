
from konlpy.tag import Mecab
# from konlpy.tag import Okt
from collections import Counter

mecab = Mecab()

# okt = Okt()
scentence = "안녕하세요, 고은 고은 앱 리뷰 테스트입니다.ㅋㅋ아버지가방에들어가신다."

f = open("alrim_20220228133741.csv", 'r', encoding='utf-8')
reviews = f.read()
noun = mecab.nouns(reviews)
count = Counter(noun)

noun_list = count.most_common(100)
for v in noun_list:
    print(v)

# # 품사 태깅없이 형태소별 토큰화
# print(mecab.morphs(scentence))
#
# # 품사 태깅하여 형태소별 토큰화
# print(mecab.pos(scentence))
#
# # 명사만 추출 -> 오피니언 마이닝에서 많이 활용
# print(mecab.nouns(scentence))