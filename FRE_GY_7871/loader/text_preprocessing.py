import pandas as pd
import numpy as np
import gensim
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


STOPWORDS = stopwords.words('english')


# Modification based on codes by Yuxuan Wang
class SimpleProcessor:
    def __init__(self, news_file, price_file, ticker_name, price_type):
        self.ticker_name = ticker_name
        self.price_type = price_type

        self.crypto_news = pd.read_csv(news_file, index_col=[0])[[ticker_name]]
        self.crypto_news.index = pd.to_datetime(self.crypto_news.index)

        self.price_vol = pd.read_csv(price_file, index_col=[0])
        self.crypto_price = self.price_vol[[ticker_name + '-' + price_type]].shift(1)

        # calc daily return data
        self.crypto_price["returns"] = self.crypto_price[self.ticker_name + '-' + self.price_type].pct_change().shift(
            -1)

        self.crypto_price.index = pd.to_datetime(self.crypto_price.index).tz_convert(None)
        self.crypto_news.index = pd.to_datetime(self.crypto_news.index)

        self.data = None

    def get_data(self):
        # sentiment version
        res = pd.DataFrame(columns=["titles", "summaries", "sentiments"])
        for i in range(len(self.crypto_news)):
            line = eval(self.crypto_news.iloc[i][0])  # str to list
            length = 0
            for elem in line:
                length += len(elem)
            if length == 0:
                continue
            else:
                # preprocess titles and summaries, remove duplicate ones
                titles, summaries = list(set(line[0])), list(set(line[1]))
                titles, summaries = " ".join(titles), " ".join(summaries)
                # average sentiment score
                sentiments = list(set(line[2]))
                for j in range(len(sentiments)):
                    if sentiments[j] == "Somewhat-Bullish":
                        sentiments[j] = 0.5
                    elif sentiments[j] == "Bullish":
                        sentiments[j] = 1
                    elif sentiments[j] == "Somewhat-Bearish":
                        sentiments[j] = -0.5
                    elif sentiments[j] == "Bearish":
                        sentiments[j] = -1
                    else:
                        sentiments[j] = 0
                sentiments = np.mean(sentiments)
                # fill in dataframes
                res.loc[self.crypto_news.index[i]] = titles, summaries, sentiments
        # cat strings
        res["text"] = res["titles"].str.cat(res["summaries"], sep=' ')

        # data preprocessing
        self.data = pd.merge(
            res, self.crypto_price, how="left", left_index=True, right_index=True
        )
        self.data = self.data[~self.data.isna().any(axis=1)][["text", "sentiments", "returns"]]
        self.data["text"] = self.remove_stopwords(pd.Series(self.tokenize_text(self.data["text"]))).values
        self.data["class"] = (self.data["sentiments"] > 0).map({True: 1, False: 0})
        return self.data.copy()

    @staticmethod
    def tokenize_text(text):
        for sentence in text:
            yield gensim.utils.simple_preprocess(str(sentence), deacc=True)

    @staticmethod
    def remove_stopwords(text):
        return text.apply(lambda x: [w for w in x if w not in STOPWORDS])

    @staticmethod
    def join_str(df):
        lists = eval(df[0])
        if lists[0]:
            return ' '.join(lists[0])
        return np.nan


if __name__ == "__main__":
    sp = SimpleProcessor(
        r"../data/btc_eth.csv",
        r"../data/price_vol.csv",
        "BTC", "close"
    )
    data = sp.get_data()
    data.text = [" ".join(text) for text in data.text]

    data.to_parquet(r"data/preprocessed_text.parquet")


