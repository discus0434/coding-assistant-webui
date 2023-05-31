import inspect
from abc import ABC, abstractstaticmethod
from typing import Callable

from coding_assistant_webui.specifications import Specifications


class Jobs(ABC):
    @abstractstaticmethod
    def job_to_func(job: str) -> Callable:
        """Convert a job to a function name.

        Parameters
        ----------
        job: str
            The job name.

        Returns
        -------
        Callable
            The function to use for the job.

        Raises
        ------
        ValueError
            If the job is not supported.
        """
        raise NotImplementedError

    @abstractstaticmethod
    def job_need_base_input(job: str) -> bool:
        """Check if the job needs base input.

        Parameters
        ----------
        job: str
            The job name.

        Returns
        -------
        bool
            If the job needs base input.

        Raises
        ------
        ValueError
            If the job is not supported.
        """
        raise NotImplementedError


class CodeJobs(Jobs):
    @staticmethod
    def job_to_func(job: str) -> Callable:
        JOB_TO_FUNC = {
            "REFACTORING": CodeJobs.REFACTORING,
            "EXPLAINING": CodeJobs.EXPLAINING,
            "CHECKING": CodeJobs.CHECKING,
            "ADDING": CodeJobs.ADDING,
            "IMPLEMENTING": CodeJobs.IMPLEMENTING,
            "TRANSPILING": CodeJobs.TRANSPILING,
        }

        if job not in JOB_TO_FUNC:
            raise ValueError(f"job must be one of {list(JOB_TO_FUNC.keys())}")

        return JOB_TO_FUNC[job]

    @staticmethod
    def job_need_base_input(job: str) -> bool:
        JOB_NEED_BASE_INPUT = {
            "REFACTORING": True,
            "EXPLAINING": True,
            "CHECKING": True,
            "ADDING": True,
            "IMPLEMENTING": False,
            "TRANSPILING": True,
        }

        return JOB_NEED_BASE_INPUT[job]

    @staticmethod
    def REFACTORING(
        specifications: list[Specifications] = [],
        **kwargs,
    ) -> str:
        """Refactor the code input as `base_input`.

        Parameters
        ----------
        specifications: list[Specifications]
            The specifications to add to the prompt.
        """
        specs = CodeJobs._add_addtional_specs(specifications)

        return inspect.cleandoc(
            f"""\
            Refactor the code below. To be better, you can use any libraries.

            {specs}

            Code:\
            """
        )

    @staticmethod
    def EXPLAINING(
        specifications: list[Specifications] = [],
        **kwargs,
    ) -> str:
        """Explain the code input as `base_input`.

        Parameters
        ----------
        specifications: list[Specifications]
            The specifications to add to the prompt.
        """
        specs = CodeJobs._add_addtional_specs(specifications)

        return inspect.cleandoc(
            f"""\
            Explain the code below.

            {specs}

            Code:\
            """
        )

    @staticmethod
    def CHECKING(
        specifications: list[Specifications] = [],
        **kwargs,
    ) -> str:
        """Check the code input as `base_input`.

        Parameters
        ----------
        specifications: list[Specifications]
            The specifications to add to the prompt.
        """
        specs = CodeJobs._add_addtional_specs(specifications)

        return inspect.cleandoc(
            f"""\
            Please check for potential issues in the code below.

            {specs}

            Code:\
            """
        )

    @staticmethod
    def ADDING(
        specifications: list[Specifications] = [],
        **kwargs,
    ) -> str:
        """Add a new feature to the code input as `base_input`.

        Parameters
        ----------
        specifications: list[Specifications]
            The specifications to add to the prompt.
        requirements: str
            The requirements of the newly added feature.

        Raises
        ------
        ValueError
            If `requirements` is not specified.
        """
        if "requirements" not in kwargs:
            raise ValueError(
                "You must specify the requirements of a newly added function with `kwargs['requirements']`."
            )

        specs = CodeJobs._add_addtional_specs(specifications)

        return inspect.cleandoc(
            f"""\
            Add a feature to the code below, following the specifications.

            Requirements of a newly added feature:
            {kwargs['requirements']}

            {specs}

            Code (before adding a feature):\
            """
        )

    @staticmethod
    def IMPLEMENTING(
        specifications: list[Specifications] = [],
        **kwargs,
    ) -> str:
        """Implement a new feature to the code input as `base_input`.

        Parameters
        ----------
        specifications: list[Specifications]
            The specifications to add to the prompt.
        requirements: str
            The requirements of the newly implemented code.
        code_lang: str
            The language of the newly implemented code.
        input_type: str, optional
            The input type of the newly implemented code,
            such as `str` `list[int]`.
        output_type: str, optional
            The output type of the newly implemented code,
            such as `np.float32` or `dict[str, str]`.

        Raises
        ------
        ValueError
            If `requirements` or `code_lang` is not specified.
        """
        if "requirements" not in kwargs or "code_lang" not in kwargs:
            raise ValueError(
                "You must specify the language of the newly implemented feature with these kwargs:",
                "kwargs['requirements']",
                "kwargs['code_lang']",
                "You can also specify the kwargs['input_type'] and kwargs['output_type'] if you want.",
            )

        if kwargs.get("input_type"):
            input_type_str = f"- **Input type**: {kwargs['input_type']}"
        else:
            input_type_str = ""

        if kwargs.get("output_type"):
            output_type_str = f"- **Output type**: {kwargs['output_type']}"
        else:
            output_type_str = ""

        specs = CodeJobs._add_addtional_specs(specifications)

        return inspect.cleandoc(
            f"""\
            Implement a code that satisfies the specifications.

            Requirements of a newly implemented code:
            - The code must be written in {kwargs['code_lang']}. Use of any other languages than {kwargs['code_lang']} are strictly prohibited.
            - The code must satisfy the following requirements:
            {kwargs['requirements']}
            {input_type_str}
            {output_type_str}

            {specs}

            Then, please implement a code that satisfies all the specifications.
            """
        )

    @staticmethod
    def TRANSPILING(
        specifications: list[Specifications] = [],
        **kwargs,
    ) -> str:
        """Transpile the code input as `base_input` into `code_lang`.

        Parameters
        ----------
        specifications: list[Specifications], optional
            The specifications to add to the prompt.

        Raises
        ------
        ValueError
            If `code_lang` is not specified.
        """
        if "code_lang" not in kwargs:
            raise ValueError(
                "You must specify the language of the newly transpiled code with `kwargs['code_lang']`."
            )

        specs = CodeJobs._add_addtional_specs(specifications)

        return inspect.cleandoc(
            f"""\
            Transpile the code below into {kwargs['code_lang']}.

            {specs}

            Code (before transpiling):\
            """
        )

    @staticmethod
    def _add_addtional_specs(specifications: list[Specifications]) -> str:
        if not specifications:
            return ""

        specs = "\n".join([f"- {spec.value}" for spec in specifications])
        specs = f"\nIn addition, the result must obey the specifications:\n{specs}"

        return specs
