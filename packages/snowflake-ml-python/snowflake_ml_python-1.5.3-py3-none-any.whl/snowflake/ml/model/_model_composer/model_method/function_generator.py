import pathlib
from typing import Optional, TypedDict

from typing_extensions import NotRequired

from snowflake.ml.model import type_hints


class FunctionGenerateOptions(TypedDict):
    max_batch_size: NotRequired[Optional[int]]
    function_type: NotRequired[str]


def get_function_generate_options_from_options(
    options: type_hints.ModelSaveOption, target_method: str
) -> FunctionGenerateOptions:
    method_options = options.get("method_options", {}).get(target_method, {})
    return FunctionGenerateOptions(
        max_batch_size=method_options.get("max_batch_size", None),
        function_type=method_options.get("function_type", "function"),
    )


class FunctionGenerator:
    FUNCTION_NAME = "infer"

    def __init__(
        self,
        model_file_rel_path: pathlib.PurePosixPath,
    ) -> None:
        self.model_file_rel_path = model_file_rel_path

    def generate(
        self,
        function_file_path: pathlib.Path,
        target_method: str,
        function_type: str,
        options: Optional[FunctionGenerateOptions] = None,
    ) -> None:
        import importlib_resources

        if options is None:
            options = {}

        template_filename = f"infer_{function_type.lower()}.py_template"

        function_template = (
            importlib_resources.files("snowflake.ml.model._model_composer.model_method")
            .joinpath(template_filename)
            .read_text()
        )

        udf_code = function_template.format(
            model_file_name=self.model_file_rel_path.name,
            target_method=target_method,
            max_batch_size=options.get("max_batch_size", None),
            function_name=FunctionGenerator.FUNCTION_NAME,
        )
        with open(function_file_path, "w", encoding="utf-8") as f:
            f.write(udf_code)
            f.flush()
