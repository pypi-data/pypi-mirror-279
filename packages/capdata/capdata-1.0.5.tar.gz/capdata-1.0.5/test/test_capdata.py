import unittest
import capdata
import pandas


class TestApiFunctions(unittest.TestCase):
    def test_init(self):
        capdata.init("xxxx", "xxxx")

    def test_get_bond_curve(self):
        curve_data = capdata.get_bond_curve("CN_TREAS_STD", '2024-05-27 00:00:00', '2024-05-27 18:00:00', '1m')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_credit_curve(self):
        curve_data = capdata.get_credit_curve("CN_RAILWAY_SPRD_STD", '2024-05-27 00:00:00', '2024-05-27 18:00:00',
                                              '1m')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_ir_curve(self):
        curve_data = capdata.get_ir_curve("CNY_FR_007", '2024-05-22 00:00:00', '2024-05-27 18:00:00', '1d')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_dividend_curve(self):
        curve_data = capdata.get_dividend_curve("50ETF_SSE_DIVIDEND", '2024-06-04 00:00:00', '2024-06-06 18:00:00', '1d')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_vol_surface(self):
        curve_data = capdata.get_vol_surface("USDCNY_VOL_SVI", '2024-06-16 00:00:00', '2024-06-18 18:00:00', '1d')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_hist_mkt(self):
        market_data = capdata.get_hist_mkt(['200310.IB', '190008.IB'], '2024-05-09', '2024-05-10 00:00:00',
                                           ['bid', 'ask'],
                                           )
        market_data = pandas.DataFrame(market_data)
        print(market_data)

    def test_get_live_mkt(self):
        market_data = capdata.get_live_mkt(['200310.IB', '190008.IB'], ['bid', 'ask'],
                                           )
        market_data = pandas.DataFrame(market_data)
        print(market_data)

    def test_get_pricing(self):
        pricing_data = capdata.get_pricing(['2292030.IB', '2292012.IB'], '2024-05-26', '2024-05-29 00:00:00',
                                           ['duration', 'modified_duration'],
                                           freq='1m')
        if pricing_data is not None:
            for data in pricing_data:
                print(data)
        else:
            print(pricing_data)

    def test_get_valuation(self):
        pricing_data = capdata.get_valuation(['2292030.IB', '2292012.IB'], '2024-05-26', '2024-05-29 00:00:00',
                                             ['present_value', 'dv01', 'cs01'],
                                             freq='1m')
        if pricing_data is not None:
            for data in pricing_data:
                print(data)
        else:
            print(pricing_data)


    def test_get_holidays(self):
        calendar = capdata.get_holidays('CFETS')
        if calendar is not None:
            print(calendar)
        else:
            print(calendar)

    def test_get_ir_index(self):
        ir_index_data = capdata.get_ir_index(['USDLIBOR_2W', 'SIBOR_12M'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_instrument(self):
        instrument_data = capdata.get_instrument(['zc17060604.SH', 'zc17021505.SH'])
        if instrument_data is not None:
            for data in instrument_data:
                print(data)
        else:
            print(instrument_data)

    def test_get_inst_template(self):
        template_data = capdata.get_inst_template(
            ['CNY_FR_007_SWAP', 'SHIBOR_USDLIBOR_3M_SWAP', 'USDCNY_CASH', 'CN_TREAS_ZERO', 'EUR_CASH_DEPO'])
        if template_data is not None:
            for data in template_data:
                print(data)
        else:
            print(template_data)


    def test_get_hist_sim_ir_curve(self):
        risk_data = capdata.get_hist_sim_ir_curve('CN_TREAS_STD', '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_sim_credit_curve(self):
        risk_data = capdata.get_hist_sim_credit_curve('CN_CORP_AAA_SPRD_STD', '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_stressed_ir_curve(self):
        risk_data = capdata.get_hist_stressed_ir_curve('CN_TREAS_PRIME', '2024-05-11', '2024-05-10')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_stressed_credit_curve(self):
        risk_data = capdata.get_hist_stressed_credit_curve('CN_SP_MTN_AAA_SPRD_STD', '2024-05-11', '2024-05-10')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_inst_sim_pnl(self):
        risk_data = capdata.get_inst_sim_pnl(['2171035.IB', '2105288.IB'], '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_inst_stressed_pnl(self):
        risk_data = capdata.get_inst_stressed_pnl(['2171035.IB', '2105288.IB'], '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_inst_var(self):
        risk_data = capdata.get_inst_var("2171035.IB", '2024-05-28', '2024-05-27', ['var', 'es'])
        if risk_data is not None:
            print(risk_data)
        else:
            print(risk_data)

