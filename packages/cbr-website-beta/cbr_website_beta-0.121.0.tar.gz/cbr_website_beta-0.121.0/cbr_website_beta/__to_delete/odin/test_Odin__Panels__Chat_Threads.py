# from unittest import TestCase
#
# import pytest
#
# from cbr_website_beta.apps.dev.odin.Odin__Panels__Chat_Threads import Odin__Panels__Chat_Threads
# from cbr_website_beta.flask.Flask_Site                         import Flask_Site
#
#
# class test_Odin__Panels__Chat_Threads(TestCase):
#
#     def setUp(self):
#         self.app          = Flask_Site().app()  # todo: move to setupClass
#         self.chat_threads = Odin__Panels__Chat_Threads()
#
#     @pytest.mark.skip('FIX: takes too long - refactor to chat thread mode')
#     def test_all_chat_threads(self):
#         with self.app.test_request_context(""):
#             raw_html = self.chat_threads.all_chat_threads()
#             #html     = Html_Parser(raw_html)
#             assert len(raw_html)>0
#
#     @pytest.mark.skip('FIX: takes too long - refactor to chat thread mode')
#     def test_chat_thread(self):
#         thread_id = '01cfada4-7aaf-4b23-b179-d788ec85fb44'  # todo: add better way to get syntetic data for thes chat threads
#         with self.app.test_request_context(""):
#             raw_html = self.chat_threads.chat_thread(thread_id)
#             assert len(raw_html)>0
#             #html = Html_Parser(raw_html)
#             #pprint(html)
