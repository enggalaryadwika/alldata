# Import Library & Packages
import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
import datetime as dt

# Load data csv
all_df = pd.read_csv("https://raw.githubusercontent.com/enggalaryadwika/alldata/main/all_data.csv")

import streamlit as st

import streamlit as st

import streamlit as st

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div style='display: flex; align-items: center; justify-content: center;'>
        
            

        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<hr style='margin: 15px 0; border-color: #4A3AFF;'>", unsafe_allow_html=True)

    st.markdown("### E-Commerce Public Dataset")
    st.markdown("[Kaggle : Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)")

    st.markdown("<hr style='margin: 15px 0; border-color: #4A3AFF;'>", unsafe_allow_html=True)

    st.markdown("### Contact")
    st.markdown(
        """
        Silahkan hubungi saya untuk informasi lebih lanjut.
        - Email: [enggalaryadwika8@gmail.com]
        
        """,
        unsafe_allow_html=True
    )
    st.markdown("<hr style='margin: 15px 0; border-color: #4A3AFF;'>", unsafe_allow_html=True)
    
    st.caption(' Enggal Aryadwika.')



# Mengubah ke format datetime
datetime_columns = ["order_approved_at"]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

def number_order_per_month(df):
    monthly_df = df.resample(rule='M', on='order_approved_at').agg({
        "order_id": "size",
    })
    monthly_df.index = monthly_df.index.strftime('%B')
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={
        "order_id": "order_count",
    }, inplace=True)
    monthly_df = monthly_df.sort_values('order_count').drop_duplicates('order_approved_at', keep='last')
    month_mapping = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    monthly_df["month_numeric"] = monthly_df["order_approved_at"].map(month_mapping)
    monthly_df = monthly_df.sort_values("month_numeric")
    monthly_df = monthly_df.drop("month_numeric", axis=1)
    return monthly_df

def customer_spend_df(df):
    sum_spend_df = df.resample(rule='M', on='order_approved_at').agg({
            "price": "sum"
    })
    sum_spend_df = sum_spend_df.reset_index()
    sum_spend_df.rename(columns={
                "price": "total_spend"
            }, inplace=True)
    sum_spend_df['order_approved_at'] = sum_spend_df['order_approved_at'].dt.strftime('%B') 
    sum_spend_df = sum_spend_df.sort_values('total_spend').drop_duplicates('order_approved_at', keep='last')
    custom_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


    sum_spend_df['month_cat'] = pd.Categorical(sum_spend_df['order_approved_at'], categories=custom_order, ordered=True)


    sorted_df = sum_spend_df.sort_values(by='month_cat')


    sorted_df = sorted_df.drop(columns=['month_cat'])
    return sorted_df

def create_by_product_df(df):
    product_id_counts = df.groupby('product_category_name_english')['product_id'].count().reset_index()
    sorted_df = product_id_counts.sort_values(by='product_id', ascending=False)
    return sorted_df

def rating_cust_df(df):
    rating_service = df['review_score'].value_counts().sort_values(ascending=False)
    
    max_score = rating_service.idxmax()

    df_cust=df['review_score']

    return (rating_service,max_score,df_cust)

def create_rfm(df):
    now=dt.datetime(2018,10,20)


    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    # Group by 'customer_id' and calculate Recency, Frequency, and Monetary
    recency = (now - df.groupby('customer_id')['order_purchase_timestamp'].max()).dt.days
    frequency = df.groupby('customer_id')['order_id'].count()
    monetary = df.groupby('customer_id')['price'].sum()

    # Create a new DataFrame with the calculated metrics
    rfm = pd.DataFrame({
        'customer_id': recency.index,
        'Recency': recency.values,
        'Frequency': frequency.values,
        'Monetary': monetary.values
    })
    #End alternative 2

    col_list = ['customer_id','Recency','Frequency','Monetary']
    rfm.columns = col_list
    return rfm


# Memanggil kembali functions
daily_orders_df=number_order_per_month(all_df)
most_and_least_products_df=create_by_product_df(all_df)
rating_service,max_score,df_rating_service=rating_cust_df(all_df)
customer_spend_df=customer_spend_df(all_df)
rfm=create_rfm(all_df)


# Header
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='color: #4A3AFF;'>ANALYSIS E-COMMERCE PUBLIC</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# === PRODUK BANYAK DIBELI DAN KURANG DIMINATI ===
st.subheader("Produk paling laris dan kurang diminati")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))  

colors = ["#3366CC", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

most_products_df = create_by_product_df(all_df)
sns.barplot(x="product_id", y="product_category_name_english", data=most_products_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk paling laris", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

least_products_df = create_by_product_df(all_df)
sns.barplot(x="product_id", y="product_category_name_english", data=least_products_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk paling kurang diminati", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)

st.markdown("<hr style='margin: 15px 0; border-color: #4A3AFF;'>", unsafe_allow_html=True)

# === KINERJA PENJUALAN DI PLATFORM E-COMMERCE ===
st.subheader('Kinerja Penjualan di Platform E-Commerce')
col1, col2 = st.columns(2)

with col1:
    high_order_num = daily_orders_df['order_count'].max()
    high_order_month = daily_orders_df[daily_orders_df['order_count'] == daily_orders_df['order_count'].max()]['order_approved_at'].values[0]

with col2:
    low_order = daily_orders_df['order_count'].min()
    low_order_month = daily_orders_df[daily_orders_df['order_count'] == daily_orders_df['order_count'].min()]['order_approved_at'].values[0]

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#3366CC",
    linestyle='-',
    mec='black',
    mew=1,
)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=12)
ax.set_title("Penjualan Pada Tahun 2023", fontsize=24)
ax.set_xlabel("Bulan", fontsize=14) 
ax.set_ylabel("Penjualan", fontsize=12) 

st.pyplot(fig)

st.markdown("<hr style='margin: 15px 0; border-color: #4A3AFF;'>", unsafe_allow_html=True)



st.caption('Enggal Aryadwika ')