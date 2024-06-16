"""
@File  :do_convert_wav_text_scp_to_jsonl.py
@Author:Xuelong Geng
@Date  :2024/6/5 2:26
@Desc  :
"""
import os

from gxl_ai_utils.utils import utils_file
import sys
arg_num = len(sys.argv)
if arg_num < 4:
    print("Usage: python do_convert_wav_text_scp_to_jsonl.py wav_path text_path output_dir")
    exit(1)
argv_1 = sys.argv[1]
if argv_1 == "--help" or argv_1 == "-h":
    print("Usage: python do_convert_wav_text_scp_to_jsonl.py wav_path text_path output_dir")
    exit(1)

wav_path = sys.argv[1]
text_path = sys.argv[2]
output_dir = sys.argv[3]
output_path = os.path.join(output_dir, "data.list")
utils_file.do_convert_wav_text_scp_to_jsonl(wav_path, text_path, output_path)