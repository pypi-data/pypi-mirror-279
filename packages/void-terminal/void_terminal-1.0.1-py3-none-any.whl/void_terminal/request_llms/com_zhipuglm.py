# encoding: utf-8
# @Time   : 2024/1/22
# @Author : Kilig947 & binary husky
# @Descr   : Compatible with the Latest ZhiPu AI
from void_terminal.toolbox import get_conf
from zhipuai import ZhipuAI
from void_terminal.toolbox import get_conf, encode_image, get_pictures_list
import logging, os


def input_encode_handler(inputs:str, llm_kwargs:dict):
    if llm_kwargs["most_recent_uploaded"].get("path"):
        image_paths = get_pictures_list(llm_kwargs["most_recent_uploaded"]["path"])
    md_encode = []
    for md_path in image_paths:
        type_ = os.path.splitext(md_path)[1].replace(".", "")
        type_ = "jpeg" if type_ == "jpg" else type_
        md_encode.append({"data": encode_image(md_path), "type": type_})
    return inputs, md_encode


class ZhipuChatInit:

    def __init__(self):
        ZHIPUAI_API_KEY, ZHIPUAI_MODEL = get_conf("ZHIPUAI_API_KEY", "ZHIPUAI_MODEL")
        if len(ZHIPUAI_MODEL) > 0:
            logging.error('ZHIPUAI_MODEL configuration option is deprecated，Please configure in LLM_MODEL')
        self.zhipu_bro = ZhipuAI(api_key=ZHIPUAI_API_KEY)
        self.model = ''

    def __conversation_user(self, user_input: str, llm_kwargs:dict):
        if self.model not in ["glm-4v"]:
            return {"role": "user", "content": user_input}
        else:
            input_, encode_img = input_encode_handler(user_input, llm_kwargs=llm_kwargs)
            what_i_have_asked = {"role": "user", "content": []}
            what_i_have_asked['content'].append({"type": 'text', "text": user_input})
            if encode_img:
                if len(encode_img) > 1:
                    logging.warning("glm-4v only supports one image,Only the first image will be processed")
                    print("glm-4v only supports one image,Only the first image will be processed")
                img_d = {"type": "image_url",
                            "image_url": {
                                "url": encode_img[0]['data']
                            }
                        }
                what_i_have_asked['content'].append(img_d)
            return what_i_have_asked

    def __conversation_history(self, history:list, llm_kwargs:dict):
        messages = []
        conversation_cnt = len(history) // 2
        if conversation_cnt:
            for index in range(0, 2 * conversation_cnt, 2):
                what_i_have_asked = self.__conversation_user(history[index], llm_kwargs)
                what_gpt_answer = {
                    "role": "assistant",
                    "content": history[index + 1]
                }
                messages.append(what_i_have_asked)
                messages.append(what_gpt_answer)
        return messages

    @staticmethod
    def preprocess_param(param, default=0.95, min_val=0.01, max_val=0.99):
        """Preprocessing Parameters，Ensure it is within the permissible range，And handle precision issues"""
        try:
            param = float(param)
        except ValueError:
            return default

        if param <= min_val:
            return min_val
        elif param >= max_val:
            return max_val
        else:
            return round(param, 2)  # Selectable precision，Currently is two decimal places

    def __conversation_message_payload(self, inputs:str, llm_kwargs:dict, history:list, system_prompt:str):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        self.model = llm_kwargs['llm_model']
        messages.extend(self.__conversation_history(history, llm_kwargs))  # Handle History
        if inputs.strip() == "": # Handle the error caused by empty input://github.com/binary-husky/gpt_academic/issues/1640 prompt {"error":{"code":"1214","message":"messages[1]:contentandtool_calls 字段不能同When为空"}
            inputs = "."    # Spaces, line breaks, and empty strings will all result in errors，Therefore, replace it with the most meaningless point
        messages.append(self.__conversation_user(inputs, llm_kwargs))  # Handle user dialogue
        """
        Sampling temperature，Control the randomness of output，Must be a positive number
        The value range is：(0.0, 1.0)，Cannot equal 0，Default value is 0.95，
        The Larger the Value，Would make the output more random，More creative;
        The smaller the value，The output will be more stable or certain
        It is recommended to adjust the top_p or temperature parameters according to the application scenario，But do not adjust two parameters at the same time
        """
        temperature = self.preprocess_param(
            param=llm_kwargs.get('temperature', 0.95),
            default=0.95,
            min_val=0.01,
            max_val=0.99
        )
        """
        Another method of temperature sampling，Called nuclear sampling
        The value range is：(0.0, 1.0) Open interval，
        Cannot be equal to 0 or 1，Default Value is 0.7
        Model considering results with top_p probability quality tokens
        For example：0.1 means the model decoder only considers taking tokens from the top 10% probability candidates
        It is recommended to adjust the top_p or temperature parameters according to the application scenario，
        But do not adjust two parameters at the same time
        """
        top_p = self.preprocess_param(
            param=llm_kwargs.get('top_p', 0.70),
            default=0.70,
            min_val=0.01,
            max_val=0.99
        )
        response = self.zhipu_bro.chat.completions.create(
            model=self.model, messages=messages, stream=True,
            temperature=temperature,
            top_p=top_p,
            max_tokens=llm_kwargs.get('max_tokens', 1024 * 4),
        )
        return response

    def generate_chat(self, inputs:str, llm_kwargs:dict, history:list, system_prompt:str):
        self.model = llm_kwargs['llm_model']
        response = self.__conversation_message_payload(inputs, llm_kwargs, history, system_prompt)
        bro_results = ''
        for chunk in response:
            bro_results += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content, bro_results


if __name__ == '__main__':
    zhipu = ZhipuChatInit()
    zhipu.generate_chat('Hello', {'llm_model': 'glm-4'}, [], 'You are WPSAi')
