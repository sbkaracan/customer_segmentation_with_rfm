############################################
# PROJECT: Customer Segmentation using RFM
############################################

# RFM Analysis, helps us to categorize customers on different segments.

# In RFM each letter represents a term. (Recency, Frequency, Monetary)
# Recency: How many days are there between the last purchase and today? If customer makes purchase 50 days ago, our receny value is 50.
# Frequency: How many purchase is made by customer before? If customer made 11 purchase before, our frequency value is 11.
# Monetary: How much money did customer spend? If customer spends 3000 dollars in its all purchases, our monetary value is 3000

# After creating R, F and M values we need to rank them between 1 and 5. According to the rankings, each customer is assigned to a segment.
# Segmentation table:

# Before the project our dataframe's structure looks like that:

# After the project the result will be seen like that:

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)


df_ = pd.read_excel("datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()


df.dropna(inplace=True)


# If there is "C" character in "Invoice", it means it is cancelled invoice. We need to remove these invoices from df because it is not a real purchase.
df = df[~df["Invoice"].str.contains("C", na=False)]

# We should multiply quantity and price because we need total amount of the process. It will be used for calculating monetary
df["TotalPrice"] = df["Quantity"] * df["Price"]

df.head()
"""
  Invoice StockCode                          Description  Quantity  \
0  536365    85123A   WHITE HANGING HEART T-LIGHT HOLDER         6   
1  536365     71053                  WHITE METAL LANTERN         6   
2  536365    84406B       CREAM CUPID HEARTS COAT HANGER         8   
3  536365    84029G  KNITTED UNION FLAG HOT WATER BOTTLE         6   
4  536365    84029E       RED WOOLLY HOTTIE WHITE HEART.         6   
          InvoiceDate  Price  Customer ID         Country  TotalPrice  
0 2010-12-01 08:26:00   2.55     17850.00  United Kingdom       15.30  
1 2010-12-01 08:26:00   3.39     17850.00  United Kingdom       20.34  
2 2010-12-01 08:26:00   2.75     17850.00  United Kingdom       22.00  
3 2010-12-01 08:26:00   3.39     17850.00  United Kingdom       20.34  
4 2010-12-01 08:26:00   3.39     17850.00  United Kingdom       20.34  
"""
###############################################################
# Görev 2: RFM Metriklerinin Hesaplanması
###############################################################


today_date = dt.datetime(2011, 12, 11)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                     'Invoice': lambda num: num.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})



rfm.head()
"""
             InvoiceDate  Invoice  TotalPrice
Customer ID                                  
12346.00             326        1    77183.60
12347.00               3        7     4310.00
12348.00              76        4     1797.24
12349.00              19        1     1757.55
12350.00             311        1      334.40
"""

rfm.columns = ['recency', 'frequency', 'monetary'] # changing column names.
rfm = rfm[rfm["monetary"] > 0] # If there is a monetary value below 0, cancel these customers.

# Creating scores with qcut. Qcut gives ranks to each value.
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1]) # the nearest times' rank is 5.
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]) # the biggest frequencies' rank is 5.
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5]) # the highest monetaries' rank is 5.


# Add R and F values as string ("5" + "1" = "51") and have RFM Score. We didn't use monetary. The reason is, there is not monetary segment on rfm table (you can see it on readme file).
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.head()
"""
             recency  frequency  monetary recency_score frequency_score  \
Customer ID                                                               
12346.00         326          1  77183.60             1               1   
12347.00           3          7   4310.00             5               5   
12348.00          76          4   1797.24             2               4   
12349.00          19          1   1757.55             4               1   
12350.00         311          1    334.40             1               1   
            monetary_score RFM_SCORE  
Customer ID                           
12346.00                 5        11  
12347.00                 5        55  
12348.00                 4        24  
12349.00                 4        41  
12350.00                 2        11  
"""




# Defining segments with regex.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True) # replacing segments with rfm scores.

rfm.head()
"""
             recency  frequency  monetary recency_score frequency_score  \
Customer ID                                                               
12346.00         326          1  77183.60             1               1   
12347.00           3          7   4310.00             5               5   
12348.00          76          4   1797.24             2               4   
12349.00          19          1   1757.55             4               1   
12350.00         311          1    334.40             1               1   
            monetary_score RFM_SCORE      segment  
Customer ID                                        
12346.00                 5        11  hibernating  
12347.00                 5        55    champions  
12348.00                 4        24      at_Risk  
12349.00                 4        41    promising  
12350.00                 2        11  hibernating  
"""
