# PROJECT: Customer Segmentation using RFM

### RFM Analysis, helps us to categorize customers on different segments.

### In RFM each letter represents a term. (Recency, Frequency, Monetary)
- Recency: How many days are there between the last purchase and today? If customer makes purchase 50 days ago, our receny value is 50.
- Frequency: How many purchase is made by customer before? If customer made 11 purchase before, our frequency value is 11.
- Monetary: How much money did customer spend? If customer spends 3000 dollars in its all purchases, our monetary value is 3000

### After creating R, F and M values we need to rank them between 1 and 5. According to the rankings, each customer is assigned to a segment.

#### Segmentation table:
![segTable](https://miro.medium.com/max/1234/0*JJBP4ToZiaw0HVPN.png)

#### Before the project our dataframe's structure looks like that:
![df1](https://i.hizliresim.com/gievd0z.png)

#### After the project the result will be seen like that:
![df2](https://i.hizliresim.com/10hp2tx.png)


#### Dataset: https://archive.ics.uci.edu/ml/datasets/online+retail

#### Note: At the customer_segmentation_rfm.py file, you can see the output of some important lines at the comment line.
#### Keywords: RFM Analysis, Customer Segmentation, CRM Analytics
