import json
import time
import logging
import traceback
import requests

# Put your own secrets such as API and proxy address in config_private.py
# When reading, first check if there is a private config_private configuration file（Not controlled by git），If there is，Then overwrite the original config file
from void_terminal.toolbox import (
    get_conf,
    update_ui,
    is_the_upload_folder,
)

proxies, TIMEOUT_SECONDS, MAX_RETRY = get_conf(
    "proxies", "TIMEOUT_SECONDS", "MAX_RETRY"
)

timeout_bot_msg = (
    "[Local Message] Request timeout. Network error. Please check proxy settings in config.py."
    + "Network error，Check if the proxy server is available，And if the format of the proxy settings is correct，The format must be[Protocol]://[Address]:[Port]，All parts are necessary。"
)


def get_full_error(chunk, stream_response):
    """
    Attempt to get the complete error message
    """
    while True:
        try:
            chunk += next(stream_response)
        except:
            break
    return chunk


def decode_chunk(chunk):
    """
    Used for解读"content"and"finish_reason"的内容
    """
    chunk = chunk.decode()
    respose = ""
    finish_reason = "False"
    try:
        chunk = json.loads(chunk[6:])
    except:
        finish_reason = "JSON_ERROR"
    # Error handling section
    if "error" in chunk:
        respose = "API_ERROR"
        try:
            chunk = json.loads(chunk)
            finish_reason = chunk["error"]["code"]
        except:
            finish_reason = "API_ERROR"
        return respose, finish_reason

    try:
        respose = chunk["choices"][0]["delta"]["content"]
    except:
        pass
    try:
        finish_reason = chunk["choices"][0]["finish_reason"]
    except:
        pass
    return respose, finish_reason


def generate_message(input, model, key, history, max_output_token, system_prompt, temperature):
    """
    Integrate all information，Select LLM model，Generate http request，Prepare to send request
    """
    api_key = f"Bearer {key}"

    headers = {"Content-Type": "application/json", "Authorization": api_key}

    conversation_cnt = len(history) // 2

    messages = [{"role": "system", "content": system_prompt}]
    if conversation_cnt:
        for index in range(0, 2 * conversation_cnt, 2):
            what_i_have_asked = {}
            what_i_have_asked["role"] = "user"
            what_i_have_asked["content"] = history[index]
            what_gpt_answer = {}
            what_gpt_answer["role"] = "assistant"
            what_gpt_answer["content"] = history[index + 1]
            if what_i_have_asked["content"] != "":
                if what_gpt_answer["content"] == "":
                    continue
                if what_gpt_answer["content"] == timeout_bot_msg:
                    continue
                messages.append(what_i_have_asked)
                messages.append(what_gpt_answer)
            else:
                messages[-1]["content"] = what_gpt_answer["content"]
    what_i_ask_now = {}
    what_i_ask_now["role"] = "user"
    what_i_ask_now["content"] = input
    messages.append(what_i_ask_now)
    playload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": True,
        "max_tokens": max_output_token,
    }
    try:
        print(f" {model} : {conversation_cnt} : {input[:100]} ..........")
    except:
        print("There may be garbled characters in the input。")
    return headers, playload


def get_predict_function(
        api_key_conf_name,
        max_output_token,
        disable_proxy = False
    ):
    """
    Generate response function for OpenAI format API，Among the incoming parameters：
    api_key_conf_name：
        `config.py`The name of the APIKEY for this model，For example"YIMODEL_API_KEY"
    max_output_token：
        Maximum token count for each request，For example, for 010,000 items yi-34b-chat-200k，Its maximum request number is 4096
        ⚠️ Do not confuse with the maximum token number of the model。
    disable_proxy：
        Whether to use a proxy，True means not in use，False for use。
    """

    APIKEY = get_conf(api_key_conf_name)

    def predict_no_ui_long_connection(
        inputs,
        llm_kwargs,
        history=[],
        sys_prompt="",
        observe_window=None,
        console_slience=False,
    ):
        """
        Send to chatGPT，Waiting for reply，Completed in one go，Do not display intermediate processes。But internally use the stream method to avoid the network being cut off midway。
        inputs：
            This is the input of this inquiry
        sys_prompt:
            System silent prompt
        llm_kwargs：
            Internal tuning parameters of chatGPT
        history：
            history is the list of previous conversations
        observe_window = None：
            Used to transfer the already output part across threads，Most of the time it`s just for fancy visual effects，Leave it blank。observe_window[0]：Observation window。observe_window[1]：Watchdog
        """
        watch_dog_patience = 5  # The patience of the watchdog，Disallow biting for 5 seconds(Not biting humans either
        if len(APIKEY) == 0:
            raise RuntimeError(f"APIKEY is empty,Please check the configuration file{APIKEY}")
        if inputs == "":
            inputs = "Hello👋"
        headers, playload = generate_message(
            input=inputs,
            model=llm_kwargs["llm_model"],
            key=APIKEY,
            history=history,
            max_output_token=max_output_token,
            system_prompt=sys_prompt,
            temperature=llm_kwargs["temperature"],
        )
        retry = 0
        while True:
            try:
                from void_terminal.request_llms.bridge_all import model_info

                endpoint = model_info[llm_kwargs["llm_model"]]["endpoint"]
                if not disable_proxy:
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        proxies=proxies,
                        json=playload,
                        stream=True,
                        timeout=TIMEOUT_SECONDS,
                    )
                else:
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        json=playload,
                        stream=True,
                        timeout=TIMEOUT_SECONDS,
                    )
                break
            except:
                retry += 1
                traceback.print_exc()
                if retry > MAX_RETRY:
                    raise TimeoutError
                if MAX_RETRY != 0:
                    print(f"Request timed out，Retrying ({retry}/{MAX_RETRY}) ……")

        stream_response = response.iter_lines()
        result = ""
        while True:
            try:
                chunk = next(stream_response)
            except StopIteration:
                break
            except requests.exceptions.ConnectionError:
                chunk = next(stream_response)  # Failed，Retry once？If it fails again, there is no way。
            response_text, finish_reason = decode_chunk(chunk)
            # The returned data stream is empty for the first time，Continue waiting
            if response_text == "" and finish_reason != "False":
                continue
            if response_text == "API_ERROR" and (
                finish_reason != "False" or finish_reason != "stop"
            ):
                chunk = get_full_error(chunk, stream_response)
                chunk_decoded = chunk.decode()
                print(chunk_decoded)
                raise RuntimeError(
                    f"API exception,Please check the terminal output。Possible reasons are:{finish_reason}"
                )
            if chunk:
                try:
                    if finish_reason == "stop":
                        logging.info(f"[response] {result}")
                        break
                    result += response_text
                    if not console_slience:
                        print(response_text, end="")
                    if observe_window is not None:
                        # Observation window，Display the data already obtained
                        if len(observe_window) >= 1:
                            observe_window[0] += response_text
                        # Watchdog，If the dog is not fed beyond the deadline，then terminate
                        if len(observe_window) >= 2:
                            if (time.time() - observe_window[1]) > watch_dog_patience:
                                raise RuntimeError("User canceled the program。")
                except Exception as e:
                    chunk = get_full_error(chunk, stream_response)
                    chunk_decoded = chunk.decode()
                    error_msg = chunk_decoded
                    print(error_msg)
                    raise RuntimeError("Json parsing is not normal")
        return result

    def predict(
        inputs,
        llm_kwargs,
        plugin_kwargs,
        chatbot,
        history=[],
        system_prompt="",
        stream=True,
        additional_fn=None,
    ):
        """
        Send to chatGPT，Get output in a streaming way。
        Used for basic conversation functions。
        inputs are the inputs for this inquiry
        top_p, Temperature is an internal tuning parameter of chatGPT
        history is the list of previous conversations（Note that both inputs and history，An error of token overflow will be triggered if the content is too long）
        chatbot is the conversation list displayed in WebUI，Modify it，Then yield it out，You can directly modify the conversation interface content
        additional_fn represents which button is clicked，See functional.py for buttons
        """
        if len(APIKEY) == 0:
            raise RuntimeError(f"APIKEY is empty,Please check the configuration file{APIKEY}")
        if inputs == "":
            inputs = "Hello👋"
        if additional_fn is not None:
            from void_terminal.core_functional import handle_core_functionality

            inputs, history = handle_core_functionality(
                additional_fn, inputs, history, chatbot
            )
        logging.info(f"[raw_input] {inputs}")
        chatbot.append((inputs, ""))
        yield from update_ui(
            chatbot=chatbot, history=history, msg="Waiting for response"
        )  # Refresh the page

        # check mis-behavior
        if is_the_upload_folder(inputs):
            chatbot[-1] = (
                inputs,
                f"[Local Message] Operation error detected! After you upload the document，Click the `**Function Plugin Area**` button for processing，Do not click the `Submit` button or the `Basic Function Area` button。",
            )
            yield from update_ui(
                chatbot=chatbot, history=history, msg="Normal"
            )  # Refresh the page
            time.sleep(2)

        headers, playload = generate_message(
            input=inputs,
            model=llm_kwargs["llm_model"],
            key=APIKEY,
            history=history,
            max_output_token=max_output_token,
            system_prompt=system_prompt,
            temperature=llm_kwargs["temperature"],
        )

        history.append(inputs)
        history.append("")
        retry = 0
        while True:
            try:
                from void_terminal.request_llms.bridge_all import model_info

                endpoint = model_info[llm_kwargs["llm_model"]]["endpoint"]
                if not disable_proxy:
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        proxies=proxies,
                        json=playload,
                        stream=True,
                        timeout=TIMEOUT_SECONDS,
                    )
                else:
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        json=playload,
                        stream=True,
                        timeout=TIMEOUT_SECONDS,
                    )
                break
            except:
                retry += 1
                chatbot[-1] = (chatbot[-1][0], timeout_bot_msg)
                retry_msg = (
                    f"，Retrying ({retry}/{MAX_RETRY}) ……" if MAX_RETRY > 0 else ""
                )
                yield from update_ui(
                    chatbot=chatbot, history=history, msg="Request timed out" + retry_msg
                )  # Refresh the page
                if retry > MAX_RETRY:
                    raise TimeoutError

        gpt_replying_buffer = ""

        stream_response = response.iter_lines()
        while True:
            try:
                chunk = next(stream_response)
            except StopIteration:
                break
            except requests.exceptions.ConnectionError:
                chunk = next(stream_response)  # Failed，Retry once？If it fails again, there is no way。
            response_text, finish_reason = decode_chunk(chunk)
            # The returned data stream is empty for the first time，Continue waiting
            if response_text == "" and finish_reason != "False":
                continue
            if chunk:
                try:
                    if response_text == "API_ERROR" and (
                        finish_reason != "False" or finish_reason != "stop"
                    ):
                        chunk = get_full_error(chunk, stream_response)
                        chunk_decoded = chunk.decode()
                        chatbot[-1] = (
                            chatbot[-1][0],
                            "[Local Message] {finish_reason},Get the following error message：\n"
                            + chunk_decoded,
                        )
                        yield from update_ui(
                            chatbot=chatbot,
                            history=history,
                            msg="API exception:" + chunk_decoded,
                        )  # Refresh the page
                        print(chunk_decoded)
                        return

                    if finish_reason == "stop":
                        logging.info(f"[response] {gpt_replying_buffer}")
                        break
                    status_text = f"finish_reason: {finish_reason}"
                    gpt_replying_buffer += response_text
                    # If an exception is thrown here，It is usually because the text is too long，See the output of get_full_error for details
                    history[-1] = gpt_replying_buffer
                    chatbot[-1] = (history[-2], history[-1])
                    yield from update_ui(
                        chatbot=chatbot, history=history, msg=status_text
                    )  # Refresh the page
                except Exception as e:
                    yield from update_ui(
                        chatbot=chatbot, history=history, msg="Json parsing is not normal"
                    )  # Refresh the page
                    chunk = get_full_error(chunk, stream_response)
                    chunk_decoded = chunk.decode()
                    chatbot[-1] = (
                        chatbot[-1][0],
                        "[Local Message] Parsing error,Get the following error message：\n" + chunk_decoded,
                    )
                    yield from update_ui(
                        chatbot=chatbot, history=history, msg="Json exception" + chunk_decoded
                    )  # Refresh the page
                    print(chunk_decoded)
                    return

    return predict_no_ui_long_connection, predict
