import pandas as pd
import numpy as np
import MyTT
import os
import sys
import lyytools
from tqdm import tqdm
from datetime import datetime, timedelta
from pytdx.hq import TdxHq_API
import time
import re
import lyystkcode
api_dict = {}
error_server_list = []
k_type = {"5min":0,"15min":1,"30min":2,"60min":3,"day2":4,"week":5,"month":6,"1min":7,"1mink":8,"day":9,"season":10,"year":11}
#项目地址：https://github.com/rainx/pytdx
#更多说明：https://rainx.gitbooks.io/pytdx/content/pytdx_hq.html
# 如果需要一些常用hosts
#from pytdx.config.hosts import hq_hosts

import lyycalendar

ins_lyycalendar = lyycalendar.lyycalendar_class()


def calc_lastdate_kline_number(code:int, last_date_dict:dict, debug=False):
    """
    通过记录每个股票数据最后日期的字典，计算出该股票的日期少了几天，从而计算出通达信要下载的K线根数
    last_date_dict字典 : 类似 688549 <class 'str'> 20240206 <class 'int'>
    返回：db_last_date_int,相差天数,kline_n
    """

    db_last_date_int = last_date_dict.get(code, ins_lyycalendar.tc_before_today(49))
    if debug: print(code,type(code),db_last_date_int,type(db_last_date_int))
    相差天数 = ins_lyycalendar.计算相隔天数_byIndex(db_last_date_int, ins_lyycalendar.最近完整收盘日(),debug=debug)
    kline_n = min((相差天数 + 2) * 16, 800)
    return db_last_date_int,相差天数, kline_n


def 分钟线合成日K(df) -> pd.DataFrame:
    所有分钟线 = df.copy()
    所有分钟线['day'] = pd.to_datetime(所有分钟线['day'])
    完美日K线 = 所有分钟线.resample('D', on='day').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()
    完美日K线 = 完美日K线.reset_index(drop=False)
    完美日K线['day'] = 完美日K线['day'].dt.date
    return (完美日K线)


def 多周期K线合并(完美日K线, 十点K线,debug=False) -> pd.DataFrame:
    # print(十点K线['date'].tail(1).apply(type).value_counts())
    # 用每天早上情况生成新日线。其中，o,h,l,c都是9点半到10点K线。CC为当天收盘价。UP为high/ref(cc,1)
    mg1_test = 十点K线.loc[:, (
        'high',
        'day',
    )]
    mg1_test.rename(columns={'high': 'tenhigh'}, inplace=True)
    多周期合成K线 = pd.merge(完美日K线, mg1_test, on='day')

    多周期合成K线['up'] = list(map(lambda x, y: round((float(x) / float(y) - 1) * 100, 2), 多周期合成K线['high'], MyTT.REF(多周期合成K线['close'], 1)))
    多周期合成K线['chonggao'] = list(map(lambda x, y: round((float(x) / float(y) - 1) * 100, 2), 多周期合成K线['tenhigh'], MyTT.REF(多周期合成K线['close'], 1)))
    if debug: print("多周期合成K线=", 多周期合成K线['chonggao'])
    多周期合成K线['huitoubo'] = list(map(lambda x, y: round((1 - (float(x) / float(y))) * 100, 2), 多周期合成K线['close'], 多周期合成K线['high']))
    return (多周期合成K线)


def 合成完美K线(df) -> pd.DataFrame:
    df['shiftc'] = df['close'].shift(1)
    df['up'] = list(map(lambda x, y: x if x > y else y, df['close'], df['shiftc']))
    所有分钟线 = df.copy()
    所有分钟线['day'] = pd.to_datetime(所有分钟线['day'])
    新日K = 分钟线合成日K(所有分钟线)
    # print(新日K)
    新15分钟K = 分钟线5合15(所有分钟线)
    完美K线 = 多周期K线合并(新日K, 新15分钟K)
    # print(完美K线)
    return 完美K线


def 原始分钟df格式化(原始分钟df, debug=False):
    原始分钟df.drop(columns=['amount', 'year', 'month', 'day', 'hour', 'minute'], inplace=True)
    原始分钟df.columns = ['open', 'close', 'high', 'low', 'volume', 'day']

    原始分钟df['shiftc'] = 原始分钟df['close'].shift(1)
    原始分钟df['up'] = list(map(lambda x, y: x if x > y else y, 原始分钟df['close'], 原始分钟df['shiftc']))
    所有分钟线 = 原始分钟df.copy()
    所有分钟线['day'] = pd.to_datetime(所有分钟线['day'])

    新日K = 分钟线合成日K(所有分钟线)
    新15分钟K = 分钟线5合15(所有分钟线)

    完美df = 多周期K线合并(新日K, 新15分钟K)

    完美df['volume'] = 完美df['volume'].apply(lambda x: int(x / 10000))
    # 完美df['open'] = 完美df['open'].apply(lambda x: int(x * 100))
    # 完美df['close'] = 完美df['close'].apply(lambda x: int(x * 100))
    # 完美df['high'] = 完美df['high'].apply(lambda x: int(x * 100))
    # 完美df['low'] = 完美df['low'].apply(lambda x: int(x * 100))
    完美df['dayint'] = 完美df['day'].apply(lambda x: int(str(x)[:4] + str(x)[5:7] + str(x)[8:10]))
    完美df['day'] = 完美df['day'].apply(lambda x: str(x)[:4] +"-"+ str(x)[5:7] +"-"+ str(x)[8:10])

    # 完美df.dropna(inplace=True)

    return 完美df


def 分钟线5合15(所有分钟线) -> pd.DataFrame:
    多分钟K线 = 所有分钟线.resample('15min', on='day').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()
    多分钟K线 = 多分钟K线.reset_index(drop=False)
    多分钟K线['time'] = 多分钟K线['day'].dt.strftime('%H%M')
    多分钟K线['day'] = 多分钟K线['day'].dt.date
    # 多分钟K线.drop(columns=['day'], inplace = True)
    十点K线 = pd.DataFrame(多分钟K线, columns=['time', 'day', 'high'])[多分钟K线['time'] == '1000']
    # 成功。从result中抽取时间和日期和最高价，生成当日的冲高数据
    return (十点K线)


def 分钟线15合15(多分钟K线):
    多分钟K线['time'] = 多分钟K线['day'].dt.strftime('%H%M')
    多分钟K线['day'] = 多分钟K线['day'].dt.date
    多分钟K线 = 多分钟K线.reset_index(drop=True)[多分钟K线['time'] <= '1000']
    df_grouped = 多分钟K线.groupby('day').max()
    #多分钟K线=多分钟K线[['day','high']]
    # 成功。从result中抽取时间和日期和最高价，生成当日的冲高数据
    df_grouped = (df_grouped.reset_index(drop=False))
    selected_columns = df_grouped[['day', 'high']]
    selected_columns.rename(columns={'high': 'chonggao'})
    #print("多分钟K线\n", selected_columns)
    return (selected_columns)


def 原始15分钟df格式化(原始分钟df, debug=False):
    原始分钟df.drop(columns=['amount', 'year', 'month', 'day', 'hour', 'minute'], inplace=True)
    原始分钟df.columns = ['open', 'close', 'high', 'low', 'volume', 'day']

    原始分钟df['shiftc'] = 原始分钟df['close'].shift(1)
    # 原始分钟df['up'] = list(map(lambda x, y: x if x > y else y, 原始分钟df['close'], 原始分钟df['shiftc']))
    所有分钟线 = 原始分钟df.copy()
    所有分钟线['day'] = pd.to_datetime(所有分钟线['day'])
    新日K = 分钟线合成日K(所有分钟线)

    新15分钟K = 分钟线15合15(所有分钟线)

    完美df = 多周期K线合并(新日K, 新15分钟K)

    完美df['volume'] = 完美df['volume'].apply(lambda x: int(x / 1000000))
    # 完美df['open'] = 完美df['open'].apply(lambda x: int(x * 100))
    # 完美df['close'] = 完美df['close'].apply(lambda x: int(x * 100))
    # 完美df['high'] = 完美df['high'].apply(lambda x: int(x * 100))
    # 完美df['low'] = 完美df['low'].apply(lambda x: int(x * 100))
    完美df['day'] = 完美df['day'].apply(lambda x: int(str(x)[:4] + str(x)[5:7] + str(x)[8:10]))
    # 完美df.dropna(inplace=True)
    return 完美df


def wmdf15(api, stk_code_num, to_down_kline, debug=False) -> pd.DataFrame:
    debug = True
    if debug:
        print("函数名：", sys._getframe().f_code.co_name, ": try to get wmdf",stk_code_num, to_down_kline)
    if debug:
        t0 = datetime.now()
    try:
        df = 通达信下载原始分钟K线(api, stk_code_num, to_down_kline, debug=debug)
        if df.empty:
            raise Exception("通达信下载原始分钟K线 error: DataFrame must not be empty")
    except Exception as e:
        print("Fuction: wmdf, try to run 通达信下载原始分钟线 error。stk_code_num:", stk_code_num, "to_down_kline:", to_down_kline, "api:", api, e)
        print("wmdf error:", e)
        return None
    if debug:
        lyytools.测速(t0, "通达信下载原始K线")
    t1 = datetime.now()

    try:
        wmdf = 原始15分钟df格式化(df)
        if debug:
            lyytools.测速(t1, "df格式转换")
    except Exception as e:
        print("error函数名：", sys._getframe().f_code.co_name, ": try to get wmdf")
        print(" stk_code_num=", stk_code_num, " to_down_line=", to_down_kline, "try to run wmdf = 原始15分钟df格式化(df) error:", e)
        return None

    return wmdf


def wmdf(api, stk_code_num, to_down_kline, server_ip=None, debug=False) -> pd.DataFrame:
    if debug: print("函数名：", sys._getframe().f_code.co_name, ": try to get wmdf")
    t0 = datetime.now()
    try:
        if debug: print("准备开始下载原始K线，IP=",api.ip)
        
        df = 通达信下载原始分钟K线(api, stk_code_num, to_down_kline, debug=debug)

        time = datetime.now() - t0
        if time>timedelta(seconds=0.3):
            print("通达信下载原始K线下载时间过长,IP="+api.ip,time)
            return None
        else:
            print(time)
        
        if df.empty:
            raise Exception("通达信下载原始分钟K线 error: DataFrame must not be empty")
    except Exception as e:
        print("Fuction: wmdf, try to run 通达信下载原始分钟线 error。stk_code_num:", stk_code_num, "to_down_kline:", to_down_kline, "api:", api, e)
        print("wmdf error:", e)
        return None
    if debug:
        lyytools.测速(t0, "通达信下载原始K线")
    t1 = datetime.now()

    try:
        wmdf = 原始分钟df格式化(df)
        if debug: print(wmdf)
    except Exception as e:
        print("error函数名：", sys._getframe().f_code.co_name, ": try to get wmdf")
        print("api=", api, " stk_code_num=", stk_code_num, " to_down_line=", to_down_kline, "try to run wmdf = 原始分钟df格式化(df) error:", e)
        return None
    if debug:
        lyytools.测速(t1, "df格式转换")
    return wmdf



def mk_api_dcit(svlist, debug=False) -> dict:
    api_dict = {}
    if debug:
        print("函数名：", sys._getframe().f_code.co_name)

    for i in tqdm(range(len(svlist)),desc="mk_api_dcit"):
        try:
            serverip, tdxport = svlist[i], 7709
            if debug:
                print("mk_api_dict: try to con to ", serverip)
            exec("api" + str(i) + " = TdxHq_API(multithread=False,heartbeat=False,auto_retry=True)")
            exec("api" + str(i) + ".connect(serverip, tdxport)")
            api_dict[svlist[i]]=eval("api" + str(i))
        except Exception as e:
            print("mk_api_dcit error", e)
    print("mk_api_dcit: All done")
    return api_dict




def 通达信下载原始分钟K线_simple(api, stkcode: str, 要下载的K线数量=800, debug=False) -> pd.DataFrame:
    """
    通达信下载原始分钟K线(tdxserverip:str, 股票数字代码:str, 开始日期:str, 结束日期, debug=False)
    """
    市场代码 = lyystkcode.get_market(stkcode)
    tdxserverip = "120.79.210.76"
    #api.connect(tdxserverip,7709)

    df_tdx = api.to_df(api.get_security_bars(1, 市场代码, stkcode, 0, 要下载的K线数量))

    return (df_tdx)


def 通达信下载原始分钟K线by_ip(tdxserverip, stkcode, retry=True, debug=False):
    市场代码 = lyystkcode.get_market(stkcode)
    print(f"market={市场代码}, code={stkcode}")

    api = TdxHq_API(heartbeat=True, multithread=False)
    api.connect(tdxserverip, 7709)
    df = api.to_df(api.get_security_bars(1, 市场代码, stkcode, 0, 800))
    return df
    # K线种类： 0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线 5 周K线 6 月K线 7 1分钟 81分钟K线 9 日K线 10 季K线 11 年K线


def test_servers_speed(ip, debug=False):
    """
    测试通达信服务器速度

    Args:
        ip (str): tdx服务器地址
        debug (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """

    api = TdxHq_API()
    api.connect(ip, 7709)
    start_time = time.time()
    result = api.get_security_bars(9, 2, "430510", 0, 10)
    if result is None or len(result)<1:
        return 9
    # api.get_security_count(0)
    end_time = time.time()
    api.disconnect()
    latency = end_time - start_time
    latency = round(latency, 2)
    latency_with_unit = f"{latency:.2f}秒"
    if debug:
        print("测速结果：", ip, latency_with_unit)
    return latency


def iplist_add_latency(iplist, debug=False):
    ip_latency_dict = {}

    for i in tqdm(range(len(iplist)), desc="通达信服务器速度测试"):
        ip = iplist[i]  # 测速
        try:
            latency = test_servers_speed(ip, debug=debug)
            if latency is not None and latency < 0.1:
                ip_latency_dict[ip] = latency
            else:
                if debug:
                    print(f"{ip}速度太慢，丢弃")
                continue
        except Exception as e:
            print("test_servers_speed error:", e)

    return ip_latency_dict


def update_latency_to_mysql(engine, ip_latency_dict, debug=False):
    if engine is None:
        import lyymysql
        from lyycfg import cfg
        cfg.get_engine_conn()
        engine = cfg.engine
        conn = cfg.conn
    if len(ip_latency_dict) >80:
        latency_df = pd.DataFrame(list(ip_latency_dict.items()), columns=['IP', 'latency'])

        # 将DataFrame写入MySQL数据库中的表stock_tdx_latency
        latency_df.to_sql('stock_tdx_servers', conn, if_exists='replace', index=False)
        conn.close()
    else:
        print("ip_latency_dict长度太短，是不是丢失很多通达信行情服务器IP，不写入数据库")


def get_fast_tdx_server_ip_list(iplist, latency, debug=False) -> list:
    """
    获取速度快延时<latency的通达信服务器地址列表
    """
    debug = True
    latency_dict = iplist_add_latency(iplist, debug=debug)
    fast_server_ip_list = [key for key, value in latency_dict.items() if value < latency]

    return fast_server_ip_list


def df_table(df, index):
    import prettytable as pt
    #利用prettytable对输出结果进行美化,index为索引列名:df_table(df,'market')
    tb = pt.PrettyTable()
    # 如果为trade_time为index转换为日期类型，其它不用管。
    if index == "trade_time":
        df = df.set_index(index)
        df.index = pd.DatetimeIndex(df.index)
    # df.reset_index(level=None, drop=True, inplace=True, col_level=0, col_fill='')
    df = df.reset_index(drop=True)
    tb.add_column(index, df.index)  #按date排序
    for col in df.columns.values:  #df.columns.values的意思是获取列的名称
        # print('col',col)
        # print('df[col]',df[col])
        tb.add_column(col, df[col])
    #print(tb)
    return tb

def get_tdx_server_ip_list_mysql(engine=None, debug=False):
    if engine is None:
        import lyymysql
        from lyycfg import cfg
        cfg.get_engine_conn()
        engine = cfg.engine
        conn = cfg.conn
    # 从表stock_tdx_servers读取IP字段
    server_df = pd.read_sql_table('stock_tdx_servers', conn)
    server_list = server_df['ip'].tolist()
    return server_list
    

    
def initialize_api(server_ip, debug=False):
    global api_dict  # 声明api_dict是全局变量

    if server_ip not in api_dict.keys():
        try:
            api = TdxHq_API(multithread=False, heartbeat=False, auto_retry=True)
            api.connect(server_ip, 7709)
            if len(api_dict) == 0:
                df_tdx = api.to_df(api.get_security_bars(1, 0, "000001", 0, 20))
                print(df_tdx)
            if debug: print("serverip=", server_ip, "api=", api)
            api_dict[server_ip] = api
            return api
        except Exception as e:
            print("initialize_api error:xx", e)
            if len(api_dict)>0:
                import random
                print("随机取一个")
                x = random.randint(0, len(api_dict)-1)
                print("随机取一个",api_dict[x])

                return api_dict[x]
            else:
                return initialize_api("119.147.212.81",True)
    else:
        if debug: print(" api_dict[server_ip] is already in api_dict")
        try:
            return api_dict[server_ip]
        except Exception as e:
            print(e)


def mk_api_list(svlist, debug=False):
    api_list = []
    if debug:
        print("函数名：" + sys._getframe().f_code.co_name)
    for i in tqdm(range(len(svlist)),desc="mk_api_list"):
        try:
            serverip, tdxport = svlist[i], 7709
            if debug:
                print("mk_api_list: try to con to " + serverip)
            exec("api" + str(i) + " = TdxHq_API(multithread=False,heartbeat=False,auto_retry=True)")
            exec("api" + str(i) + ".connect(serverip, tdxport)")
            api_list.append(eval("api" + str(i)))
        except Exception as e:
            # sql = "UPDATE stock_tdx_servers SET error_times = error_times + 1 WHERE ip = '"+serverip+"'"
            # conn.execute(text(sql))
            global error_server_list
            error_server_list.append(serverip)
            print(f"mk_api_list ip={serverip}, errmsg=" + str(e))
    print("error server=",error_server_list)
    print("mkapi: All done")
    return api_list

def read_cache(cache_file):
    with open(cache_file, "r", encoding='utf-8') as f:
        faster_server_list = [item.strip() for item in f.readlines()]
    return faster_server_list




def perfect_new_fast_server_list(cache_file="faster_tdxserver_cache.ini", interval=24, next_function=None, timeout=0.6, debug=False):
    cache_file = os.path.join(os.getcwd(), cache_file)
    debug=True
    # 读取缓存文件以获取服务器列表
    if os.path.isfile(cache_file):
        print("Cache file exists")
        mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        one_hour_ago = datetime.now() - timedelta(hours=interval)

        # 1.缓存存在且新鲜
        if mod_time >= one_hour_ago and mod_time <= datetime.now():
            if debug: print("Cache file is fresh, reading it")
            server_list = read_cache(cache_file)
            #os.utime(cache_file, (time.time(), time.time()))
            return server_list
            
            
        # 2.缓存存在但不新鲜    
        else:
            # 2.1 从next_function获取新的服务器列表
            if next_function is not None:
                server_list = next_function()
            # 2.2 实在不行，使用旧的缓存
            if next_function is None or server_list is None:
                print("next_function is None or server_list is None, using old cache")
                server_list= read_cache(cache_file)
                
            faster_server_list = get_fast_tdx_server_ip_list(server_list, timeout, debug)
            with open(cache_file, "w", encoding="utf-8") as f:
                f.writelines('%s\n' % item for item in faster_server_list)    
            return faster_server_list

    #缓存不存在
    else:        
        print("cache file not exists")        
        if next_function is not None:
            server_list = next_function()
            print("No file or not fresh, downloading new by next function")
        else:                    
            print("No file or not fresh, downloading new from pytdx.config.hosts")
            from pytdx.config.hosts import hq_hosts
            server_list = [host[1] for host in hq_hosts]
    #对服务器列表进行测速
    faster_server_list = get_fast_tdx_server_ip_list(server_list, timeout, debug)
    
    #保存到缓存以备后用
    with open(cache_file, "w", encoding="utf-8") as f:
        f.writelines('%s\n' % item for item in faster_server_list)    
    return faster_server_list

def get_cg_dict(api, stkcode: str, 要下载的K线数量=800, debug=False) -> pd.DataFrame:
    """
    通达信下载原始分钟K线(tdxserverip:str, 股票数字代码:str, 开始日期:str, 结束日期, debug=False)
    """
    市场代码 = int(stkcode[0].find('6')) + 1
    print(f"market={市场代码}, code={stkcode}")
    tdxserverip = "120.79.210.76"
    #api.connect(tdxserverip,7709)
    df = api.to_df(api.get_security_bars(1, 市场代码, stkcode, 0, 要下载的K线数量))
    tb = df_table(df, "datetime")
    #print(tb)
    # 将 "datetime" 列转换为日期时间类型
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['day'] = df['datetime'].dt.date
    # 提取小时和分钟
    df['time'] = df['datetime'].dt.time
    time_obj = datetime.strptime("10:00", "%H:%M").time()
    # 选取满足条件的记录
    selected_data = df[(df['time'] <= time_obj)]
    #print(selected_data)
    # 按日期分组，并计算每天最大高点值
    max_high_per_day = selected_data.groupby('day')['high'].max()
    #print(type(max_high_per_day))
    #max_high_per_day.rename(columns={'high': 'cg'}, inplace=True)
    # 将结果转换为字典形式
    result_dict = max_high_per_day.to_dict()
    # for key in result_dict.keys():
    #     print(f"Key: {key}, Type: {type(key)}")
    return max_high_per_day, result_dict


def newwmdf(api, code, daykline_n):
    cg_df, cg_dict = get_cg_dict(api, code, daykline_n * 16)
    market = int(code.startswith("6"))
    df = api.to_df(api.get_security_bars(9, market, code, 0, 50))
    df['day'] = pd.to_datetime(df['datetime']).dt.date
    result = df.merge(cg_df, on='day', how='left')
    result = result.rename(columns={'high_y': 'cg'})
    return result


def 测试15(api, stkcode: str, 要下载的K线数量=800, debug=False) -> pd.DataFrame:
    """
    通达信下载原始分钟K线(tdxserverip:str, 股票数字代码:str, 开始日期:str, 结束日期, debug=False)
    """
    市场代码 = int(stkcode[0].find('6')) + 1
    #print(f"market={市场代码}, code={stkcode}")
    tdxserverip = "120.79.210.76"
    #api.connect(tdxserverip,7709)
    df_tdx_15min = api.to_df(api.get_security_bars(1, 市场代码, stkcode, 0, 要下载的K线数量))
    tb = df_table(df_tdx_15min, "datetime")
    print(tb)
    wmdf = 原始15分钟df格式化(df_tdx_15min)
    return wmdf




def 通达信下载原始分钟K线(api, 股票数字代码, 要下载的K线数量,ktype='15min',start_index=0, debug=False) -> pd.DataFrame:
    """
    通达信下载原始分钟K线(tdxserverip:str, 股票数字代码:str, 要下载的K线数量:str,ktype:15min,1min,day 表明分钟还是日线 结束日期, debug=False)
    """
    fun_name = sys._getframe().f_code.co_name
    t0 = datetime.now()
    if debug:
        print("函数名：", fun_name)
    # if not api.is_connected():
    #     print("没有连接")
    #     api.connect("120.79.210.76", 7709)  

    市场代码 = lyystkcode.get_market(股票数字代码)
    if debug:print("市场代码=",市场代码,"，股票数字代码=",股票数字代码,",",k_type[ktype],",要下载的K线数量=",要下载的K线数量)
    # api = TdxHq_API()
    # tdxserverip = "120.79.210.76"
    # api.connect(tdxserverip, 7709)
    # 股票数字代码="873833"
    print("开始下载："+股票数字代码)
    df_tdx = api.to_df(api.get_security_bars(k_type[ktype], 市场代码, 股票数字代码, start_index, 要下载的K线数量))
    print("下载完成： "+股票数字代码)
    # df_tdx = api.to_df(api.get_security_bars(9, 2, "833075", 0, 要下载的K线数量))
    # print(df_tdx)

    # if len(df_tdx) < 1:
    #     print(f"{fun_name}, code= {股票数字代码}  空数据，请检查@ {str(api)} + 市场代码={市场代码} to{ str(要下载的K线数量)}")
    # if debug: print(len(df_tdx), "条数据")
    # if debug: print(df_tdx)
    # df_tdx = api.to_df(api.get_security_bars(9, 0, "000001", 0, 要下载的K线数量))
    # print("000001,len=",len(df_tdx))

    # time.sleep(33333)
    return (df_tdx)

def get_fenshi(api, 股票数字代码, 要下载的K线数量,ktype='15min', debug=False) -> pd.DataFrame:
    data = api.get_history_transaction_data()
    
    
    

if __name__ == "__main__":
    server_list = get_tdx_server_ip_list_mysql()
    print("server_list=",server_list)
    ip_latency_dict = iplist_add_latency(server_list)
    update_latency_to_mysql(None, ip_latency_dict)
    print("all done")
    time.sleep(3333)
    
    tdxserverip = "120.79.210.76"
    api = TdxHq_API()
    api.get_history_transaction_data()
    api.connect(tdxserverip, 7709)
    d = {}
    d[tdxserverip]=api
    
    通达信下载原始分钟K线(d[tdxserverip],"837212",800)
    
    #错在昨天，cg应该大于5，价格为11.59，cg实际为2.74
    #df = 通达信下载原始分钟K线by_ip(tdxserverip, "300313")
    print("-" * 80)
    api = TdxHq_API()
    # api.isconnected()
    api.connect(tdxserverip, 7709)
    print(api.to_df(api.get_security_bars(9, 2, "873833", 0, 800)))
    exit()

    df2 = wmdf15(api, "880863", 60)
    print("df", df2)
    exit()
    df22 = df_table(df2, "datetime")
    print(df22)
    wmdf = 原始分钟df格式化(df2)
    print(wmdf)
    df3 = df_table(wmdf, "day")

    print(df3)
    exit()
    from pytdx.hq import TdxHq_API
    api = TdxHq_API()
    api.connect('221.237.182.7', 7709)

    data = api.get_k_data('000001', '19900101', '20211231')

    print(data)
    exit()
