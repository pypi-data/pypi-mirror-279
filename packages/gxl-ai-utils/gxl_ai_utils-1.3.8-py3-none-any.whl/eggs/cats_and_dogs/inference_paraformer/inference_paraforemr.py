import tqdm

from gxl_ai_utils.utils import utils_file

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os
import sys

os.environ['CUDA_VISIBLE_DEVICES'] = '1'
inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    model_revision="v2.0.4")
utils_file.makedir_sil('./output_dir_1')
text_res = inference_pipeline("/home/work_nfs7/depression_dataset/shukang_samplewav/22162.wav")
print(text_res)
wav_dict = utils_file.load_dict_from_scp("./shukang_wav.scp")
res_text_list = []
for key, path in tqdm.tqdm(wav_dict.items(), total=len(wav_dict)):
    print(key, path)
    if not os.path.exists(path):
        continue
    try:
        text_res = inference_pipeline(path)
        print(f'{key} {text_res["text"]}')
        res_text_list.append(f'{key} {text_res["text"]}')
    except Exception as e:
        print(e)
        continue
utils_file.write_list_to_file(res_text_list, "./output_dir_2/shukang_text.list")
