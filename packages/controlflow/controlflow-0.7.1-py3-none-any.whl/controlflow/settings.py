import os
import sys
import warnings
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Union

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    pass


class ControlFlowSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CONTROLFLOW_",
        env_file=(
            ""
            if os.getenv("CONTROLFLOW_TEST_MODE")
            else ("~/.controlflow/.env", ".env")
        ),
        extra="allow",
        arbitrary_types_allowed=True,
        validate_assignment=True,
    )


class PrefectSettings(ControlFlowSettings):
    """
    All settings here are used as defaults for Prefect, unless overridden by env vars.
    Note that `apply()` must be called before Prefect is imported.
    """

    PREFECT_LOGGING_LEVEL: str = "WARNING"
    PREFECT_EXPERIMENTAL_ENABLE_NEW_ENGINE: str = "true"

    def apply(self):
        import os

        if "prefect" in sys.modules:
            warnings.warn(
                "Prefect has already been imported; ControlFlow defaults will not be applied."
            )

        for k, v in self.model_dump().items():
            if k not in os.environ:
                os.environ[k] = v


class Settings(ControlFlowSettings):
    max_task_iterations: Optional[int] = Field(
        default=100,
        description="The maximum number of iterations to attempt to complete a task "
        "before raising an error. If None, the task will run indefinitely. "
        "This setting can be overridden by the `max_iterations` attribute "
        "on a task.",
    )
    prefect: PrefectSettings = Field(default_factory=PrefectSettings)

    # ------------ home settings ------------

    home_path: Path = Field(
        default="~/.controlflow",
        description="The path to the ControlFlow home directory.",
        validate_default=True,
    )

    # ------------ display and logging settings ------------

    # ------------ flow settings ------------

    eager_mode: bool = Field(
        default=True,
        description="If True, @task- and @flow-decorated functions are run immediately. "
        "This can be set on a per-task or per-flow basis using the `eager` argument.",
    )
    enable_local_input: bool = Field(
        default=True,
        description="If True, the user can provide input via "
        "the terminal. Otherwise, only API input is accepted.",
    )
    strict_flow_context: bool = Field(
        default=False,
        description="If False, calling Task.run() outside a flow context will automatically "
        "create a flow and run the task within it. If True, an error will be raised.",
    )

    # ------------ LLM settings ------------

    llm_model: str = Field(default="openai/gpt-4o", description="The LLM model to use.")
    llm_temperature: float = Field(0.7, description="The temperature for LLM sampling.")

    # ------------ Flow visualization settings ------------

    enable_print_handler: bool = Field(
        default=True,
        description="If True, the PrintHandler will be enabled. Superseded by the enable_tui setting.",
    )

    enable_tui: bool = Field(
        default=False,
        description="If True, the TUI will be enabled. If False, the TUI will be disabled.",
    )
    run_tui_headless: bool = Field(
        default=False,
        description="If True, the TUI will run in headless mode, which is useful for debugging.",
    )

    # ------------ Debug settings ------------

    raise_on_tool_error: bool = Field(
        True, description="If True, an error in a tool call will raise an exception."
    )

    print_handler_width: Optional[int] = Field(
        default=None,
        description="The number of coloumns to use for the print handler. If None, the width of "
        "the terminal will be used. Useful for screenshots and examples that need to fit a known width. For docs, use 50.",
    )

    def model_post_init(self, __context: Any) -> None:
        self.prefect.apply()
        return super().model_post_init(__context)

    @field_validator("home_path", mode="before")
    def _validate_home_path(cls, v: Union[str, Path]) -> Path:
        v = Path(v).expanduser()
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v


settings = Settings()


@contextmanager
def temporary_settings(**kwargs: Any):
    """
    Temporarily override ControlFlow setting values, including nested settings objects.

    To override nested settings, use `__` to separate nested attribute names.

    Args:
        **kwargs: The settings to override, including nested settings.

    Example:
        Temporarily override log level and OpenAI API key:
        ```python
        import controlflow
        from controlflow.settings import temporary_settings

        # Override top-level settings
        with temporary_settings(log_level="INFO"):
            assert controlflow.settings.log_level == "INFO"
        assert controlflow.settings.log_level == "DEBUG"

        # Override nested settings
        with temporary_settings(openai__api_key="new-api-key"):
            assert controlflow.settings.openai.api_key.get_secret_value() == "new-api-key"
        assert controlflow.settings.openai.api_key.get_secret_value().startswith("sk-")
        ```
    """
    old_env = os.environ.copy()
    old_settings = deepcopy(settings)

    def set_nested_attr(obj: object, attr_path: str, value: Any):
        parts = attr_path.split("__")
        for part in parts[:-1]:
            obj = getattr(obj, part)
        setattr(obj, parts[-1], value)

    try:
        for attr_path, value in kwargs.items():
            set_nested_attr(settings, attr_path, value)
        yield

    finally:
        os.environ.clear()
        os.environ.update(old_env)

        for attr, value in old_settings:
            set_nested_attr(settings, attr, value)
