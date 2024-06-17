# from unittest import TestCase
#
# import pytest
#
# from cbr_website_beta.data.odin.Analysis__Chat_Threads import Analysis__Chat_Threads
# from osbot_utils.utils.Dev import pprint
# from osbot_utils.utils.Misc import list_set
#
#
# @pytest.mark.skip('FIX: takes too long - refactor to chat thread mode')
# class test_Analysis__Chat_Threads(TestCase):
#     chat_threads    : Analysis__Chat_Threads
#     max_answer_size : int
#
#     @classmethod
#     def setUpClass(cls):
#         cls.max_answer_size = 1
#         cls.chat_threads    = Analysis__Chat_Threads(max_answer_size=cls.max_answer_size)
#
#     def test_all_consolidated_threads(self):
#         assert len(self.chat_threads.all_consolidated_threads()) > 0
#
#     def test_create_consolidated_thread(self):
#         for thread__id in self.chat_threads.threads_ids():
#             consolidated_thread = self.chat_threads.create_consolidated_thread(thread__id)
#             for thread_item in consolidated_thread:
#                 assert list_set(thread_item) == ['answer', 'answer_size', 'answer_timestamp', 'index', 'prompt', 'prompt_date', 'prompt_model', 'prompt_time', 'prompt_timestamp', 'prompt_with_images', 'timespan', 'user']
#
#     def test_threads_data(self):
#         threads_data = self.chat_threads.threads_data()
#         assert len(threads_data) > 0
#
#     def test_users__consolidated_threads(self):
#         consolidated_threads__by_user = self.chat_threads.users__consolidated_threads()
#         for user, threads in consolidated_threads__by_user.items():
#             assert threads == self.chat_threads.user__consolidated_threads(user)
#
#     def test__data_analysis(self):
#         all_data = self.chat_threads.threads_data()
#         pprint(len(all_data))