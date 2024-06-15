prompts_hs = """ Please start with `{headstart}`，Write the first act of a novel。

- As Concise as Possible，Do not include too many plots，Because you will interact with the user to continue writing the plot below，Leave enough interaction space。
- When characters appear，Provide the Names of Characters。
- Actively use techniques such as environmental and character descriptions，Let Readers Feel Your Story World。
- Actively use rhetorical devices，For example, similes, personification, parallelism, antithesis, hyperbole, etc.。
- Word count requirement：The first act has fewer than 300 characters，And less than 2 paragraphs。
"""

prompts_interact = """ Review of the previous text of the novel：
「
{previously_on_story}
」

You are a writer，Based on the above plot，Provide 4 different directions for subsequent plot development，Each development direction is concisely described in one sentence。Later，I will choose from these 4 options，Choose a plot development。

Example of Output Format：
1. Subsequent Plot Development 1
2. Subsequent plot development 2
3. Subsequent Plot Development
4. Plot development
"""


prompts_resume = """Review of the previous text of the novel：
「
{previously_on_story}
」

You are a writer，We are discussing with each other，Determine the development of the subsequent plot。
In the following plot development，
「
{choice}
」
I Think a More Reasonable Approach Is：{user_choice}。
Please Based on the Previous Text（Do not repeat the previous text），Around the plot I have chosen，Write the next scene of the novel。

- Prohibit making up plots that do not match my choice。
- As Concise as Possible，Do not include too many plots，Because you will interact with the user to continue writing the plot below，Leave enough interaction space。
- Do not repeat the previous text。
- When characters appear，Provide the Names of Characters。
- Actively use techniques such as environmental and character descriptions，Let Readers Feel Your Story World。
- Actively use rhetorical devices，For example, similes, personification, parallelism, antithesis, hyperbole, etc.。
- The next scene of the novel has fewer than 300 words，And less than 2 paragraphs。
"""


prompts_terminate = """Review of the previous text of the novel：
「
{previously_on_story}
」

You are a writer，We are discussing with each other，Determine the development of the subsequent plot。
Now，The story should end，I think the most reasonable ending for the story is：{user_choice}。

Please Based on the Previous Text（Do not repeat the previous text），Write the last scene of the novel。

- Do not repeat the previous text。
- When characters appear，Provide the Names of Characters。
- Actively use techniques such as environmental and character descriptions，Let Readers Feel Your Story World。
- Actively use rhetorical devices，For example, similes, personification, parallelism, antithesis, hyperbole, etc.。
- Word count requirement：The last scene has fewer than 1000 words。
"""


from void_terminal.toolbox import CatchException, update_ui, update_ui_lastest_msg
from void_terminal.crazy_functions.multi_stage.multi_stage_utils import GptAcademicGameBaseState
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.request_llms.bridge_all import predict_no_ui_long_connection
from void_terminal.crazy_functions.game_fns.game_utils import get_code_block, is_same_thing
import random


class MiniGame_ResumeStory(GptAcademicGameBaseState):
    story_headstart = [
        'The pioneer knows，He is now the only person in the entire universe。',
        'Late at night，A young person walks through Tiananmen Square towards the Memorial Hall。In the Chronicle of the 22nd Century，The computer named his code M102。',
        'He Knows，The last lesson will be taught ahead of schedule。Another wave of severe pain strikes from the liver，Almost made him faint。',
        'At a distance of fifty thousand light-years from Earth，At the center of the Milky Way，An interstellar war that has lasted for 20,000 years is drawing to a close。A square area gradually appears in the space there，As if the brilliant background of stars has been cut out into a square。',
        'Yi Yi and three others set sail on a yacht to recite poetry in the South Pacific，Their destination is Antarctica，If we can smoothly arrive there in a few days，They will emerge from the crust to see the poetry cloud。',
        'Many People Are Born with an Unexplained Attraction to Something，As if his birth was meant to date this thing，That`s exactly right，Yuan Yuan is fascinated by soap bubbles。'
    ]


    def begin_game_step_0(self, prompt, chatbot, history):
        # init game at step 0
        self.headstart = random.choice(self.story_headstart)
        self.story = []
        chatbot.append(["Interactive Story Writing", f"The beginning of this story is：{self.headstart}"])
        self.sys_prompt_ = 'You are a brilliant writer with a rich imagination。Interacting with your friends，Write a story together，Therefore, Each Story Paragraph You Write Should Be Less Than 300 Words（Excluding the ending）。'


    def generate_story_image(self, story_paragraph):
        try:
            from void_terminal.crazy_functions.ImageGeneration import gen_image
            prompt_ = predict_no_ui_long_connection(inputs=story_paragraph, llm_kwargs=self.llm_kwargs, history=[], sys_prompt='You need to based on the novel paragraph given by the user，Conduct a Brief Environmental Description。Requirement：Within 80 characters。')
            image_url, image_path = gen_image(self.llm_kwargs, prompt_, '512x512', model="dall-e-2", quality='standard', style='natural')
            return f'<br/><div align="center"><img src="file={image_path}"></div>'
        except:
            return ''

    def step(self, prompt, chatbot, history):

        """
        First，Handle special cases like game initialization
        """
        if self.step_cnt == 0:
            self.begin_game_step_0(prompt, chatbot, history)
            self.lock_plugin(chatbot)
            self.cur_task = 'head_start'
        else:
            if prompt.strip() == 'exit' or prompt.strip() == 'End of the plot':
                # should we terminate game here?
                self.delete_game = True
                yield from update_ui_lastest_msg(lastmsg=f"Game over。", chatbot=chatbot, history=history, delay=0.)
                return
            if 'Plot Conclusion' in prompt:
                self.cur_task = 'story_terminate'
            # # well, game resumes
            # chatbot.append([prompt, ""])
        # update ui, don't keep the user waiting
        yield from update_ui(chatbot=chatbot, history=history)


        """
        Handle the main logic of the game
        """
        if self.cur_task == 'head_start':
            """
            This is the first step of the game
            """
            inputs_ = prompts_hs.format(headstart=self.headstart)
            history_ = []
            story_paragraph = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs_, 'Beginning of the story', self.llm_kwargs,
                chatbot, history_, self.sys_prompt_
            )
            self.story.append(story_paragraph)
            # # Illustration
            yield from update_ui_lastest_msg(lastmsg=story_paragraph + '<br/>Generating Illustration ...', chatbot=chatbot, history=history, delay=0.)
            yield from update_ui_lastest_msg(lastmsg=story_paragraph + '<br/>'+ self.generate_story_image(story_paragraph), chatbot=chatbot, history=history, delay=0.)

            # # Building subsequent plot guidance
            previously_on_story = ""
            for s in self.story:
                previously_on_story += s + '\n'
            inputs_ = prompts_interact.format(previously_on_story=previously_on_story)
            history_ = []
            self.next_choices = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs_, 'Please choose from the following story directions，Choose one（Certainly，You Can Also Choose to Provide Alternative Storylines）：', self.llm_kwargs,
                chatbot,
                history_,
                self.sys_prompt_
            )
            self.cur_task = 'user_choice'


        elif self.cur_task == 'user_choice':
            """
            According to the user`s prompt，Determine the next step of the story
            """
            if 'Please choose from the following story directions，Choose one' in chatbot[-1][0]: chatbot.pop(-1)
            previously_on_story = ""
            for s in self.story:
                previously_on_story += s + '\n'
            inputs_ = prompts_resume.format(previously_on_story=previously_on_story, choice=self.next_choices, user_choice=prompt)
            history_ = []
            story_paragraph = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs_, f'Next part of the story（Your choice is：{prompt}）。', self.llm_kwargs,
                chatbot, history_, self.sys_prompt_
            )
            self.story.append(story_paragraph)
            # # Illustration
            yield from update_ui_lastest_msg(lastmsg=story_paragraph + '<br/>Generating Illustration ...', chatbot=chatbot, history=history, delay=0.)
            yield from update_ui_lastest_msg(lastmsg=story_paragraph + '<br/>'+ self.generate_story_image(story_paragraph), chatbot=chatbot, history=history, delay=0.)

            # # Building subsequent plot guidance
            previously_on_story = ""
            for s in self.story:
                previously_on_story += s + '\n'
            inputs_ = prompts_interact.format(previously_on_story=previously_on_story)
            history_ = []
            self.next_choices = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs_,
                'Please choose from the following story directions，Choose one。Certainly，You can also provide other story directions in your mind。Additionally，If You Want the Plot to End Immediately，Please enter the plot direction，And use the four characters `Plot Conclusion` as a prompt for the program。', self.llm_kwargs,
                chatbot,
                history_,
                self.sys_prompt_
            )
            self.cur_task = 'user_choice'


        elif self.cur_task == 'story_terminate':
            """
            According to the user`s prompt，Determine the ending of the story
            """
            previously_on_story = ""
            for s in self.story:
                previously_on_story += s + '\n'
            inputs_ = prompts_terminate.format(previously_on_story=previously_on_story, user_choice=prompt)
            history_ = []
            story_paragraph = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs_, f'Story ending（Your choice is：{prompt}）。', self.llm_kwargs,
                chatbot, history_, self.sys_prompt_
            )
            # # Illustration
            yield from update_ui_lastest_msg(lastmsg=story_paragraph + '<br/>Generating Illustration ...', chatbot=chatbot, history=history, delay=0.)
            yield from update_ui_lastest_msg(lastmsg=story_paragraph + '<br/>'+ self.generate_story_image(story_paragraph), chatbot=chatbot, history=history, delay=0.)

            # terminate game
            self.delete_game = True
            return
