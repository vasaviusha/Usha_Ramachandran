#!/usr/bin/env python
# coding: utf-8

# #Customer Behavior analysis
# 

# #importing the data

# In[1]:


import pandas as pd 
df = pd.read_csv("D:\PowerBI_Dashboard_projects_PPT\customer_shopping_behavior.csv")


# In[4]:


df.head()
df.info()


# # # Summary statistics using .describe()

# In[5]:


df.describe(include ="all")


# # Checking if missing data or null values are present in the dataset

# In[6]:


df.isnull().sum()


# In[8]:


#found that only Review Rating has 37 blanks


# In[9]:


# Imputing missing values in Review Rating column with the median rating of the product category instead of all values median


# In[10]:


#changing all columns to lower case and proper naming convention


# In[12]:


df.columns=df.columns.str.lower()
df.columns =df.columns.str.replace(' ', '_')


# In[13]:


df.info()


# In[15]:


df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})


# In[16]:


df.head()


# In[19]:


df.isnull().sum()


# In[20]:


df['review_rating'] = df.groupby('category')['review_rating'].transform(lambda x:x.fillna(x.median()))


# In[21]:


df.isnull().sum()


# # create a new column age_group

# In[23]:


labels = ['Teenage', 'Adult','Middle_age','Senior_Citizen']
df['age_group'] = pd.qcut(df['age'],q=4, labels = labels)


# In[24]:


df[['age','age_group']].head(20)


# # # create new column purchase_frequency_days

# In[25]:


frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}


# In[27]:


df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)


# In[28]:


df[['purchase_frequency_days','frequency_of_purchases']].head(10)


# # Checking whether 2 columns are same discount applied & promo code applied

# In[30]:


(df['promo_code_used'] == df['discount_applied']).all()


# # # Dropping promo code used column

# In[31]:


df.drop('promo_code_used',axis =1)


# # Connecting Python script to PostgreSQL

# In[36]:


pip install psycopg2-binary sqlalchemy


# In[37]:


from sqlalchemy import create_engine

# Step 1: Connect to PostgreSQL
# Replace placeholders with your actual details
username = "postgres"      # default user
password = "postgres" # the password you set during installation
host = "localhost"         # if running locally
port = "5432"              # default PostgreSQL port
database = "customer_behavior"    # the database you created in pgAdmin

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2: Load DataFrame into PostgreSQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")


# In[ ]:




