import inspect
from abc import ABC, abstractmethod
from enum import Enum
from typing import Union

import guidance

from coding_assistant_webui._jobs import CodeJobs
from coding_assistant_webui._specifications import Specifications


class ModelNames(Enum):
    """Enum for model names.

    If you want to use a model other than the ones listed here,
    you can add it to this enum.
    """

    GPT_4: str = "gpt-4"
    GPT_3_5_TURBO: str = "gpt-3.5-turbo"


class BaseModel(ABC):
    """Base class for generation.

    This class does 2 things:
    1. Initializes the model with Microsoft guidance.
    2. According to the job, initializes the prompt and throw it to
    LLM.

    Attributes
    ----------
    llm: guidance.llms.OpenAI
        The model to use for generation.
        You can use models listed in
        `coding_assistant_webui._models.ModelNames`.
    """

    def __init__(
        self,
        model: Union[str, ModelNames] = ModelNames.GPT_3_5_TURBO,
    ):
        if isinstance(model, ModelNames):
            self.llm = guidance.llms.OpenAI(model=model.value)
        else:
            self.llm = guidance.llms.OpenAI(model=model)

    def __call__(
        self,
        job: str,
        base_input: str,
        *,
        specifications: list[Specifications] = [],
        temperature: float = 0.1,
        max_tokens: int = 100,
        **kwargs,
    ) -> str:
        """Generate something according to the job.

        Parameters
        ----------
        job: str
            The job to do.
        base_input: str
            The base input sentence to throw to the model.
        specifications: list[Specifications]
            The specifications to add to the prompt.
        temperature: float
            The temperature to use for generation.
        max_tokens: int
            The maximum tokens to generate.

        Returns
        -------
        str
            The generated string.
        """
        # 1. Initialize the prompt according to the job
        plan = guidance(
            self._init_prompt(
                job,
                specifications=specifications,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            ),
            llm=self.llm,
        )

        # 2. Throw the prompt to the model
        res = plan(base_input=base_input)

        # 3. Return the generated string
        return res["answer"]

    @abstractmethod
    def _init_prompt(
        self,
        job: str,
        specifications: list[Specifications] = [],
        temperature: float = 0.1,
        max_tokens: int = 100,
        **kwargs,
    ) -> str:
        """Initialize the prompt according to the job.

        Parameters
        ----------
        job: str
            The job to do.
        specifications: list[Specifications]
            The specifications to add to the prompt.
        temperature: float
            The temperature to use for generation.
        max_tokens: int
            The maximum tokens to generate.

        Returns
        -------
        str
            The whole prompt to throw to the model.
        """
        pass


class CodeModel(BaseModel):
    """Model for code generation.

    Attributes
    ----------
    llm: guidance.llms.OpenAI
        The model used for code generation.
        You can use models listed in
        `coding_assistant_webui._models.ModelNames`.
    """

    def __init__(
        self,
        model: Union[str, ModelNames] = ModelNames.GPT_3_5_TURBO,
    ):
        super().__init__(model=model)

    def _init_prompt(
        self,
        job: str,
        specifications: list[Specifications] = [],
        temperature: float = 0.1,
        max_tokens: int = 100,
        **kwargs,
    ) -> str:
        # 1. Get the code specification according to the job
        specification = CodeJobs.job_to_func(job)(
            specifications=specifications, **kwargs
        )

        # 2. If the job needs code as `base_input`, add a code block
        if CodeJobs.job_need_base_input(job):
            code_block = inspect.cleandoc(
                """
                ```
                {{base_input}}
                ```
                """
            )
        else:
            code_block = ""

        # 3. Initialize the prompt
        prompt = inspect.cleandoc(
            f"""\
            {{{{#system~}}}}
            You are a helpful assistant.
            {{{{~/system}}}}
            {{{{#user~}}}}
            {specification}
            {code_block}
            {{{{~/user}}}}
            {{{{#assistant~}}}}
            {{{{gen 'answer' temperature={temperature} max_tokens={max_tokens}}}}}
            {{{{~/assistant}}}}\
            """
        )

        # 4. remove all indentation from prompt and return
        return "\n".join([line.strip() for line in prompt.splitlines()])
