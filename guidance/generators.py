import openai
import pathlib
import diskcache
import os

curr_dir = pathlib.Path(__file__).parent.resolve()
_file_cache = diskcache.Cache(f"{curr_dir}/../lm.diskcache")

try:
    with open(os.path.expanduser('~/.openai_lm_model_name'), 'r') as file:
        gpt_model = file.read().replace('\n', '')
except:
    raise Exception("Warning: No OpenAI model name found, you need to put your OpenAI model name in the file ~/.openai_lm_model_name")


try:
    with open(os.path.expanduser('~/.openai_api_key'), 'r') as file:
        openai.api_key = file.read().replace('\n', '')
except:
    raise Exception("Warning: No OpenAI api key found, you need to put your OpenAI key in the file ~/.openai_api_key")


class OpenAI():
    def __init__(self, model=None):
        if model is None:
            model = gpt_model
        self.model = model
    
    def __call__(self, prompt, stop=None, temperature=0.0, n=1, max_tokens=250, logprobs=None):
        key = "_---_".join([str(v) for v in (self.model, prompt, stop, temperature, n, max_tokens, logprobs)])
        if key not in _file_cache:
            print("CALLING LM")
            _file_cache[key] = openai.Completion.create(
                model=self.model, prompt=prompt, max_tokens=max_tokens,
                temperature=temperature, top_p=1.0, n=n, stop=stop, logprobs=logprobs
            )
        return _file_cache[key]
