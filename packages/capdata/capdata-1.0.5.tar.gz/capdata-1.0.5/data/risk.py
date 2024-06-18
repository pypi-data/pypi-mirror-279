import request.request as rq

"""
获取历史模拟的利率收益率曲线数据
参数:
  curve -- 曲线编码  CN_TREAS_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_sim_ir_curve(curve, sim_date, base_date, num_sims=200):
    data_json = {'curve': curve, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/hist/sim/ir/curve", data_json)


"""
获取历史模拟的信用利差曲线数据
参数:
  curve -- 曲线编码  CN_CORP_AAA_SPRD_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_sim_credit_curve(curve, sim_date, base_date, num_sims=200):
    data_json = {'curve': curve, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/hist/sim/credit/curve", data_json)


"""
获取历史压力情景下利率收益率曲线数据
参数:
  curve -- 曲线编码  CN_TREAS_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_stressed_ir_curve(curve, sim_date, base_date, num_sims=200):
    data_json = {'curve': curve, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/hist/stressed/ir/curve", data_json)


"""
获取历史压力情景下信用利差曲线数据
参数:
  curve -- 曲线编码  CN_CORP_AAA_SPRD_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_stressed_credit_curve(curve, sim_date, base_date, num_sims=200):
    data_json = {'curve': curve, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/hist/stressed/credit/curve", data_json)


"""
获取产品模拟情景下损益数据
参数:
  inst -- 产品编码  ['2171035.IB','2105288.IB']
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_inst_sim_pnl(inst, sim_date, base_date, num_sims=200):
    data_json = {'inst': inst, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/inst/sim/pnl", data_json)


"""
获取产品压力情景下损益数据
参数:
  inst -- 产品编码  ['2171035.IB','2105288.IB']
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_inst_stressed_pnl(inst, sim_date, base_date, num_sims=200):
    data_json = {'inst': inst, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/inst/stressed/pnl", data_json)


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
    data_json = {'inst': inst, 'simDate': sim_date, 'baseDate': base_date, 'fields': fields,
                 'confidenceInterval': confidence_interval}
    return rq.post_token("/capdata/get/inst/var", data_json)
