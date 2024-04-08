import requests
from bs4 import BeautifulSoup
import time
import datetime

data = {}

def extract_stock_data(soup):
    """从BeautifulSoup对象中提取股票相关数据"""
    stock_data = soup.find("div", class_="stock-current")
    if stock_data:
        stock_price = stock_data.find("strong")
        if stock_price:
            return {
                "current_price": stock_price.text,
                "highest_price": soup.find_all('span')[4].text,
                "opening_price": soup.find_all('span')[5].text,
                "upper_limit_price": soup.find_all('span')[6].text,
                "lower_limit_price": soup.find_all('span')[8].text,
                "lowest_price": soup.find_all('span')[9].text,
                "previous_closing_price": soup.find_all('span')[10].text,
            }
    return {}
'''
def print_stock_data(stock_data):
    """打印股票数据"""
    if stock_data:
        print("当前价格为\t", stock_data["current_price"])
        print("最高价\t", stock_data["highest_price"])
        print("开盘价\t", stock_data["opening_price"])
        print("涨停价\t", stock_data["upper_limit_price"])
        print("最低价\t", stock_data["lower_limit_price"])
        print("昨收价\t", stock_data["lowest_price"])
        print("跌停价\t", stock_data["previous_closing_price"])
'''
def send(stock_data):
    #传入了一个stock_data字典
    your_token = "**********************"#填入自己的推送的token
    url = "https://api.anpush.com/push/"+your_token
    # 遍历stock_data字典，将每个股票的数据格式化为字符串，并添加到content中
     # 遍历stock_data字典，将每个股票的数据格式化为字符串，并添加到content中
    payload = {
        "title": "lxhstockpush",
        #从字典中获取多个股票的数据
        "content": "" ,
        "channel": "43322,27938,57266,22916"
    }
    #创建一个股票名和股票编号的字典 将content_line中的股票编号替换为股票名
    stock_code = {"SZ000158": "常山北明", "SH688609": "九联科技",
                  "SZ300541":"先进数通","SZ300608":"思特奇",
                  "SZ300663":"科蓝软件","SZ002174":"游族网络",
                  "SZ300047":"天源迪科"}
    count = 0
    font_table = '| 常山北明 | 九联科技 | 先进数通 | 思特奇 | 科蓝软件 | 游族网络 | 天源迪科 |\n'
    font_table +='|-----------|----------|----------|----------|----------|----------|----------|\n'
    
    for stock,data in stock_data.items():
        font_table +=f"| {data['current_price']} "
    font_table +="|\n\n"
    payload["content"] += font_table 
    payload["content"] +='\n'
    print(payload['content'])
    '''
    content_line = {
        "SZ000158": {"常山北明","当前价格: f"{stock_data["current_price"]}",最高价: 8.84,开盘价: 8.78,涨停价: 9.64,最低价: 8.67,昨收价: 7.88"},
        "SH688609": "九联科技",
        "SZ300541":"先进数通",
        "SZ300608":"思特奇",
        "SZ300663":"科蓝软件",
        "SZ002174":"游族网络",
        "SZ300047":"天源迪科"
    }
    
    '''
    stock_info_list = []
    markdown_table = '| 股票名称 | 当前价格 | 最高价 | 开盘价 | 涨停价 | 最低价 | 昨收价 | 跌停价 |\n'
    markdown_table += '|-----------|----------|----------|----------|----------|----------|----------|----------|\n'
    for stock,data in stock_data.items():
        #content_line = {"SZ000158": {"常山北明","SH688609": "九联科技",
        #"SZ300541":"先进数通",
        #"SZ300608":"思特奇",
        #"SZ300663":"科蓝软件",
        #"SZ002174":"游族网络",
        #"SZ300047":"天源迪科"
    #}}
        stock_name = stock_code.get(stock, stock)
        stock_info = {
            '股票名称': stock_name,
            '当前价格': data['current_price'],
            '最高价': data['highest_price'],
            '开盘价': data['opening_price'],
            '涨停价': data['upper_limit_price'],
            '最低价': data['lower_limit_price'],
            '昨收价': data['lowest_price'],
            '跌停价': data['previous_closing_price'],
        }
        
        stock_info_list.append(stock_info)
        
        markdown_table += f"| {stock_info['股票名称']} | {stock_info['当前价格']} | {stock_info['最高价']} | {stock_info['开盘价']} | {stock_info['涨停价']} | {stock_info['最低价']} | {stock_info['昨收价']} | {stock_info['跌停价']} |\n"
        #content_line = f"股票 {stock}: 当前价格 {data['current_price']}, 最高价 {data['highest_price']}, 开盘价 {data['opening_price']}, 涨停价 {data['upper_limit_price']}, 最低价 {data['lower_limit_price']},昨收价 {data['lowest_price']}, 跌停价 {data['previous_closing_price']}\n"
        # 将SZ000158 替换为 股票名 
        #content_line = content_line.replace(stock, stock_code[stock])      
        #替换掉content_line中的股票编号为股票名
        
        #payload['content'] += content_line
    print(markdown_table)
    payload['content'] += markdown_table
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)
def run():
    #global data  
    code = ["SZ000158","SH688609","SZ300541","SZ300608","SZ300663","SZ002174","SZ300047"]
    for i in code:
        url = "https://xueqiu.com/S/" + i 
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except requests.exceptions.RequestException as err:
            print(f'Request error: {err}')
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            stock_data = extract_stock_data(soup)
            data.update({i:stock_data})#更新数据 
    send(data)
    #        time.sleep(10)
            #print_stock_data(stock_data)
def times():
    while True:
        # 获取当前时间
        now = datetime.datetime.now()
        current_hour = now.hour

        # 检查当前时间是否是预定的运行时间
        if current_hour == 10 and now.minute == 0:
            run()
        elif current_hour == 10 and now.minute == 30:
            run()
        elif current_hour == 11:
            run()
        elif current_hour == 13:
            if now.minute == 0 or now.minute == 30:
                run()
        elif current_hour == 14:
            if now.minute == 0:
                run()

        # 等待一小段时间再次检查时间（例如5分钟）
        time.sleep(300)


# 调用运行函数
if __name__ == "__main__":
    run()
