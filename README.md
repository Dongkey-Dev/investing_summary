# Summary investing news

[investing.com/news/world-news](http://investing.com/news/world-news) 의 10페이지 내의 기사들을 크롤링하고, Sklearn 라이브러리의 CountVectorizer를 이용하여 긁어온 기사들을 기사별로 요약해주는 코드입니다.

먼저 investingKR_crawling.py 코드를 실행하여 가장 최근 날짜의 기사들을 크롤링 합니다.

크롤링된 데이터는 xlsx 확장명으로 저장됩니다.(엑셀)

![11](https://user-images.githubusercontent.com/57933815/92077519-8dcdc800-edf7-11ea-925b-27b9a854df2c.png)

총 350개의 index가 저장됩니다.

여기서 각각의 Text를 summary_eng.py 코드를 이용하여 요약을 진행할 것입니다.

예시로 가장 상단의 기사( 'Cattle ship feared lost off Japan in storm, one crew member rescued' )를 summary 코드에 돌린다면,

```markup
By Junko Fujita and Praveen Menon TOKYO/WELLINGTON (Reuters) - 
A ship carrying 43 crew and nearly 6,000 cattle from New Zealand to China capsized after 
losing an engine in stormy weather in the East China Sea, the only crew member rescued 
so far told Japan's coastguard on Thursday. The Gulf Livestock 1 sent a distress call 
from the west of Amami Oshima island in southwestern Japan on Wednesday as the region 
experienced strong winds, heavy seas and drenching rains from Typhoon Maysak as it headed 
towards the Korean peninsula. Japan's coastguard said it rescued one crew member, Sareno 
Edvarodo, a 45-year-old chief officer from the Philippines, on on Wednesday night 
(Tokyo time) while searching for the ship.  

According to Edvarodo, the ship lost an engine before it was hit by a wave and capsized, 
a coastguard spokeswoman said.  
When the ship capsized, crew were instructed to put on lifejacket. 
Edvarodo said he jumped into the water and did not see any other crew members 
before he was rescued. Pictures provided by the coastguard showed a person in a lifejacket 
being hauled from choppy seas in darkness. The Gulf Livestock 1 departed Napier in 
New Zealand on Aug. 14 with 5,867 cattle and 43 crew members on board, 
bound for the Port of Jingtang in Tangshan, China. 

The journey was expected to take about 17 days, 
New Zealand's foreign ministry told Reuters. The crew included 39 people from the 
Philippines, two from New Zealand, and two from Australia, the coastguard said. 

Graphic - Path of the Gulf Livestock 1 livestock carrier: 
https://fingfx.thomsonreuters.com/gfx/ce/xklpynjkwvg/GulfLivestock1Path.png 
The 139 metre (450 ft), 
Panamanian-flagged vessel was built in 2002 and the registered owner is Amman-based 
Rahmeh Compania Naviera SA, according to Refinitiv Eikon data. The ship manager is 
Hijazi & Ghosheh Co.  New Zealand animal rights organisation, SAFE, said the tragedy 
demonstrated the risks of the live animal export trade. "These cows should never 
have been at sea," said Campaigns Manager Marianne Macdonald. 

"This is a real crisis, and our thoughts are with the families of the 43 crew 
who are missing with the ship. But questions remain, including why this trade is 
allowed to continue." 

Last year, New Zealand's government launched a review of country's live export trade, 
worth around NZ$54 million ($37 million) in 2019, after thousands of animals being 
exported from New Zealand and Australia died in transit.   

A conditional ban on the live export of cattle was one of several options being considered, 
Agriculture Minister Damien O'Connor said.

```

(기사 원본 Text)

```markup
A ship carrying 43 crew and nearly 6,000 cattle from New Zealand to China capsized 
after losing an engine in stormy weather in the East China Sea, the only crew member 
rescued so far told Japan's coastguard on Thursday. Japan's coastguard said it rescued 
one crew member, Sareno Edvarodo, a 45-year-old chief officer from the Philippines, 
on on Wednesday night (Tokyo time) while searching for the ship.   

Last year, New Zealand's government launched a review of country's live export trade, 
worth around NZ$54 million ($37 million) in 2019, after thousands of animals being 
exported from New Zealand and Australia died in transit.
```

(Summary 처리된 Text)

36줄 가량의 기사가 7줄로 요약되어 나옵니다.

이 summary의 프로세싱 단계는 크게 4가지의 단계로 나뉩니다.

1. Spacy의 en_core_web_sm 모델을 텍스트에 적용시켜 문장 단위로 분리시킵니다.
2. CountVectorizer 라이브러리를 이용하여 단어의 빈도를 토큰화 시킨 dict를 만듭니다. (명사추출)
3. 분석하고자 하는 text에서 의미있는 단어별로 상대 빈도를 계산합니다.
4. 순위가 매겨진 단어를 기준으로 핵심 문장들의 순위를 매기고, 합성합니다.

summary 과정의 핵심 기술은 TextRank 입니다. 

요약하고자 하는 텍스트를 단어별로 쪼개고, 의미 없는 단어(Stop words : is, the, of 등)를 제거한 뒤, 

의미있는 단어들의 상대 비중을 계산(각 단어의 중요성)한뒤, 그래프를 생성하고 이를 TextRank에 적용합니다.

![22](https://user-images.githubusercontent.com/57933815/92077524-8efef500-edf7-11ea-90ae-d24d7128f05f.png)

TextRank가 높게 책정된 단어들은 keyword column에서 확인할 수 있습니다.

요약된 Text는 summary column에 저장됩니다.
