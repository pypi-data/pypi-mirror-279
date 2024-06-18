import openai
from os import getenv
from tiktoken import encoding_for_model
import logging

# Default generic model (not fine-tuned) to use for common tasks
DEFAULT_GENERIC_MODEL = 'gpt-4o'
DEFAULT_GENERIC_MODEL_TOKENIZER = 'gpt-3.5-turbo'

# The latest default set production model for the Bootstrap inferencer.
LATEST_DEFAULT_BOOTSTRAP_MODEL = 'ft:gpt-3.5-turbo-0125:globy:globy-bootstrap-03:9B9vtaMj'

class Inferencer:
    """
    Base class for the inferencers.
    """
    def __init__(self, **kwargs):
        self.model_type = kwargs['model_type']
        self.noop = kwargs.get('noop', False)
        self.verbose = kwargs.get('verbose', False)
        self.logger = kwargs.get('logger', logging.getLogger("GlobyLogger"))
        self.log_prefix = kwargs.get('log_prefix', 'Inferencer')
        self.context = kwargs.get('context', None)
        if self.model_type == 'OPENAI':
            self.client = openai.OpenAI(api_key=getenv('OPENAI_API_KEY'))
            self.model = DEFAULT_GENERIC_MODEL
            self.tokenizer = OpenAITokenizer(DEFAULT_GENERIC_MODEL_TOKENIZER)

    def generate(self, sample, check_token_limit=False, history=None, temperature=None, seed=None) -> str:
        """
        Perform inference on the sample and return the response.
        """
        if check_token_limit and self.tokenizer.exceeds_token_limit(sample):
            self.logger.error(f"[{self.log_prefix}] ERROR: The token count of the sample ({len(sample)}) exceeds the model's token limit ({self.tokenizer.max_tokens}). Skipping sample.")
            return None
        if self.verbose:
            print(f'{self.log_prefix}] Performing inference on the input sample...')
        self.logger.debug(f"\n[{self.log_prefix}] [Inference data]{sample}[/Inference data]\n")
        if self.noop:
            return 'NOOP'
        if self.model_type == 'OPENAI':
            return self._openai_inference(sample, history=history, seed=seed, temperature=temperature)
        raise ValueError(f"Model type {self.model_type} not supported.")

    def _openai_inference(self, sample, history=None, temperature=None, seed=None, parse_samples=True) -> str:
        result = None

        # Allow the native openAI format to be passed
        if parse_samples:
            messages = self._create_openai_samples(sample)
        else:
            messages = sample
        if history:
            sample = history + [sample]
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                seed=seed,
                )
            self.logger.debug(f"\n[{self.log_prefix}] [OpenAI]{completion}[/OpenAI]\n")
            result = completion.choices[0].message
        except openai.BadRequestError as br:
            self.logger.error(f"[{self.log_prefix}] ERROR: {br} - Skipping sample.")
        return result

    def _create_openai_samples(self, samples) -> list:
        """
        Create a list of samples for the OpenAI API.
        Pass either a single message as a string or a list of messages.
        """
        if type(samples) == str:
            return [
                {"role": "system", "content": f"{self.context}"},
                {"role": "user", "content": f"{samples}"}
            ]
        messages = [
            {"role": "system", "content": f"{self.context}"}
        ]
        for message in samples:
            messages.append({"role": "user", "content": message})
        return messages



class Tokenizer:
    """
    Base class for the tokenizers.
    """
    def __init__(self, model):
        self.tokenizer = encoding_for_model(model)
        self.max_tokens = 4096

    def exceeds_token_limit(self, text) -> bool:
        """ Check if the token count of the text is within the model's token limit. """
        tokens = self.tokenizer.encode(text)
        return len(tokens) >= self.max_tokens


class BootstrapInferencer(Inferencer):
    """
    Bootstrap inferencer. This inferencer can be used for converting HTML code to Visual Composer code.
    Refer to NewBootstrapInferencer() function for creating a new instance of this class and any params that you may want to pass.
    """
    def __init__(self, **kwargs):
        kwargs['context'] = "You are a professional web developer that converts HTML code to Visual Composer code."
        super().__init__(**kwargs)
        if self.model_type == 'OPENAI':
            if 'model' in kwargs:
                self.model = kwargs['model']
                print(f"Using specified overriden model: {self.model}")
            else:
                self.model = LATEST_DEFAULT_BOOTSTRAP_MODEL
            self.tokenizer = OpenAITokenizer('gpt-3.5-turbo')


class ChatCompletion(Inferencer):
    """
    Chat completion inferencer. This inferencer can be used for chatbot interactions or instruct use cases like interacting with a Globy assistant.
    Refer to NewChatBot() function for creating a new instance of this class and any params that you may want to pass.
    """
    def __init__(self, **kwargs):
        self.context = kwargs['context']
        self.seed = kwargs.get('seed', None)
        super().__init__(**kwargs)
        if self.model_type == 'OPENAI':
            if 'model' in kwargs:
                self.model = kwargs['model']
                print(f"Using specified overriden model: {self.model}")
            else:
                self.model = DEFAULT_GENERIC_MODEL
            self.tokenizer = OpenAITokenizer(DEFAULT_GENERIC_MODEL_TOKENIZER)

    def start_interactive_chat(self):
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            response = self._openai_inference(user_input, seed=self.seed, parse_samples=False)
            print(f"Model: {response}")

    def start_chat(self, user_input: dict):
        """
        Args:
        "user_input" - The user input to start the chat.
        """
        return self._openai_inference(user_input, seed=self.seed, parse_samples=False)

    def chat(self, user_input: dict):
        """
        Args:
        "user_input" - The user input to continue the chat.
        """
        return self._openai_inference(user_input, seed=self.seed, parse_samples=False)


class OpenAITokenizer(Tokenizer):
    def __init__(self, model):
        self.tokenizer = encoding_for_model(model)
        self.max_tokens = 16385


def NewBootstrapInferencer(html_code, output_queue, inferencer_kwargs, model_type='OPENAI') -> BootstrapInferencer:
    """
    Create a new instance of the BootstrapInferencer.

    Required args:
    "html_code" - The HTML content to be processed.
    "output_queue" - The queue to store the results.
    "model_type" - The model type to use for inference. Default is 'OPENAI'.
    "inferencer_args" is an optional dictionary passed to the inferencer:
    - noop: No operation mode. Will just process the data. Default is False.
    - verbose: Enable verbose mode. Default is False.
    - logger: Logger instance.
    - log_prefix: Prefix for the log messages.
    - model: Use this to override the default model, e.g. 'gpt-4o' or 'gpt-3.5-turbo'.
    """
    inferencer_kwargs['model_type'] = model_type
    worker = BootstrapInferencer(**inferencer_kwargs)
    output_queue.put(worker.generate(html_code))
    return worker

def NewBootstrapTokenizer(model='gpt-3.5-turbo') -> OpenAITokenizer:
    """
    Create a new instance of the BootstrapTokenizer.
    """
    return OpenAITokenizer(model)

def NewChatBot(context, inferencer_kwargs=None, model_type='OPENAI') -> ChatCompletion:
    """
    Create a new instance of the ChatCompletion.

    Required args:
    "context" - The context/instruction. Also known as "system prompt".
    "output_queue" - The queue to store the results.
    "model_type" - The model type to use for inference. Default is 'OPENAI'.
    "inferencer_args" is an optional dictionary passed to the inferencer:
    - noop: No operation mode. Will just process the data. Default is False.
    - verbose: Enable verbose mode. Default is False.
    - logger: Logger instance.
    - log_prefix: Prefix for the log messages.
    - model: Use this to override the default model, e.g. 'gpt-4o' or 'gpt-3.5-turbo'.
    """
    if not inferencer_kwargs:
        inferencer_kwargs = {}
    inferencer_kwargs['model_type'] = model_type
    inferencer_kwargs['context'] = context
    worker = ChatCompletion(**inferencer_kwargs)
    return worker

def NewBootstrapTokenizer(model='gpt-3.5-turbo') -> OpenAITokenizer:
    """
    Create a new instance of the BootstrapTokenizer.
    """
    return OpenAITokenizer(model)