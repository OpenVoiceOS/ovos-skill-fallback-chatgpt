import openai as ai
from ovos_workshop.skills.fallback import FallbackSkill
from ovos_utils.process_utils import RuntimeRequirements
from ovos_utils import classproperty


class ChatGPTSkill(FallbackSkill):

    def __init__(self):
        super().__init__("ChatGPT")
        self._chat = None
        self.max_utts = 15  # memory size TODO from skill settings
        self.qa_pairs = []  # tuple of q+a
        self.current_q = None
        self.current_a = None

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(internet_before_load=True,
                                   network_before_load=True,
                                   gui_before_load=False,
                                   requires_internet=True,
                                   requires_network=True,
                                   requires_gui=False,
                                   no_internet_fallback=False,
                                   no_network_fallback=False,
                                   no_gui_fallback=True)

    def initialize(self):
        self.add_event("speak", self.handle_speak)
        self.add_event("recognizer_loop:utterance", self.handle_utterance)
        self.register_fallback(self.ask_chatgpt, 85)

    def handle_utterance(self, message):
        utt = message.data.get("utterances")[0]
        self.current_q = utt
        self.current_a = None
        # TODO: imperfect, subject to race conditions between bus messages
        # use session_id/ident to track all matches

    def handle_speak(self, message):
        utt = message.data.get("utterance")
        if not self.current_q:
            # TODO - use session_id/ident to track all matches
            # append to previous question if multi-speak answer
            return
        if utt and self.memory:
            self.qa_pairs.append((self.current_q, utt))
        self.current_q = None
        self.current_a = None

    @property
    def memory(self):
        return self.settings.get("memory", True)

    @property
    def initial_prompt(self):
        start_chat_log = """The assistant is helpful, creative, clever, and very friendly."""
        s = self.settings.get("initial_prompt", start_chat_log)
        return f"The following is a conversation with an AI assistant. {s}"

    @property
    def chatgpt(self):
        # this is a property to allow lazy init
        # the key may be set after skill is loaded
        key = self.settings.get("key")
        if not key:
            raise ValueError("OpenAI api key not set in skill settings.json")
        if not self._chat:
            ai.api_key = key
            self._chat = ai.Completion()
        return self._chat

    @property
    def chat_history(self):
        # TODO - intro question from skill settings
        intro_q = ("Hello, who are you?", "I am an AI created by OpenAI. How can I help you today?")
        if len(self.qa_pairs) > self.max_utts:
            qa = [intro_q] + self.qa_pairs[-1*self.max_utts:]
        else:
            qa = [intro_q] + self.qa_pairs
        chat = self.initial_prompt.strip() + "\n\n"
        if qa:
            qa = "\n".join([f"Human: {q}\nAI: {a}" for q, a in qa])
            if chat.endswith("\nHuman: "):
                chat = chat[-1*len("\nHuman: "):]
            if chat.endswith("\nAI: "):
                chat += f"Please rephrase the question\n"
            chat += qa
        return chat

    def get_prompt(self, utt):
        self.current_q = None
        self.current_a = None
        prompt = self.chat_history
        if not prompt.endswith("\nHuman: "):
            prompt += f"\nHuman: {utt}?\nAI: "
        else:
            prompt += f"{utt}?\nAI: "
        return prompt

    def ask_chatgpt(self, message):
        utterance = message.data['utterance']
        prompt = self.get_prompt(utterance)
        # TODO - params from skill settings
        response = self.chatgpt.create(prompt=prompt, engine="davinci", temperature=0.85,
                                       top_p=1, frequency_penalty=0,
                                       presence_penalty=0.7, best_of=2, max_tokens=100, stop="\nHuman: ")
        answer = response.choices[0].text.split("Human: ")[0].split("AI: ")[0].strip()
        if not answer or not answer.strip("?") or not answer.strip("_"):
            return False
        if self.memory:
            self.qa_pairs.append((utterance, answer))
        self.speak(answer)
        return True


def create_skill():
    return ChatGPTSkill()


if __name__ == "__main__":
    from ovos_utils.messagebus import FakeBus, Message

    s = ChatGPTSkill()
    s._startup(bus=FakeBus())
    msg = Message("intent_failure", {"utterance": "Explain quantum computing in simple terms"})
    s.ask_chatgpt(msg)
    print(s.qa_pairs[-1])
    msg = Message("intent_failure", {"utterance": "Got any creative ideas for a 10 year old’s birthday?"})
    s.ask_chatgpt(msg)
    print(s.qa_pairs[-1])
    msg = Message("intent_failure", {"utterance": "Do you think aliens exist?"})
    s.ask_chatgpt(msg)
    print(s.qa_pairs[-1])
    msg = Message("intent_failure", {"utterance": "When will the world end?"})
    s.ask_chatgpt(msg)
    print(s.qa_pairs[-1])
    print("##################################3")
    print(s.chat_history)
    # funny failure cases:
    #    ????
    #    Are you seriously asking that?
    #    I hardly understand quantum physics myself, but I found an article that you might find useful.
