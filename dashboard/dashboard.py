import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

# load data
df = pd.read_csv("dashboard//main_data.csv")

# Konversi kolom datetime
datetime_columns = ["order_delivered_customer_date", "order_estimated_delivery_date"]
for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])

# Sidebar untuk pemilihan tanggal
with st.sidebar:
    min_date = df["order_delivered_customer_date"].min()
    max_date = df["order_delivered_customer_date"].max()
    start_date = st.date_input("Rentang Waktu Awal", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("Rentang Waktu Akhir", min_value=min_date, max_value=max_date, value=max_date)

# Filter data berdasarkan rentang tanggal yang dipilih
main_df = df[(df["order_delivered_customer_date"] >= str(start_date)) & 
                (df["order_delivered_customer_date"] <= str(end_date))]

st.header('Dashboard Analisis Bisnis Sederhana')

# Visualisasi 1: Total Keuntungan
st.subheader('Grafik Total Keuntungan')

monthly_orders_df = main_df.resample('M', on='order_delivered_customer_date').size().reset_index(name='order_count')

plt.figure(figsize=(10, 5))
plt.plot(
    monthly_orders_df["order_delivered_customer_date"],
    monthly_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
plt.title("Total Keuntungan", loc="center", fontsize=20)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
st.pyplot()
with st.expander("Penjelasan singkat"):
    st.write(
        """Grafik di atas menunjukkan pergerakan total keuntungan setiap bulan. 
        Pada grafik tersebut menunjukkan pergerakan yang cenderung terus naik. Namun, jika rentang data
        sampai pada bulan September dan Oktober tahun 2018 kebanyakan belum dalam status `delivered` 
        sehingga belum terekap. Namun secara keseluruhan, dari beberapa periode sebelumnya menunjukkan peningkatan yang konstan dan positif 
        """
    )
# Visualisasi 2: Produk Terbaik dan Terburuk
st.subheader('Kategori Produk Paling Banyak dan Paling Sedikit DIbeli')

sum_order_items_df = main_df.groupby("product_category_name").size().reset_index(name="quantity_x")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

sns.barplot(x="quantity_x", y="product_category_name", data=sum_order_items_df.sort_values(by="quantity_x", ascending=False).head(5), palette="Blues", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Kategori Produk Paling Banyak Dibeli", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

sns.barplot(x="quantity_x", y="product_category_name", data=sum_order_items_df.sort_values(by="quantity_x", ascending=True).head(5), palette="Reds_r", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Kategori Produk Paling Sedikit Dibeli", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("Grafik Kategori Produk", fontsize=20)
st.pyplot()
with st.expander("Penjelasan Singkat"):
    st.write(
        """Grafik tersebut menunjukkan 5 kategori produk paling banyak dibeli dan 
        paling sedikit dibeli. Gradasi warna menunjukkan jika semakin gelap warna, maka
        semakin kecil nilainya.
        """
    )
# Visualisasi 3: Top 5 Kota dengan Jumlah Pelanggan Terbanyak
st.subheader('Grafik Kota Dengan Customer Terbanyak')

customer_count_by_city = main_df['customer_city'].value_counts().head(5)

plt.figure(figsize=(10, 5))
sns.barplot(
    x=customer_count_by_city.values, 
    y=customer_count_by_city.index,
    palette=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
)
plt.title("5 Kota dengan Jumlah Customer Terbanyak", loc="center", fontsize=15)
plt.ylabel("Kota", fontsize=12)
plt.xlabel("Jumlah Customer", fontsize=12)
plt.xticks(fontsize=10)
st.pyplot()
with st.expander("Penjelasan Singkat"):
    st.write(
        """Grafik tersebut menunjukkan 5 kota dengan jumlah customer terbanyak.
        Grafik dengan warna biru muda merupakan nilai paling besar dibandingkan dengan
        nilai yang lain.
        """
    )
# Visualisasi 4: Rata-rata Review Berdasarkan Status Pengiriman
st.subheader('Grafik Rata-rata Review')

average_review_by_status = main_df.groupby('Barang_tiba')['review_score'].mean()

plt.figure(figsize=(10, 6))
sns.barplot(x=average_review_by_status.index, y=average_review_by_status.values, palette='Set2')
plt.title('Rata-rata Review Berdasarkan Status Pengiriman', fontsize=16)
plt.xlabel('Status Pengiriman', fontsize=14)
plt.ylabel('Rata-rata Review', fontsize=14)

for i, val in enumerate(average_review_by_status.values):
    plt.text(i, val + 0.05, f'{val:.2f}', horizontalalignment='center', fontsize=12)

st.pyplot()
with st.expander("Penjelasan Singkat"):
    st.write(
        """Grafik tersebut menunjukkan rata-rata review yang dikelompokkan berdasarkan
        status pengiriman yaitu `Tepat Waktu` dan `Terlambat`. Berdasarkan grafik tersebut,
        status pengiriman berpengaruh terhadap kepuasan customer, karena dengan pengiriman tepat waktu
        rata-rata review lebih baik jika dibandingkan dengan pengiriman terlambat.
        """
    )
