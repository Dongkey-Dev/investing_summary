from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import pt_core_news_sm
import pandas as pd

RESULT =  []

def summarize(df) :
    for i, row in df.iterrows() : 
        doc = nlp(row['Text'])

        corpus = [sent.text.lower() for sent in doc.sents ]
        cv = CountVectorizer(stop_words=list(stopwords.words('english')))   
        cv_fit=cv.fit_transform(corpus)    
        word_list = cv.get_feature_names();    
        count_list = cv_fit.toarray().sum(axis=0)
        word_frequency = dict(zip(word_list,count_list))

        val=sorted(word_frequency.values())
        higher_word_frequencies = [word for word,freq in word_frequency.items() if freq in val[-3:]]
        # print("\n----------------------------------------------\nWords with higher frequencies: ", higher_word_frequencies)
        # gets relative frequency of words
        higher_frequency = val[-1]
        for word in word_frequency.keys():  
            word_frequency[word] = (word_frequency[word]/higher_frequency)

        sentence_rank={}
        for sent in doc.sents:
            for word in sent :       
                if word.text.lower() in word_frequency.keys():            
                    if sent in sentence_rank.keys():
                        sentence_rank[sent]+=word_frequency[word.text.lower()]
                    else:
                        sentence_rank[sent]=word_frequency[word.text.lower()]

        top_sentences=(sorted(sentence_rank.values())[::-1])
        top_sent=top_sentences[:3]

        summary=[]
        for sent,strength in sentence_rank.items():  
            if strength in top_sent:
                summary.append(sent)
            else:
                continue
        for i in range(len(summary)): 
            summary[i] = str(summary[i])
        text = ' '.join(summary) 
        data = {"Text": row['Text'], "summary" : text, "url" : row['url'],"keyword" : ', '.join(higher_word_frequencies)}
        RESULT.append(data)

if __name__=="__main__" :
    nlp = pt_core_news_sm.load()
    df = pd.read_excel("result_investing021537.xlsx")
    df = df[~df['Text'].isnull()]
    summarize(df)
    result_df = pd.DataFrame(RESULT, columns=['Text','summary','url','keyword'])
    result_df.to_excel('summary_result.xlsx')
    
        
        