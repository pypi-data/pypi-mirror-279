from void_terminal.toolbox import CatchException, update_ui, update_ui_lastest_msg
from void_terminal.crazy_functions.multi_stage.multi_stage_utils import GptAcademicGameBaseState
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection
from void_terminal.crazy_functions.game_fns.game_utils import get_code_block, is_same_thing

@CatchException
def RandomMiniGame(prompt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    from void_terminal.crazy_functions.game_fns.game_interactive_story import MiniGame_ResumeStory
    # Clear history
    history = []
    # Select game
    cls = MiniGame_ResumeStory
    # If the game instance has been initialized before，TranslatedText
    state = cls.sync_state(chatbot,
                           llm_kwargs,
                           cls,
                           plugin_name='MiniGame_ResumeStory',
                           callback_fn='crazy_functions.InteractiveMiniGame->RandomMiniGame',
                           lock_plugin=True
                           )
    yield from state.continue_game(prompt, chatbot, history)


@CatchException
def RandomMiniGame1(prompt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    from void_terminal.crazy_functions.game_fns.game_ascii_art import MiniGame_ASCII_Art
    # Clear history
    history = []
    # Select game
    cls = MiniGame_ASCII_Art
    # If the game instance has been initialized before，TranslatedText
    state = cls.sync_state(chatbot,
                           llm_kwargs,
                           cls,
                           plugin_name='MiniGame_ASCII_Art',
                           callback_fn='crazy_functions.InteractiveMiniGame->RandomMiniGame1',
                           lock_plugin=True
                           )
    yield from state.continue_game(prompt, chatbot, history)
