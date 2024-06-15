import os
import fake_gradio as gr
from void_terminal.toolbox import get_conf, ProxyNetworkActivate

CODE_HIGHLIGHT, ADD_WAIFU, LAYOUT = get_conf("CODE_HIGHLIGHT", "ADD_WAIFU", "LAYOUT")
theme_dir = os.path.dirname(__file__)


def dynamic_set_theme(THEME):
    set_theme = gr.themes.ThemeClass()
    with ProxyNetworkActivate("Download_Gradio_Theme"):
        print("Downloading Gradio themes，Please wait。")
        try:
            if THEME.startswith("Huggingface-"):
                THEME = THEME.lstrip("Huggingface-")
            if THEME.startswith("huggingface-"):
                THEME = THEME.lstrip("huggingface-")
            set_theme = set_theme.from_hub(THEME.lower())
        except:
            print("An exception occurred when downloading the Gradio theme。")
    return set_theme


def adjust_theme():
    try:
        set_theme = gr.themes.ThemeClass()
        with ProxyNetworkActivate("Download_Gradio_Theme"):
            print("Downloading Gradio themes，Please wait。")
            try:
                THEME = get_conf("THEME")
                if THEME.startswith("Huggingface-"):
                    THEME = THEME.lstrip("Huggingface-")
                if THEME.startswith("huggingface-"):
                    THEME = THEME.lstrip("huggingface-")
                set_theme = set_theme.from_hub(THEME.lower())
            except:
                print("An exception occurred when downloading the Gradio theme。")

        from void_terminal.themes.common import get_common_html_javascript_code
        js = get_common_html_javascript_code()
        
        if not hasattr(gr, "RawTemplateResponse"):
            gr.RawTemplateResponse = gr.routes.templates.TemplateResponse
        gradio_original_template_fn = gr.RawTemplateResponse

        def gradio_new_template_fn(*args, **kwargs):
            res = gradio_original_template_fn(*args, **kwargs)
            res.body = res.body.replace(b"</html>", f"{js}</html>".encode("utf8"))
            res.init_headers()
            return res

        gr.routes.templates.TemplateResponse = (
            gradio_new_template_fn  # override gradio template
        )
    except Exception:
        set_theme = None
        print("Gradio version is outdated, Cannot customize font and color。")
    return set_theme


with open(os.path.join(theme_dir, "common.css"), "r", encoding="utf-8") as f:
    advanced_css = f.read()
