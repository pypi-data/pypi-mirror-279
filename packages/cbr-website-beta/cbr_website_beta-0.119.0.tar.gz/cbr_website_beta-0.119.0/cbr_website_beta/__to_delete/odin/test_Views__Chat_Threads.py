# from unittest import TestCase
#
# import pytest
#
# from cbr_website_beta.apps.user.views.Views__Chat_Threads import Views__Chat_Threads
# from cbr_website_beta.utils.for_testing.App_TestCase import App_TestCase
# from osbot_utils.utils.Dev import pprint
#
#
# class test_Views__Chat_Threads(App_TestCase):
#
#     def setUp(self):
#         super().setUp()
#         self.views__chat_threads = Views__Chat_Threads()
#
#     @pytest.mark.skip('FIX: takes too long - refactor to chat thread mode')
#     def test_views(self):
#         with self.render_element(path='/user/chat-threads', username='a', element_id='chat-threads') as (_, element):
#             assert _.title() == 'User Chat Threads | Cyber Boardroom'
#             assert _.html_parser.id__text('intro-section') == '   Past Chat Threads Please see below your past conversations and debates with Athena)    '
#             pprint (_.html_parser.id__text('threads-section'))