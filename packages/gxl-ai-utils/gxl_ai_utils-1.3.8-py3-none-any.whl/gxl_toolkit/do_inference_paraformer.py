import tqdm

from gxl_ai_utils.utils import utils_file

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os
import sys

arg_num = len(sys.argv)

input_wav_scp_path = sys.argv[1]
output_dir = sys.argv[2]
if len(sys.argv) > 3:
    lab_text_path = sys.argv[3]
else:
    lab_text_path = None

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    model_revision="v2.0.4")
utils_file.makedir_sil(output_dir)

wav_dict = utils_file.load_dict_from_scp(input_wav_scp_path)
res_text_list = []
for key, path in tqdm.tqdm(wav_dict.items(), total=len(wav_dict)):
    utils_file.logging_print(key, path)
    if not os.path.exists(path):
        continue
    try:
        text_res = inference_pipeline(path)
        utils_file.logging_print(f'{key} {text_res["text"]}')
        res_text_list.append(f'{key} {text_res["text"]}')
    except Exception as e:
        print(e)
        continue
utils_file.write_list_to_file(res_text_list, os.path.join(output_dir, 'text_hyp'))
if lab_text_path is not None:
    utils_file.do_compute_wer(lab_text_path, os.path.join(output_dir, 'text_hyp'), output_dir)


