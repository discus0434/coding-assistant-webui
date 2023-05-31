import gradio as gr
from dotenv import load_dotenv

from coding_assistant_webui import CodeModel, ModelNames, Specifications

load_dotenv()


class GradioInterface:
    def __init__(self, job: str):
        self.job = job

    async def generate(
        self,
        model: str,
        temperature: float,
        max_tokens: int,
        specifications: list[str],
        inp: str = "",
        requirements: str = "",
        code_lang: str = "",
        input_type: str = "",
        output_type: str = "",
    ) -> str:
        if specifications is not None:
            specifications = [Specifications[spec] for spec in specifications]
        else:
            specifications = []

        code = CodeModel(model=model)
        res = code(
            job=self.job,
            base_input=inp,
            specifications=specifications,
            temperature=temperature,
            max_tokens=max_tokens,
            requirements=requirements,
            code_lang=code_lang,
            input_type=input_type,
            output_type=output_type,
        )
        return res


if __name__ == "__main__":
    with gr.Blocks() as demo:
        model = gr.Dropdown(
            [model.value for model in ModelNames],
            value="gpt-3.5-turbo",
            label="Which model do you want to use?",
        )
        temperature = gr.Slider(
            minimum=0.0, maximum=1.0, value=0.1, step=0.1, label="Temperature"
        )
        max_tokens = gr.Slider(
            minimum=100, maximum=5000, value=500, step=100, label="Max tokens"
        )

        specs = gr.CheckboxGroup(
            [spec for spec in Specifications._member_names_],
            value=None,
            label="What specifications do you want to add?",
        )

        with gr.Tab(label="Refactoring"):
            with gr.Row():
                with gr.Column():
                    inp = gr.Textbox(
                        placeholder="Paste your code here",
                        lines=10,
                        max_lines=500,
                        label="Input code",
                    )
                    btn = gr.Button("Generate")
                with gr.Column():
                    out = gr.Textbox(label="Output")
                    btn.click(
                        fn=GradioInterface(job="REFACTORING").generate,
                        inputs=[model, temperature, max_tokens, specs, inp],
                        outputs=out,
                    )

        with gr.Tab(label="Explaining"):
            with gr.Row():
                with gr.Column():
                    inp = gr.Textbox(
                        placeholder="Paste your code here",
                        lines=10,
                        max_lines=500,
                        label="Input code",
                    )
                    btn = gr.Button("Generate")

                with gr.Column():
                    out = gr.Textbox(label="Output")
                    btn.click(
                        fn=GradioInterface(job="EXPLAINING").generate,
                        inputs=[model, temperature, max_tokens, specs, inp],
                        outputs=out,
                    )

        with gr.Tab(label="Checking"):
            with gr.Row():
                with gr.Column():
                    inp = gr.Textbox(
                        placeholder="Paste your code here",
                        lines=10,
                        max_lines=500,
                        label="Input code",
                    )
                    btn = gr.Button("Generate")

                with gr.Column():
                    out = gr.Textbox(label="Output")
                    btn.click(
                        fn=GradioInterface(job="CHECKING").generate,
                        inputs=[model, temperature, max_tokens, specs, inp],
                        outputs=out,
                    )

        with gr.Tab(label="Adding"):
            with gr.Row():
                with gr.Column():
                    inp = gr.Textbox(
                        placeholder="Paste your code here",
                        lines=10,
                        max_lines=500,
                        label="Input code",
                    )

                    requirements = gr.Textbox(
                        placeholder="Write feature requirements here",
                        lines=5,
                        max_lines=10,
                        label="Feature requirements",
                    )

                    btn = gr.Button("Generate")

                with gr.Column():
                    out = gr.Textbox(label="Output")
                    btn.click(
                        fn=GradioInterface(job="ADDING").generate,
                        inputs=[
                            model,
                            temperature,
                            max_tokens,
                            specs,
                            inp,
                            requirements,
                        ],
                        outputs=out,
                    )

        with gr.Tab(label="Implementing"):
            with gr.Row():
                with gr.Column():
                    inp = gr.Textbox(
                        placeholder="Paste your code here",
                        lines=0,
                        max_lines=1,
                        visible=False,
                        label="Input code",
                    )

                    requirements = gr.Textbox(
                        placeholder="Write feature requirements here",
                        lines=5,
                        max_lines=10,
                        label="Feature requirements",
                    )

                    code_lang = gr.Textbox(
                        placeholder="Desired code language (e.g. Python, C++, etc.)",
                        lines=1,
                        max_lines=2,
                        label="Code language",
                    )

                    input_type = gr.Textbox(
                        placeholder="Desired input type (e.g. int, str, list, etc.)",
                        lines=1,
                        max_lines=2,
                        label="Input type (Optional)",
                    )

                    output_type = gr.Textbox(
                        placeholder="Desired output type (e.g. int, str, list, etc.)",
                        lines=1,
                        max_lines=2,
                        label="Output type (Optional)",
                    )
                    btn = gr.Button("Generate")

                with gr.Column():
                    out = gr.Textbox(label="Output")
                    btn.click(
                        fn=GradioInterface(job="IMPLEMENTING").generate,
                        inputs=[
                            model,
                            temperature,
                            max_tokens,
                            specs,
                            inp,
                            requirements,
                            code_lang,
                            input_type,
                            output_type,
                        ],
                        outputs=out,
                    )

        with gr.Tab(label="Transpiling"):
            with gr.Row():
                with gr.Column():
                    inp = gr.Textbox(
                        placeholder="Paste your code here",
                        lines=10,
                        max_lines=500,
                        label="Input code",
                    )

                    requirements = gr.Textbox(
                        placeholder="Write feature requirements here",
                        lines=0,
                        max_lines=1,
                        visible=False,
                    )

                    code_lang = gr.Textbox(
                        placeholder="Code language",
                        lines=1,
                        max_lines=2,
                        label="Code language",
                    )

                    btn = gr.Button("Generate")

                with gr.Column():
                    out = gr.Textbox(label="Output")
                    btn.click(
                        fn=GradioInterface(job="TRANSPILING").generate,
                        inputs=[
                            model,
                            temperature,
                            max_tokens,
                            specs,
                            inp,
                            requirements,
                            code_lang,
                        ],
                        outputs=out,
                    )

    demo.launch()
