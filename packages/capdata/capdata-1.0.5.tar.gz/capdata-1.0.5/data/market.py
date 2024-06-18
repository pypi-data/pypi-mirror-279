import request.request as rq

"""
获取历史行情数据
参数:
    inst -- 产品编码列表 ['200310.IB', '190008.IB']

    start -- 开始时间  2024-05-09

    end -- 结束时间  2024-05-10

    fields -- 需要返回的字段(open、close、high、low、pre_adj_close、post_adj_close、volume、turnover、num_trades、settlement、
    open_interest、bid、ask、bid_size、ask_size、trade、trade_size、level1、level2、level2_5、level2_10、lix)  ['bid','ask']

    freq  -- 频率( 1m, 1d, 1w)

    window -- 时间窗口 ['10:00:00','10:30:00']

    mkt -- 市场
"""


def get_hist_mkt(inst, start, end, fields, window=None, mkt=None, freq="1d"):
    data_json = {'inst': inst, 'start': start, 'end': end, 'freq': freq, 'window': window, 'mkt': mkt,
                 'fields': fields}
    return rq.post_token("/capdata/get/hist/mkt", data_json)


"""
获取日内实时行情数据
参数:
  inst -- 产品编码列表 ['200310.IB', '190008.IB']

  fields -- 需要返回的字段(bid、ask、level1、level2、level2_5、level2_10、lix)  ['bid','ask']

  mkt -- 市场   
"""


def get_live_mkt(inst, fields, mkt=""):
    data_json = {'inst': inst, 'mkt': mkt, 'fields': fields}
    return rq.post_token("/capdata/get/live/mkt", data_json)
