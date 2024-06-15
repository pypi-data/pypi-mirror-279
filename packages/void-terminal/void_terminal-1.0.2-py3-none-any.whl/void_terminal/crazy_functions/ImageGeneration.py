from void_terminal.toolbox import CatchException, update_ui, get_conf, select_api_key, get_log_folder
from void_terminal.crazy_functions.multi_stage.multi_stage_utils import GptAcademicState


def gen_image(llm_kwargs, prompt, resolution="1024x1024", model="dall-e-2", quality=None, style=None):
    import requests, json, time, os
    from void_terminal.request_llms.bridge_all import model_info

    proxies = get_conf('proxies')
    # Set up OpenAI API key and model
    api_key = select_api_key(llm_kwargs['api_key'], llm_kwargs['llm_model'])
    chat_endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
    # 'https://api.openai.com/v1/chat/completions'
    img_endpoint = chat_endpoint.replace('chat/completions','images/generations')
    # # Generate the image
    url = img_endpoint
    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'n': 1,
        'size': resolution,
        'model': model,
        'response_format': 'url'
    }
    if quality is not None:
        data['quality'] = quality
    if style is not None:
        data['style'] = style
    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    print(response.content)
    try:
        image_url = json.loads(response.content.decode('utf8'))['data'][0]['url']
    except:
        raise RuntimeError(response.content.decode())
    # Save the file locally
    r = requests.get(image_url, proxies=proxies)
    file_path = f'{get_log_folder()}/image_gen/'
    os.makedirs(file_path, exist_ok=True)
    file_name = 'Image' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.png'
    with open(file_path+file_name, 'wb+') as f: f.write(r.content)


    return image_url, file_path+file_name


def edit_image(llm_kwargs, prompt, image_path, resolution="1024x1024", model="dall-e-2"):
    import requests, json, time, os
    from void_terminal.request_llms.bridge_all import model_info

    proxies = get_conf('proxies')
    api_key = select_api_key(llm_kwargs['api_key'], llm_kwargs['llm_model'])
    chat_endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
    # 'https://api.openai.com/v1/chat/completions'
    img_endpoint = chat_endpoint.replace('chat/completions','images/edits')
    # # Generate the image
    url = img_endpoint
    n = 1
    headers = {
        'Authorization': f"Bearer {api_key}",
    }
    make_transparent(image_path, image_path+'.tsp.png')
    make_square_image(image_path+'.tsp.png', image_path+'.tspsq.png')
    resize_image(image_path+'.tspsq.png', image_path+'.ready.png', max_size=1024)
    image_path = image_path+'.ready.png'
    with open(image_path, 'rb') as f:
        file_content = f.read()
        files = {
            'image': (os.path.basename(image_path), file_content),
            # 'mask': ('mask.png', open('mask.png', 'rb'))
            'prompt':   (None, prompt),
            "n":        (None, str(n)),
            'size':     (None, resolution),
        }

    response = requests.post(url, headers=headers, files=files, proxies=proxies)
    print(response.content)
    try:
        image_url = json.loads(response.content.decode('utf8'))['data'][0]['url']
    except:
        raise RuntimeError(response.content.decode())
    # Save the file locally
    r = requests.get(image_url, proxies=proxies)
    file_path = f'{get_log_folder()}/image_gen/'
    os.makedirs(file_path, exist_ok=True)
    file_name = 'Image' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.png'
    with open(file_path+file_name, 'wb+') as f: f.write(r.content)


    return image_url, file_path+file_name


@CatchException
def ImageGeneration_DALLE2(prompt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    """
    txt             Text entered by the user in the input field,For example, a paragraph that needs to be translated,For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters,Such as temperature and top_p,Generally pass it on as is
    plugin_kwargs   Plugin model parameters,No use for the time being
    chatbot         Chat display box handle,Displayed to the user
    history         Chat history,Context summary
    system_prompt   Silent reminder to GPT
    user_request    Current user`s request information（IP addresses, etc.）
    """
    history = []    # Clear history,To avoid input overflow
    if prompt.strip() == "":
        chatbot.append((prompt, "[Local Message] Image generation prompt is blank，Please enter image generation prompts in the `input area`。"))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the interface, interface update
        return
    chatbot.append(("You are calling the `Image Generation` plugin。", "[Local Message] Generate image, Please switch the model to gpt-* first。If the Chinese prompt is not effective, Try English Prompt。Processing ....."))
    yield from update_ui(chatbot=chatbot, history=history) # Refreshing the interface takes some time due to the request for gpt,Let`s do a UI update in time
    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    resolution = plugin_kwargs.get("advanced_arg", '1024x1024')
    image_url, image_path = gen_image(llm_kwargs, prompt, resolution)
    chatbot.append([prompt,
        f'Image transfer URL: <br/>`{image_url}`<br/>'+
        f'Transfer URL preview: <br/><div align="center"><img src="{image_url}"></div>'
        f'Local file address: <br/>`{image_path}`<br/>'+
        f'Local file preview: <br/><div align="center"><img src="file={image_path}"></div>'
    ])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the interface, interface update


@CatchException
def ImageGeneration_DALLE3(prompt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    history = []    # Clear history,To avoid input overflow
    if prompt.strip() == "":
        chatbot.append((prompt, "[Local Message] Image generation prompt is blank，Please enter image generation prompts in the `input area`。"))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the interface, interface update
        return
    chatbot.append(("You are calling the `Image Generation` plugin。", "[Local Message] Generate image, Please switch the model to gpt-* first。If the Chinese prompt is not effective, Try English Prompt。Processing ....."))
    yield from update_ui(chatbot=chatbot, history=history) # Refreshing the interface takes some time due to the request for gpt,Let`s do a UI update in time
    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    resolution_arg = plugin_kwargs.get("advanced_arg", '1024x1024-standard-vivid').lower()
    parts = resolution_arg.split('-')
    resolution = parts[0] # Resolution parsing
    quality = 'standard' # Quality and Style Defaults
    style = 'vivid'
    # Iterate to check for extra parameters
    for part in parts[1:]:
        if part in ['hd', 'standard']:
            quality = part
        elif part in ['vivid', 'natural']:
            style = part
    image_url, image_path = gen_image(llm_kwargs, prompt, resolution, model="dall-e-3", quality=quality, style=style)
    chatbot.append([prompt,
        f'Image transfer URL: <br/>`{image_url}`<br/>'+
        f'Transfer URL preview: <br/><div align="center"><img src="{image_url}"></div>'
        f'Local file address: <br/>`{image_path}`<br/>'+
        f'Local file preview: <br/><div align="center"><img src="file={image_path}"></div>'
    ])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the interface, interface update


class ImageEditState(GptAcademicState):
    # Not yet completed
    def get_image_file(self, x):
        import os, glob
        if len(x) == 0:             return False, None
        if not os.path.exists(x):   return False, None
        if x.endswith('.png'):      return True, x
        file_manifest = [f for f in glob.glob(f'{x}/**/*.png', recursive=True)]
        confirm = (len(file_manifest) >= 1 and file_manifest[0].endswith('.png') and os.path.exists(file_manifest[0]))
        file = None if not confirm else file_manifest[0]
        return confirm, file

    def lock_plugin(self, chatbot):
        chatbot._cookies['lock_plugin'] = 'crazy_functions.ImageGeneration->ImageModification_DALLE2'
        self.dump_state(chatbot)

    def unlock_plugin(self, chatbot):
        self.reset()
        chatbot._cookies['lock_plugin'] = None
        self.dump_state(chatbot)

    def get_resolution(self, x):
        return (x in ['256x256', '512x512', '1024x1024']), x

    def get_prompt(self, x):
        confirm = (len(x)>=5) and (not self.get_resolution(x)[0]) and (not self.get_image_file(x)[0])
        return confirm, x

    def reset(self):
        self.req = [
            {'value':None, 'description': 'Please upload the image first（Must be in .png format）, Then click this plugin again',                      'verify_fn': self.get_image_file},
            {'value':None, 'description': 'Please enter the resolution,Optional：256x256, 512x512 or 1024x1024, Then click this plugin again',   'verify_fn': self.get_resolution},
            {'value':None, 'description': 'Please enter modification requirements,It is recommended to use English prompts, Then click this plugin again',                 'verify_fn': self.get_prompt},
        ]
        self.info = ""

    def feed(self, prompt, chatbot):
        for r in self.req:
            if r['value'] is None:
                confirm, res = r['verify_fn'](prompt)
                if confirm:
                    r['value'] = res
                    self.dump_state(chatbot)
                    break
        return self

    def next_req(self):
        for r in self.req:
            if r['value'] is None:
                return r['description']
        return "All information has been collected"

    def already_obtained_all_materials(self):
        return all([x['value'] is not None for x in self.req])

@CatchException
def ImageModification_DALLE2(prompt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    # Not yet completed
    history = []    # Clear history
    state = ImageEditState.get_state(chatbot, ImageEditState)
    state = state.feed(prompt, chatbot)
    state.lock_plugin(chatbot)
    if not state.already_obtained_all_materials():
        chatbot.append(["Image modification\n\nTranslatedText（Erase the areas in the image that need to be modified with an eraser to pure white，That is, RGB=255,255,255）\n2. Enter resolution \n3. Enter modification requirements", state.next_req()])
        yield from update_ui(chatbot=chatbot, history=history)
        return

    image_path = state.req[0]['value']
    resolution = state.req[1]['value']
    prompt = state.req[2]['value']
    chatbot.append(["Image modification, Executing", f"Image:`{image_path}`<br/>Resolution:`{resolution}`<br/>Modify requirements:`{prompt}`"])
    yield from update_ui(chatbot=chatbot, history=history)
    image_url, image_path = edit_image(llm_kwargs, prompt, image_path, resolution)
    chatbot.append([prompt,
        f'Image transfer URL: <br/>`{image_url}`<br/>'+
        f'Transfer URL preview: <br/><div align="center"><img src="{image_url}"></div>'
        f'Local file address: <br/>`{image_path}`<br/>'+
        f'Local file preview: <br/><div align="center"><img src="file={image_path}"></div>'
    ])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the interface, interface update
    state.unlock_plugin(chatbot)

def make_transparent(input_image_path, output_image_path):
    from PIL import Image
    image = Image.open(input_image_path)
    image = image.convert("RGBA")
    data = image.getdata()
    new_data = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    image.putdata(new_data)
    image.save(output_image_path, "PNG")

def resize_image(input_path, output_path, max_size=1024):
    from PIL import Image
    with Image.open(input_path) as img:
        width, height = img.size
        if width > max_size or height > max_size:
            if width >= height:
                new_width = max_size
                new_height = int((max_size / width) * height)
            else:
                new_height = max_size
                new_width = int((max_size / height) * width)

            resized_img = img.resize(size=(new_width, new_height))
            resized_img.save(output_path)
        else:
            img.save(output_path)

def make_square_image(input_path, output_path):
    from PIL import Image
    with Image.open(input_path) as img:
        width, height = img.size
        size = max(width, height)
        new_img = Image.new("RGBA", (size, size), color="black")
        new_img.paste(img, ((size - width) // 2, (size - height) // 2))
        new_img.save(output_path)
