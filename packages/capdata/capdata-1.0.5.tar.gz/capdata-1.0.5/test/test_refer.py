import unittest
import data.refer as refer


class TestReferFunctions(unittest.TestCase):
    def test_get_holidays(self):
        calendar = refer.get_holidays('CFETS')
        if calendar is not None:
            print(calendar)
        else:
            print(calendar)

    def test_get_ir_index(self):
        ir_index_data = refer.get_ir_index(['USDLIBOR_2W', 'SIBOR_12M'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_instrument(self):
        instrument_data = refer.get_instrument(['zc17060604.SH', 'zc17021505.SH'])
        if instrument_data is not None:
            for data in instrument_data:
                print(data)
        else:
            print(instrument_data)

    def test_get_inst_template(self):
        template_data = refer.get_inst_template(
            ['CNY_FR_007_SWAP', 'SHIBOR_USDLIBOR_3M_SWAP', 'USDCNY_CASH', 'CN_TREAS_ZERO', 'EUR_CASH_DEPO'])
        if template_data is not None:
            for data in template_data:
                print(data)
        else:
            print(template_data)
