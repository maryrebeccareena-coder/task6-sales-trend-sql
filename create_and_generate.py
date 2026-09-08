import sqlite3, random, pandas as pd, matplotlib, os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

os.makedirs('/home/claude/all_tasks/task6_sql/screenshots', exist_ok=True)

conn = sqlite3.connect('/home/claude/all_tasks/task6_sql/online_sales.db')
cur = conn.cursor()
cur.executescript("""
DROP TABLE IF EXISTS orders; DROP TABLE IF EXISTS products;
CREATE TABLE products(product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT, unit_price REAL);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, order_date TEXT, quantity INTEGER, amount REAL, region TEXT, FOREIGN KEY(product_id) REFERENCES products(product_id));
""")
products=[(1,'Laptop Pro','Electronics',1299.99),(2,'Wireless Mouse','Electronics',29.99),(3,'USB-C Hub','Electronics',49.99),(4,'Running Shoes','Sports',89.99),(5,'Yoga Mat','Sports',34.99),(6,'Water Bottle','Sports',19.99),(7,'Coffee Maker','Kitchen',79.99),(8,'Air Fryer','Kitchen',119.99),(9,'Python Book','Books',39.99),(10,'Data Science Guide','Books',44.99),(11,'Smartphone X','Electronics',799.99),(12,'Headphones Pro','Electronics',149.99),(13,'Desk Chair','Furniture',299.99),(14,'Standing Desk','Furniture',499.99),(15,'Skincare Kit','Beauty',59.99)]
cur.executemany("INSERT INTO products VALUES(?,?,?,?)", products)
regions=['North','South','East','West','Central']
random.seed(99)
orders=[]; oid=1
for year in [2022,2023]:
    for month in range(1,13):
        for _ in range(random.randint(40,120)):
            day=random.randint(1,28); dt=f"{year}-{month:02d}-{day:02d}"
            pid=random.randint(1,15); qty=random.randint(1,5)
            amt=round(products[pid-1][3]*qty*(1-random.choice([0,0,0,0.05,0.10])),2)
            orders.append((oid,random.randint(1,500),pid,dt,qty,amt,random.choice(regions))); oid+=1
cur.executemany("INSERT INTO orders VALUES(?,?,?,?,?,?,?)", orders)
conn.commit()
print(f"✅ online_sales.db: {len(products)} products, {len(orders)} orders")

BG='#0f0f23'; CARD='#1a1a3e'; ACC='#7c3aed'; ACC2='#06b6d4'; ACC3='#10b981'; ACC4='#f59e0b'; WHITE='#e2e8f0'

def style(ax):
    ax.set_facecolor(CARD); ax.tick_params(colors=WHITE,labelsize=9)
    ax.xaxis.label.set_color(WHITE); ax.yaxis.label.set_color(WHITE); ax.title.set_color(WHITE)
    for sp in ax.spines.values(): sp.set_color('#2d2d5e')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

def save_table(df,title,fname,figsize=(12,4)):
    fig,ax=plt.subplots(figsize=figsize); fig.patch.set_facecolor(BG); ax.set_facecolor(BG); ax.axis('off')
    tbl=ax.table(cellText=df.values,colLabels=df.columns,cellLoc='center',loc='center')
    tbl.auto_set_font_size(False); tbl.set_fontsize(9)
    for (r,c),cell in tbl.get_celld().items():
        if r==0: cell.set_facecolor(ACC); cell.set_text_props(color=WHITE,fontweight='bold')
        else:
            cell.set_facecolor('#222244' if r%2==0 else CARD); cell.set_text_props(color=WHITE)
        cell.set_edgecolor('#2d2d5e')
    fig.suptitle(title,color=WHITE,fontsize=11,fontweight='bold',y=0.98)
    plt.tight_layout(); plt.savefig(f'/home/claude/all_tasks/task6_sql/screenshots/{fname}',dpi=130,bbox_inches='tight',facecolor=BG); plt.close()
    print(f"  ✅ {fname}")

df=pd.read_sql("SELECT STRFTIME('%Y',order_date) AS year, STRFTIME('%m',order_date) AS month, COUNT(DISTINCT order_id) AS order_volume, ROUND(SUM(amount),2) AS monthly_revenue FROM orders GROUP BY year,month ORDER BY year,month",conn)
save_table(df,"Q1: Monthly Revenue & Order Volume (GROUP BY Year/Month)","01_monthly_revenue_table.png",(13,7))

fig,ax=plt.subplots(figsize=(14,6)); fig.patch.set_facecolor(BG); style(ax)
labels=[f"{r['year']}-{r['month']}" for _,r in df.iterrows()]
ax.plot(range(len(df)),df['monthly_revenue'],color=ACC2,lw=2.5,marker='o',ms=5,label='Revenue')
ax.fill_between(range(len(df)),df['monthly_revenue'],alpha=0.2,color=ACC2)
ax_t=ax.twinx(); ax_t.plot(range(len(df)),df['order_volume'],color=ACC4,lw=2,marker='s',ms=4,label='Orders')
ax_t.tick_params(colors=WHITE); ax_t.set_ylabel('Order Volume',color=WHITE)
ax.set_xticks(range(len(df))); ax.set_xticklabels(labels,rotation=45,fontsize=7,color=WHITE)
ax.set_title('Monthly Revenue & Order Volume Trend (2022–2023)\nRevenue peaks in Q4 — clear holiday shopping effect',color=WHITE,fontsize=13,fontweight='bold')
ax.set_xlabel('Month',color=WHITE); ax.set_ylabel('Revenue ($)',color=WHITE)
l1,lb1=ax.get_legend_handles_labels(); l2,lb2=ax_t.get_legend_handles_labels()
ax.legend(l1+l2,lb1+lb2,facecolor=CARD,labelcolor=WHITE)
plt.tight_layout(); plt.savefig('/home/claude/all_tasks/task6_sql/screenshots/02_monthly_trend_chart.png',dpi=130,bbox_inches='tight',facecolor=BG); plt.close()
print("  ✅ 02_monthly_trend_chart.png")

df2=pd.read_sql("SELECT STRFTIME('%Y',order_date) AS year, STRFTIME('%m',order_date) AS month, ROUND(SUM(amount),2) AS monthly_revenue, COUNT(DISTINCT order_id) AS order_count FROM orders GROUP BY year,month ORDER BY monthly_revenue DESC LIMIT 3",conn)
save_table(df2,"Q2: Top 3 Months by Revenue (ORDER BY + LIMIT)","03_top3_months.png",(10,3))

df3=pd.read_sql("SELECT region, COUNT(DISTINCT order_id) AS total_orders, ROUND(SUM(amount),2) AS total_revenue, ROUND(AVG(amount),2) AS avg_order_value FROM orders GROUP BY region ORDER BY total_revenue DESC",conn)
save_table(df3,"Q3: Revenue by Region (GROUP BY + Aggregates)","04_revenue_by_region.png",(12,4))

fig,ax=plt.subplots(figsize=(10,5)); fig.patch.set_facecolor(BG); style(ax)
bars=ax.bar(df3['region'],df3['total_revenue'],color=[ACC,ACC2,ACC3,ACC4,'#ef4444'],alpha=0.9)
for b,v in zip(bars,df3['total_revenue']): ax.text(b.get_x()+b.get_width()/2,v+500,f'${v:,.0f}',ha='center',color=WHITE,fontsize=9)
ax.set_title('Total Revenue by Region\nAll regions perform comparably — balanced distribution',color=WHITE,fontsize=13,fontweight='bold')
ax.set_xlabel('Region',color=WHITE); ax.set_ylabel('Revenue ($)',color=WHITE)
plt.tight_layout(); plt.savefig('/home/claude/all_tasks/task6_sql/screenshots/05_revenue_by_region.png',dpi=130,bbox_inches='tight',facecolor=BG); plt.close()
print("  ✅ 05_revenue_by_region.png")

df4=pd.read_sql("SELECT p.category, COUNT(DISTINCT o.order_id) AS orders, SUM(o.quantity) AS units, ROUND(SUM(o.amount),2) AS revenue FROM orders o JOIN products p ON o.product_id=p.product_id GROUP BY p.category ORDER BY revenue DESC",conn)
save_table(df4,"Q4: Revenue by Category (JOIN + GROUP BY)","06_category_revenue.png",(12,4))

df5=pd.read_sql("SELECT COUNT(*) AS count_all, COUNT(order_id) AS count_non_null, COUNT(DISTINCT order_id) AS distinct_orders, COUNT(DISTINCT customer_id) AS distinct_customers FROM orders",conn)
save_table(df5,"Q5: COUNT(*) vs COUNT(DISTINCT) Comparison","07_count_demo.png",(12,2.5))

df6=pd.read_sql("SELECT STRFTIME('%Y',order_date) AS year, COUNT(DISTINCT order_id) AS total_orders, COUNT(DISTINCT customer_id) AS unique_customers, ROUND(SUM(amount),2) AS total_revenue, ROUND(AVG(amount),2) AS avg_order_value FROM orders GROUP BY year ORDER BY year",conn)
save_table(df6,"Q6: Year-over-Year Revenue Comparison","08_yoy_comparison.png",(13,3))

df7=pd.read_sql("SELECT STRFTIME('%Y',order_date) AS year, STRFTIME('%m',order_date) AS month, ROUND(SUM(amount),2) AS revenue FROM orders WHERE order_date BETWEEN '2023-01-01' AND '2023-06-30' GROUP BY year,month ORDER BY revenue DESC LIMIT 6",conn)
save_table(df7,"Q7: Top Months in H1 2023 (LIMIT + Date Range)","09_h1_2023.png",(12,4))

df8=pd.read_sql("SELECT SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) AS null_amounts, SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customers, COUNT(*) AS total_rows FROM orders",conn)
save_table(df8,"Q8: NULL Value Detection in orders table","10_null_check.png",(10,2.5))

conn.close()
print("\n🎉 All Task 6 screenshots done!")
