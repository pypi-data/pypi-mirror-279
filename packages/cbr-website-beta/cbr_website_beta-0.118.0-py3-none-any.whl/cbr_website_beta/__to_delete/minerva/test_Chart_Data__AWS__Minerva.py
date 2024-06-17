# from unittest import TestCase
#
# import pytest
#
# from osbot_utils.utils.Misc import list_set
#
# from cbr_website_beta.bots.Minerva_Rest_API import Minerva_Rest_API
# from osbot_utils.utils.Dev import pprint
#
# from cbr_website_beta.chart_data.minerva.Chart_Data__AWS__Minerva import Chart_Data__AWS__Minerva
#
#
# class test_Chart_Data__AWS__Minerva(TestCase):
#
#     def setUp(self) -> None:
#         self.chart_data = Chart_Data__AWS__Minerva()
#
#     @pytest.mark.skip('todo: fix Minerva who is returning: Internal Server Error on this endpoint')
#     def test_aws_cost_explorer(self):
#         result = self.chart_data.aws_cost_explorer()
#         #pprint(result)
#         assert list_set(result) == ['all_costs', 'all_days', 'all_services']

# views

# @pytest.mark.skip("to implement")
# def test_aws_costs__direct(self):
#     html = aws_costs()
#     assert html is not None
