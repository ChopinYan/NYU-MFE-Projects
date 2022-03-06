# IAQF22
*stared: low priority

**Please code every part(define part as first titled) as a class or function inside a file**

**We can easily combine all the files into a main file**


# Data - Deyang
Notes: 
**In Fixincome, the data index is defferent from others!!**
## day-freq indicators
Five groups:
- Equity Market
- Fix Income
- Macro
- commodity
- trading factors (optional)

# *HMM model 
- use HMM on RS3000 and derived features

# Feature Extraction - Khoa and Zhengxuan
- **use Hierarchical clustering with DTW measure to perform clustering on on variable**
- **After computing clusters for each variable, we compute the average of a set of time serie to get a representitaive template. (average)**
- For each training and test sample, we ﬁrst compute DTWsubseqD to each template.(similarity measure), This provides a vector of distances, which is the same size as the number of templates, for each sample.

> Progamming Detials
> 
> Input: 
> - Dataframe, with varibales name as columns(n), datetime as index(m)
> - size = m, n
> - element = raw data value.
> 
> Output:
> - Dataframe, with cluster label as columns(k), datetime as index(l)
> - size = k, l
> - element = each value in dataframe means the similarity value


# Clustering and classification model - Danni and Zijian
## Clustering
- PCA before clustering
- K-means method for clustering
- *Hierarchical clustering

> Progamming Detials
> 
> Input: 
> - Dataframe, could be raw data or data after Feature selection
> - **rememeber to standardize the dataframe before put into PCA**
>
> Clustering:
> - **choose how many clusters based on Silhouette Score**
> - use k-means or hierarchical clustering techinques
> 
> Output:
> - Dataframe, with one extra columns called cluster label.



## Classification method 
- Random forest, Gradient Boosting, LDA, Logistic Reg, K-means, NN, SVM
- remember when training, do train Xt with Yt+1, because we wanna to predict
> Progamming Detials
> 
> Input: 
> - Dataframe, with one extra columns called cluster label.
> 
> Fitting:
> - train-test splitting
> - fit the variable and its label(t+1) on training set
> 
> Predicting:
> - predict on the test set.
> - convert predictions into buy-hold-sell **daily signals (0,-1,1)** corresponding with 3 market regimes
> 
> 
> Output:
> - 1 column Dataframe, columnname = singal
> - index = datetime index
> - sigal = 0, 1, -1

# Backtesting - Deyang and Yiren
**all strategy performed on RS3000**
## Tail-hedging
The tail-hedging strategy is designed for investors that seek long exposure to a given asset while being hedged against crisis periods. The strategy holds a long position during regime 1 and switches to a short position during regime 2; it is designed for assets with positive expected returns during regime 1 and negative expected returns in regime 2.
> Progamming Detials
> 
> Input: 
> - signals,
> 
> Output:
> - net value curve, MDD, sharpe ratio, Tracking error, etc...

## Tactical Allocation
The strategy rotates between two different portfolios. The active portfolio at a given point in time is dependent on the detected regime. **Throughout regime 1, the strategy maintains a traditional 60/40 portfolio consisting of the S&P 500 and U.S. treasury bonds. During regime 2, the strategy switches to a portfolio of short positions on the S&P 500 and crude oil, and long positions in gold and U.S. treasury bonds**, each allocated 25% of the total portfolio weight.
> Progamming Detials
> 
> Input: 
> - signals,
> 
> Output:
> - net value curve, MDD, sharpe ratio, Tracking error, etc...
