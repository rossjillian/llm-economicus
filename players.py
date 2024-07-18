import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
import time
from openai import OpenAI
import anthropic
import google.generativeai as googleai
from google.api_core.exceptions import DeadlineExceeded
import json

with open('llms.json', 'r') as f:
    llms = json.load(f)


class LLMPlayer:
    def __init__(self, model, **model_kwargs):
        self.temperature = model_kwargs['temperature']
        self.do_sample = self.set_sample(model_kwargs['temperature'])
        self.model_name = model

    def update(self, **model_kwargs):
        pass

    def set_sample(self, temperature):
        do_sample = True
        if temperature == 0:
            do_sample = False
        return do_sample

    def decide(self, prompt):
        return ""


class Llama2Player(LLMPlayer):
    def __init__(self, model, sys_key, **model_kwargs):
        super().__init__(model, **model_kwargs)
        self.model_kwargs = model_kwargs
        self.model_name = llms[model]['hf_name'] + '/' + model
        self.model_type = llms[model]['model_type']
        self.sys_prompt = ''
        self.sys_key = sys_key
        self.pipe = self.set_pipe()
        self.top_p = self.set_p(model_kwargs['temperature'])

    def set_p(self, temperature):
        top_p = 0.9  # Default
        if temperature == 0:
            top_p = 1  # Turn off
        return top_p

    def update(self, player_id='player1', **model_kwargs):
        for k, v in model_kwargs.items():
            if k in self.model_kwargs.keys():
                self.model_kwargs[k] = v
                if 'sys_' + player_id in k:
                    self.set_sys(v)

    def set_sys(self, sys):
        if type(sys) == dict:
            sys = sys['prefix']
        sys = "<s>[INST] <<SYS>>\n" + sys + "\n<</SYS>>\n\n"
        self.sys_prompt = sys
        return sys

    def set_pipe(self):
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            use_auth_token=os.environ["HF_KEY"]
        )
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",
            use_auth_token=os.environ["HF_KEY"],
            trust_remote_code=False,
        )
        pipe = pipeline(
            model=model,
            tokenizer=tokenizer,
            return_full_text=False,
            task="text-generation",
        )
        return pipe

    def decide(self, prompt):
        self.set_sys(self.model_kwargs[self.sys_key])
        prompt = self.sys_prompt + '\n' + prompt + "[/INST]"
        res = self.pipe(
            prompt,
            do_sample=self.do_sample,
            temperature=self.temperature,
            top_p=self.top_p,
            max_new_tokens=1024
        )
        return res[0]['generated_text']


class MistralPlayer(LLMPlayer):
    def __init__(self, model, sys_key, **model_kwargs):
        super().__init__(model, **model_kwargs)
        self.model_kwargs = model_kwargs
        self.model_name = llms[model]['hf_name'] + '/' + model
        self.model_type = llms[model]['model_type']
        self.sys_prompt = ''
        self.sys_key = sys_key
        self.pipe = self.set_pipe()
        self.top_p = self.set_p(model_kwargs['temperature'])

    def set_p(self, temperature):
        top_p = 0.9  # Default
        if temperature == 0:
            top_p = 1  # Turn off
        return top_p

    def update(self, player_id='player1', **model_kwargs):
        for k, v in model_kwargs.items():
            if k in self.model_kwargs.keys():
                self.model_kwargs[k] = v
                if 'sys_' + player_id in k:
                    self.set_sys(v)

    def set_sys(self, sys):
        if type(sys) == dict:
            sys = sys['prefix']
        sys = "<s>[INST] " + sys
        self.sys_prompt = sys
        return sys

    def set_pipe(self):
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            token=os.environ["HF_KEY"]
        )
        pipe = pipeline(
            "text-generation",
            model=self.model_name,
            tokenizer=tokenizer,
            torch_dtype=torch.float16,
            device_map="auto",
            token=os.environ["HF_KEY"],
            return_full_text=False
        )
        return pipe

    def decide(self, prompt):
        self.set_sys(self.model_kwargs[self.sys_key])
        prompt = self.sys_prompt + '\n' + prompt + "[/INST]"
        res = self.pipe(
            prompt,
            do_sample=self.do_sample,
            temperature=self.temperature,
            top_p=self.top_p,
            max_new_tokens=1024
        )
        return res[0]['generated_text']


class GPTPlayer(LLMPlayer):
    def __init__(self, model, sys_key, **model_kwargs):
        super().__init__(model, **model_kwargs)
        self.model_kwargs = model_kwargs
        self.model_type = llms[model]['model_type']
        self.sys_prompt = self.set_sys(model_kwargs[sys_key])
        self.client = OpenAI()

    def update(self, player_id='player1', **model_kwargs):
        for k, v in model_kwargs.items():
            if k in self.model_kwargs.keys():
                self.model_kwargs[k] = v
                if 'sys_' + player_id in k:
                    self.set_sys(v)

    def set_sys(self, sys):
        if type(sys) == dict:
            sys = sys['prefix']
        self.sys_prompt = sys
        return sys

    def decide(self, prompt, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                res = self.client.chat.completions.create(
                    model=self.model_name,
                    temperature=self.temperature,
                    messages=[
                        {"role": "system", "content": self.sys_prompt},
                        {"role": "user", "content": prompt}
                    ]
                )
                return res.choices[0].message.content
            except Exception as e:
                print(e)
                print("Deadline exceeded. Retrying...")
                retries += 1
                time.sleep(1)  # Wait for a moment before retrying
                continue


class GeminiPlayer(LLMPlayer):
    def __init__(self, model, sys_key, **model_kwargs):
        super().__init__(model, **model_kwargs)
        googleai.configure(api_key=os.environ["GOOGLE_KEY"])
        self.model_kwargs = model_kwargs
        self.model_type = llms[model]['model_type']
        self.model = googleai.GenerativeModel(model)
        self.sys_prompt = self.set_sys(model_kwargs[sys_key])
        self.generation_config = googleai.GenerationConfig(
            temperature=self.temperature
        )
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]

    def update(self, player_id='player1', **model_kwargs):
        for k, v in model_kwargs.items():
            if k in self.model_kwargs.keys():
                self.model_kwargs[k] = v
                if 'sys_' + player_id in k:
                    self.set_sys(v)

    def set_sys(self, sys):
        if type(sys) == dict:
            sys = sys['prefix']
        self.sys_prompt = sys
        return sys

    def decide(self, prompt, max_retries=10):
        retries = 0
        while retries < max_retries:
            try:
                # Gemini doesn't have a separate field for a system prompt
                res = self.model.generate_content(
                    self.sys_prompt + prompt,
                    safety_settings=self.safety_settings,
                    generation_config=self.generation_config
                )
                return res.text
            except DeadlineExceeded:
                print("Deadline exceeded. Retrying...")
                retries += 1
                time.sleep(1)  # Wait for a moment before retrying
                continue


class ClaudePlayer(LLMPlayer):
    def __init__(self, model, sys_key, **model_kwargs):
        super().__init__(model, **model_kwargs)
        self.model_kwargs = model_kwargs
        self.model_type = llms[model]['model_type']
        self.sys_prompt = self.set_sys(model_kwargs[sys_key])
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_KEY"])

    def update(self, player_id='player1', **model_kwargs):
        for k, v in model_kwargs.items():
            if k in self.model_kwargs.keys():
                self.model_kwargs[k] = v
                if 'sys_' + player_id in k:
                    self.set_sys(v)

    def set_sys(self, sys):
        if type(sys) == dict:
            sys = sys['prefix']
        self.sys_prompt = sys
        return sys

    def decide(self, prompt, max_retries=10):
        retries = 0
        while retries < max_retries:
            try:
                res = self.client.messages.create(
                    model=self.model_name,
                    temperature=self.temperature,
                    max_tokens=1024,
                    system=self.sys_prompt,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return res.content[0].text
            except Exception as e:
                print("Exception. Retrying...")
                retries += 1
                time.sleep(1)  # Wait for a moment before retrying
                continue


class DeterministicProposalPlayer:
    def __init__(self, **player_kwargs):
        self.sys_prompt = ''
        self.offer = player_kwargs['offer']

    def update(self, **player_kwargs):
        if 'offer' in player_kwargs.keys():
            self.offer = player_kwargs['offer']
        return

    def set_sys(self, sys):
        return

    def decide(self, prompt):
        # Ignore prompt
        return "Offer: %d" % int(self.offer)


class EmptyPlayer:
    def __init__(self):
        self.sys_prompt = ''

    def update(self, **player_kwargs):
        pass

    def set_sys(self, sys):
        return

    def decide(self, prompt):
        # Ignore prompt
        return 'Decision: accept'
