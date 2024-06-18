import request.request as rq

import data.curve
import data.market
import data.pricing
import data.refer
import data.risk

"""
capdata 认证
"""


def init(name, pwd):
    auth_json = {'account': name, 'pwd': pwd}
    token = rq.post_no_token("/capdata/auth", auth_json)
    rq.save_token(token)
    print(token)


"""
   获取债券收益率曲线
   参数:
     curve -- 曲线编码
     start -- 开始时间
     end -- 结束时间
     freq -- 频率(1m, 1d, 1w)
     window -- 时间窗口 ['10:00:00','10:30:00']
   """


def get_bond_curve(curve, start, end, freq='1d', window=None):
    return data.curve.get_bond_curve(curve, start, end, freq, window)


"""
获取信用利差曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, 1d, 1w)
  window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_credit_curve(curve, start, end, freq='1d', window=None):
    return data.curve.get_credit_curve(curve, start, end, freq, window)


"""
获取利率收益率曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, 1d, 1w)
  window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_ir_curve(curve, start, end, freq='1d', window=None):
    return data.curve.get_ir_curve(curve, start, end, freq, window)


"""
获取股息分红率曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, 1d, 1w)
  window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_dividend_curve(curve, start, end, freq='1d', window=None):
    return data.curve.get_dividend_curve(curve, start, end, freq, window)


"""
获取波动率曲面数据
参数:
  surface -- 波动率曲面编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, 1d, 1w)
  window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_vol_surface(surface, start, end, freq='1d', window=None):
    return data.curve.get_vol_surface(surface, start, end, freq, window)


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
    return data.market.get_hist_mkt(inst, start, end, fields, window, mkt, freq)


"""
获取日内实时行情数据
参数:
  inst -- 产品编码列表 ['200310.IB', '190008.IB']
  fields -- 需要返回的字段(bid、ask、level1、level2、level2_5、level2_10、lix)  ['bid','ask']
  mkt -- 市场   
"""


def get_live_mkt(inst, fields, mkt=""):
    return data.market.get_live_mkt(inst, fields, mkt)


"""
获取产品定价数据
参数:
    inst -- 产品编码列表 ['2292030.IB', '2292012.IB']
    start -- 开始时间  2024-05-26
    end -- 结束时间  2024-05-29
    fields -- 需要返回的字段(price、duration、modified_duration、macaulay_duration、convexity、z_spread、dv01、bucket_dv01、cs01、
    bucket_cs01、delta、gamma、vega、term_bucket_vega、term_strike_bucket_vega、volga、term_bucket_volga、term_strike_bucket_volga、
    vanna、term_bucket_vanna、term_strike_bucket_vanna、rho)  ['duration','modified_duration']
    freq  -- 频率( 1m, 1d, 1w)
    window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_pricing(inst, start, end, fields, window=None, mkt=None, freq="1d"):
    return data.pricing.get_pricing(inst, start, end, fields, window, mkt, freq)


"""
获取产品估值数据
参数:
    inst -- 产品编码列表 ['2292030.IB', '2292012.IB']
    start -- 开始时间  2024-05-26
    end -- 结束时间  2024-05-29
    fields -- 需要返回的字段(present_value、dv01、bucket_dv01、frtb_bucket_dv01、cs01、bucket_cs01、frtb_bucket_cs01、delta、frtb_delta、
     gamma、frtb_curvature、vega、term_bucket_vega、term_strike_bucket_vega、frtb_vega、volga、term_bucket_volga、term_strike_bucket_volga、
     vanna、term_bucket_vanna、term_strike_bucket_vanna、rho)  ['dv01','cs01']
    freq  -- 频率( 1m, 1d, 1w)
    window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_valuation(inst, start, end, fields, window=None, mkt=None, freq="1d"):
    return data.pricing.get_valuation(inst, start, end, fields, window, mkt, freq)


"""
获取指定日历下的假期数据
参数:
  calendar -- 日历 CFETS
"""


def get_holidays(calendar):
    return data.refer.get_holidays(calendar)


"""
获取基准利率定义数据
参数:
  ir_index -- 基准利率编码列表 ['USDLIBOR_2W','SIBOR_12M']
"""


def get_ir_index(ir_index):
    return data.refer.get_ir_index(ir_index)


"""
获取产品信息参考数据
参数:
  inst -- 产品编码列表 ['zc17060604.SH','zc17021505.SH']
"""


def get_instrument(inst):
    return data.refer.get_instrument(inst)


"""
获取产品模板参考数据  
参数:
  inst -- 模板编码列表 ['CNY_FR_007_SWAP','SHIBOR_USDLIBOR_3M_SWAP','USDCNY_CASH','CN_TREAS_ZERO','EUR_CASH_DEPO']
"""


def get_inst_template(inst):
    return data.refer.get_inst_template(inst)


"""
获取历史模拟的利率收益率曲线数据
参数:
  curve -- 曲线编码  CN_TREAS_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_sim_ir_curve(curve, sim_date, base_date, num_sims=200):
    return data.risk.get_hist_sim_ir_curve(curve, sim_date, base_date, num_sims)


"""
获取历史模拟的信用利差曲线数据
参数:
  curve -- 曲线编码  CN_CORP_AAA_SPRD_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_sim_credit_curve(curve, sim_date, base_date, num_sims=200):
    return data.risk.get_hist_sim_credit_curve(curve, sim_date, base_date, num_sims)


"""
获取历史压力情景下利率收益率曲线数据
参数:
  curve -- 曲线编码  CN_TREAS_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_stressed_ir_curve(curve, sim_date, base_date, num_sims=200):
    return data.risk.get_hist_stressed_ir_curve(curve, sim_date, base_date, num_sims)


"""
获取历史压力情景下信用利差曲线数据
参数:
  curve -- 曲线编码  CN_CORP_AAA_SPRD_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_stressed_credit_curve(curve, sim_date, base_date, num_sims=200):
    return data.risk.get_hist_sim_credit_curve(curve, sim_date, base_date, num_sims)


"""
获取产品模拟情景下损益数据
参数:
  inst -- 产品编码  ['2171035.IB','2105288.IB']
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_inst_sim_pnl(inst, sim_date, base_date, num_sims=200):
    return data.risk.get_inst_sim_pnl(inst, sim_date, base_date, num_sims)


"""
获取产品压力情景下损益数据
参数:
  inst -- 产品编码  ['2171035.IB','2105288.IB']
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_inst_stressed_pnl(inst, sim_date, base_date, num_sims=200):
    return data.risk.get_inst_stressed_pnl(inst, sim_date, base_date, num_sims)


"""
获取产品Value-at-Risk数据
参数:
  inst -- 产品编码  2171035.IB
  sim_date -- 情景时间  2024-05-28 
  base_date -- 基础时间 2024-05-27
  fields -- 响应字段 (var, mirror_var, stressed_var, mirror_stressed_var, es, mirror_es, stressed_es, mirror_stressed_es) ['var','es']
  confidence_interval  -- 置信区间 0.95
"""


def get_inst_var(inst, sim_date, base_date, fields, confidence_interval=0.95):
    return data.risk.get_inst_var(inst, sim_date, base_date, fields, confidence_interval)
