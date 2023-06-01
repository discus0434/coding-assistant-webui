from enum import Enum


class Specifications(Enum):
    """Enum for specifications to add to the prompt.


    If you want another specification, all you need is add it to this
    enum.
    Note that the specification is sometimes ignored by the model. If
    you make the model sure to follow the specification, you may
    speak in a very strong tone, which is quite odd though.
    """

    COMMENT: str = "add a comment to the code to explain what it does, to make it easier to understand."
    DOCSTRING: str = "add a docstring to each functions and classes in **NUMPY STYLE**. You must write NUMPY STYLE DocString, NEVER Google style."
    TYPE_ANNOTATION: str = "add type annotations to the code. You can suppose that the code is written in Python 3.10."
    NO_NATURAL_LANGS: str = "**YOU MUST NOT OUTPUT ANYTHING ELSE THAT ARE NOT RELATED TO THE CODE ITSELF.**"
    WRITE_IN_JAPANESE: str = "write the entire comment and explanation in Japanese. In addition, you MUST NOT repeat user's input in Japanese."
