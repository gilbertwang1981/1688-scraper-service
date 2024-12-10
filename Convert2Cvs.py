import pymysql
import pandas as pd
from urllib.parse import unquote

db_host = '192.168.8.12'
db_port = 13306
db_user = 'root'
db_password = 'KPqazxsw'
db_name = 'kp_sk_sync'
db_table = 'jubilee_product_scrapy'

page_size = 100
offset = 0

data_list_placeholder = []

data_for_df = []

connection = pymysql.connect(
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password,
    database=db_name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


def cleanUrls(urls):
    url_list = urls.split(', ')
    cleaned_urls = []
    for url in url_list:
        if url.startswith('//'):
            url = 'https:' + url
            for suffix in ['.jpg', '.jpeg', '.png', '.gif']:
                index = url.find(suffix)
                if index != -1:
                    url = url[:index + len(suffix)]
        cleaned_urls.append(url)

    cleaned_urls_str = ', '.join(cleaned_urls)
    return cleaned_urls_str


try:
    with connection.cursor() as cursor:
        while True:
            sql = f"""
            SELECT id, title, description, images, price, category  
            FROM {db_table}
            LIMIT {offset}, {page_size}
            """
            cursor.execute(sql)
            result = cursor.fetchall()

            if not result:
                break

            # 直接将查询结果添加到用于DataFrame的列表中
            for row in result:
                # URL 解码 title 和 description
                row['title'] = unquote(row['title'])
                row['description'] = unquote(row['description'])
                row['price'] = row['price'].split(' ')[1]
                row['category'] = row['category']

                # 处理 images 字段
                row["images"] = cleanUrls(row["images"])

                data_for_df.append(row)

            offset += page_size

    df = pd.DataFrame(data_for_df)

finally:
    connection.close()

# 导出到CSV
output_file = 'jubilee_product_scrapy.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Data exported to {output_file} successfully.")
