# 형태소 분석
from konlpy.tag import Komoran
from konlpy.tag import Mecab
# word2vec
from gensim.models import Word2Vec

import pandas as pd

# load models
komoran = Komoran()
ko_model = Word2Vec.load('./lib/ko/ko.bin')


def get_opposite(str):
    pos = komoran.pos(str)

    verb = None
    for token in pos:
        if token[1] == 'VV':
            verb = token[0]
            break

    print(pos)

    try:
        sim = ko_model.wv.most_similar(verb)
        print('>> 동사 : ' + verb)
        print(sim)

        return sim
    except:
        print('검출 실패')
        return None


lines = ['데이터 영역 안에 오류가 있는지 없는지 알아내는 추가적인(부가적인) 데이터.', 'Host ID 부분은 그 Network에 접속되어 있는 컴퓨터의 식별번호를 의미한다.', 'TCP는 한 번에 많은 상대에게 데이터를 전달하고자 할 때 사용된다.',
'2∼10GHz의 고주파대역을 활용하는 무선 통신 기술이다.']

f_src_name = 'words.tsv'
dataset = pd.read_csv(f_src_name, delimiter='\t', header=None)
print(dataset)


for line in lines:
    print(get_opposite(line))