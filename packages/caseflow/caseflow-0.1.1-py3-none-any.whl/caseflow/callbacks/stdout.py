from typing import Any, Dict, List, Optional, TextIO
from uuid import UUID
from caseflow.callbacks.base import CaseStepBaseCallbackHandler
from caseflow.model import CaseRespnseModel

_TEXT_COLOR_MAPPING = {
    "blue": "36;1",
    "yellow": "33;1",
    "pink": "38;5;200",
    "green": "32;1",
    "red": "31;1",
}


def get_colored_text(text: str, color: str) -> str:
    """Get colored text."""
    color_str = _TEXT_COLOR_MAPPING[color]
    return f"\u001b[{color_str}m\033[1;3m{text}\u001b[0m"


def print_text(
    text: str, color: Optional[str] = None, end: str = "", file: Optional[TextIO] = None
) -> None:
    """Print text with highlighting and no end characters."""
    text_to_print = get_colored_text(text, color) if color else text
    print(text_to_print, end=end, file=file)  # noqa: T201
    if file:
        file.flush()  # ensure all printed content are written to file


class CaseStepStdOutCallbackHandler(CaseStepBaseCallbackHandler):

    def on_case_start(self, caseInfo, **kwargs):

        print_text("[case/start] ", color="green", end="")
        print(f"{caseInfo=}")

    def on_case_error(self, caseInfo, error, **kwargs):

        print_text("[case/error] ", color="red", end="")
        print(f"{error=}")

    def on_case_end(
        self,
        caseInfo: Dict | Dict[str, Any],
        caseResult: CaseRespnseModel,
        **kwargs: Any,
    ) -> Any:

        print_text("[case/end] ", color="green", end="")
        print(f"{caseResult=}")

    def on_case_step_start(
        self,
        stepEntry: Dict | Dict[str, Any],
        run_id: UUID,
        **kwargs: Any,
    ) -> Any:
        stepIndex = kwargs.get("stepIndex")
        print_text(
            f"[case_step/start] stepId: {run_id.hex} stepIndex: {stepIndex}",
            color="green",
            end="\n",
        )
        print(f"{stepEntry=}")

    def on_case_step_end(
        self,
        stepEntry: Dict | Dict[str, Any],
        stepResult,
        *,
        run_id: UUID,
        response=None,
        isCheckSusscess: bool | None = None,
        variables: Dict | Dict[str, Any] | None = None,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        metadata: Dict | Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        stepIndex = kwargs.get("stepIndex")
        print_text(
            f"[case_step/end] stepId: {run_id.hex} stepIndex: {stepIndex}",
            color="green",
            end="\n",
        )
        print(f"{stepResult=}")

    def on_step_output(
        self,
        stepEntry: Dict | Dict[str, Any],
        *,
        run_id: UUID,
        stepVariables: Optional[Dict[str, Any]] = None,
        stepOutputVariables: Optional[Dict[str, Any]] = None,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        metadata: Dict | Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        stepIndex = kwargs.get("stepIndex")
        print_text(
            f"[case_step/output] stepId: {run_id.hex} stepIndex: {stepIndex}",
            color="green",
            end="\n",
        )
        print(f"{stepOutputVariables=}")

    def on_step_check(
        self,
        stepEntry: Dict | Dict[str, Any],
        *,
        run_id: UUID,
        stepResponse=None,
        stepRespText: str | None = None,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        metadata: Dict | Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        stepIndex = kwargs.get("stepIndex")
        print_text(
            f"[case_step/check] stepId: {run_id.hex} stepIndex: {stepIndex}",
            color="green",
            end="\n",
        )
        