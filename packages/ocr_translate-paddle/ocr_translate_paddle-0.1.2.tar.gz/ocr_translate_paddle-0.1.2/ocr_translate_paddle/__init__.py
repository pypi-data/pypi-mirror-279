###################################################################################
# ocr_translate-paddle - a plugin for ocr_translate                               #
# Copyright (C) 2023-present Davide Grassano                                      #
#                                                                                 #
# This program is free software: you can redistribute it and/or modify            #
# it under the terms of the GNU General Public License as published by            #
# the Free Software Foundation, either version 3 of the License.                  #
#                                                                                 #
# This program is distributed in the hope that it will be useful,                 #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                  #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   #
# GNU General Public License for more details.                                    #
#                                                                                 #
# You should have received a copy of the GNU General Public License               #
# along with this program.  If not, see {http://www.gnu.org/licenses/}.           #
#                                                                                 #
# Home: https://github.com/Crivella/ocr_translate-paddle                          #
###################################################################################
"""Plugins to enable usage of PaddleOCR in ocr_translate"""

__version__ = '0.1.2'

paddle_box_model_data = {
    'name': 'paddle/paddle-box',
    'lang': [
        'ar', 'en', 'hi', 'fr', 'fa', 'ur', 'oc', 'it', 'mr', 'ne', 'pt', 'bg', 'et', 'be', 'ga', 'te', 'hr', 'hu',
        'ta', 'id', 'af', 'is', 'az', 'ku', 'bs', 'lt', 'cs', 'lv', 'cy', 'mi', 'da', 'ms', 'mt', 'no', 'pl', 'sk',
        'sl', 'sq', 'sv', 'sw', 'tl', 'tr', 'uz', 'ug', 'vi', 'mn', 'es', 'ru', 'uk', 'nl', 'ro',
        'zht', 'zh', 'ja', 'ko', 'de', 'sr', 'av'
        ],
    'lang_code': 'iso1',
    'iso1_map': {
        'zht': 'chinese_cht',
        'zh': 'ch',
        'de': 'german',
        'ja': 'japan',
        'ko': 'korean',
        'sr': 'rs_cyrillic',
        'av': 'ava',
    },
    'entrypoint': 'paddle.box',
}

paddle_ocr_model_data = {
    'name': 'paddle/paddle-ocr',
    'lang': [
        'ar', 'en', 'hi', 'fr', 'fa', 'ur', 'oc', 'it', 'mr', 'ne', 'pt', 'bg', 'et', 'be', 'ga', 'te', 'hr', 'hu',
        'ta', 'id', 'af', 'is', 'az', 'ku', 'bs', 'lt', 'cs', 'lv', 'cy', 'mi', 'da', 'ms', 'mt', 'no', 'pl', 'sk',
        'sl', 'sq', 'sv', 'sw', 'tl', 'tr', 'uz', 'ug', 'vi', 'mn', 'es', 'ru', 'uk', 'nl', 'ro',
        'zht', 'zh', 'ja', 'ko', 'de', 'sr', 'av'
        ],
    'lang_code': 'iso1',
    'iso1_map': {
        'zht': 'chinese_cht',
        'zh': 'ch',
        'de': 'german',
        'ja': 'japan',
        'ko': 'korean',
        'sr': 'rs_cyrillic',
        'av': 'ava',
    },
    'entrypoint': 'paddle.ocr',
    'ocr_mode': 'single'
}
