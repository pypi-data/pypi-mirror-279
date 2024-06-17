from __future__ import annotations

from ast import Dict
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from langchain_core.callbacks import RunManager
from langchain_core.callbacks import (
    AsyncRunManager,
    AsyncCallbackManager,
    CallbackManager,
)
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.callbacks.manager import handle_event, shielded, ahandle_event
from langchain_core.callbacks.manager import Callbacks
from langchain.globals import get_verbose

from caseflow.model import CaseRespnseModel


def ahandle_event_for_case_step(handle_event_func):
    async def wrapper(*args, **kwargs) -> None:
        handlers_ = [
            handler
            for handler in args[0]
            if issubclass(handler.__class__, CaseStepBaseCallbackHandler)
        ]
        newArgs = [
            handlers_,
        ] + list(args[1:])
        await handle_event_func(*newArgs, **kwargs)

    return wrapper


ahandle_event = ahandle_event_for_case_step(ahandle_event)


class CaseMixin:
    """Mixin for case callbacks"""

    def on_case_start(
        self,
        caseInfo: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when a case starts running."""

    def on_case_end(
        self,
        caseInfo: Dict[str, Any],
        caseResult: CaseRespnseModel,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """on_case_end"""

    def on_case_error(
        self,
        caseInfo: Dict[str, Any],
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """on_case_error"""


class CaseStepMixin:
    """Mixin for case step callbacks"""

    def on_case_step_start(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """on_case_step_start"""

    def on_case_step_end(
        self,
        stepEntry: Dict[str, Any],
        stepResult,
        *,
        run_id: UUID,
        response=None,
        isCheckSusscess:Optional[bool] = None,
        variables:Optional[Dict[str, Any]] = None,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """on_case_step_end"""

    def on_case_step_error(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """on_case_step_error"""

    def on_case_step_logic_handler(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """on_case_step_logic_handler"""

    def on_step_output(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        stepVariables:Optional[Dict[str, Any]] = None,
        stepOutputVariables:Optional[Dict[str, Any]] = None,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """ """

    def on_step_check(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        stepResponse = None,
        stepRespText: Optional[str] = None,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """ """

    def on_step_variables_set(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """ """


class CaseStepBaseCallbackHandler(CaseMixin, CaseStepMixin):
    """CaseStepBaseCallbackHandler"""

    raise_error: bool = False
    run_inline: bool = False

    @property
    def ignore_case(self) -> bool:
        """Whether to ignore case callbacks."""
        return False

    @property
    def ignore_case_step(self) -> bool:
        """Whether to ignore case step callbacks."""
        return False


class CaseSteoCallbackManager(CallbackManager, CaseMixin, CaseStepMixin):
    """Callback manager for LLM run."""

    def __init__(
        self,
        handlers: List[BaseCallbackHandler],
        inheritable_handlers: List[BaseCallbackHandler] | None = None,
        parent_run_id: UUID | None = None,
        *,
        tags: List[str] | None = None,
        inheritable_tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
        inheritable_metadata: Dict[str, Any] | None = None,
        run_id: Optional[UUID] = None,
    ) -> None:
        super().__init__(
            handlers,
            inheritable_handlers,
            parent_run_id,
            tags=tags,
            inheritable_tags=inheritable_tags,
            metadata=metadata,
            inheritable_metadata=inheritable_metadata,
        )
        self.run_id = run_id or uuid4()

    def on_case_start(
        self,
        caseInfo: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_case_start",
            "ignore_case",
            caseInfo=caseInfo,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    def on_case_end(
        self,
        caseInfo: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_case_end",
            "ignore_case",
            caseInfo=caseInfo,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    def on_case_error(
        self,
        caseInfo: Dict[str, Any],
        error: BaseException,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_case_error",
            "ignore_case",
            caseInfo=caseInfo,
            run_id=self.run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    def on_case_step_start(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_case_step_start",
            "ignore_case_step",
            stepEntry=stepEntry,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    def on_case_step_end(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_case_step_end",
            "ignore_case_step",
            stepEntry=stepEntry,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    def on_case_step_error(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_case_step_error",
            "ignore_case_step",
            stepEntry=stepEntry,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    def on_case_step_logic_handler(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_case_step_logic_handler",
            "ignore_case_step",
            stepEntry=stepEntry,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    def on_step_output(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        stepVariables:Optional[Dict[str, Any]] = None,
        stepOutputVariables:Optional[Dict[str, Any]] = None,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_step_output",
            "ignore_case_step",
            stepEntry=stepEntry,
            stepVariables=stepVariables,
            stepOutputVariables=stepOutputVariables,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    def on_step_check(
        self,
        stepEntry: Dict[str, Any],
        *,
        stepResponse = None,
        stepRespText: Optional[str] = None,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_step_check",
            "ignore_case_step",
            stepEntry=stepEntry,
            stepResponse=stepResponse,
            stepRespText=stepRespText,
            run_id=self.run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    def on_step_variables_set(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        handle_event(
            self.handlers,
            "on_step_variables_set",
            "ignore_case_step",
            stepEntry=stepEntry,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )


class AsyncCaseSteoCallbackManager(AsyncCallbackManager, CaseMixin, CaseStepMixin):
    """Callback manager for LLM run."""

    def __init__(
        self,
        handlers: List[BaseCallbackHandler],
        inheritable_handlers: List[BaseCallbackHandler] | None = None,
        parent_run_id: UUID | None = None,
        *,
        tags: List[str] | None = None,
        inheritable_tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
        inheritable_metadata: Dict[str, Any] | None = None,
        run_id: Optional[UUID] = None,
    ) -> None:
        super().__init__(
            handlers,
            inheritable_handlers,
            parent_run_id,
            tags=tags,
            inheritable_tags=inheritable_tags,
            metadata=metadata,
            inheritable_metadata=inheritable_metadata,
        )
        self.run_id = run_id or uuid4()

    def get_sync(self) -> CaseSteoCallbackManager:
        """Get the equivalent sync RunManager.

        Returns:
            CallbackManagerForLLMRun: The sync RunManager.
        """
        return CaseSteoCallbackManager(
            run_id=self.run_id,
            handlers=self.handlers,
            inheritable_handlers=self.inheritable_handlers,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            inheritable_tags=self.inheritable_tags,
            metadata=self.metadata,
            inheritable_metadata=self.inheritable_metadata,
        )

    @shielded
    async def on_case_start(
        self,
        caseInfo: Dict[str, Any],
        *,
        run_id: Optional[UUID] = None,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AsyncCaseSteoCallbackManager:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        if run_id is None:
            run_id = uuid4()
        await ahandle_event(
            self.handlers,
            "on_case_start",
            "ignore_case",
            caseInfo=caseInfo,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )
        return self.__class__(
            run_id=run_id,
            handlers=self.handlers,
            inheritable_handlers=self.inheritable_handlers,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            inheritable_tags=self.inheritable_tags,
            metadata=self.metadata,
            inheritable_metadata=self.inheritable_metadata,
        )

    @shielded
    async def on_case_end(
        self,
        caseInfo: Dict[str, Any],
        caseResult: CaseRespnseModel,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        await ahandle_event(
            self.handlers,
            "on_case_end",
            "ignore_case",
            caseInfo=caseInfo,
            caseResult=caseResult,
            run_id=self.run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    @shielded
    async def on_case_error(
        self,
        caseInfo: Dict[str, Any],
        error: BaseException,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        await ahandle_event(
            self.handlers,
            "on_case_error",
            "ignore_case",
            caseInfo=caseInfo,
            error=error,
            run_id=self.run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    @shielded
    async def on_case_step_start(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AsyncCaseSteoCallbackManager:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """

        if run_id is None:
            run_id = uuid4()

        await ahandle_event(
            self.handlers,
            "on_case_step_start",
            "ignore_case_step",
            stepEntry=stepEntry,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )
        return self.__class__(
            run_id=run_id,
            handlers=self.handlers,
            inheritable_handlers=self.inheritable_handlers,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            inheritable_tags=self.inheritable_tags,
            metadata=self.metadata,
            inheritable_metadata=self.inheritable_metadata,
        )

    @shielded
    async def on_case_step_end(
        self,
        stepEntry: Dict[str, Any],
        stepResult,
        *,
        response=None,
        isCheckSusscess:Optional[bool] = None,
        variables:Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        await ahandle_event(
            self.handlers,
            "on_case_step_end",
            "ignore_case_step",
            stepEntry=stepEntry,
            stepResult=stepResult,
            response=response,
            isCheckSusscess=isCheckSusscess,
            variables=variables,
            run_id=self.run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    @shielded
    async def on_case_step_error(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        await ahandle_event(
            self.handlers,
            "on_case_step_error",
            "ignore_case_step",
            stepEntry=stepEntry,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    @shielded
    async def on_case_step_logic_handler(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        await ahandle_event(
            self.handlers,
            "on_case_step_logic_handler",
            "ignore_case_step",
            stepEntry=stepEntry,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    @shielded
    async def on_step_output(
        self,
        stepEntry: Dict[str, Any],
        *,
        stepVariables:Optional[Dict[str, Any]] = None,
        stepOutputVariables:Optional[Dict[str, Any]] = None,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        await ahandle_event(
            self.handlers,
            "on_step_output",
            "ignore_case_step",
            stepEntry=stepEntry,
            stepVariables=stepVariables,
            stepOutputVariables=stepOutputVariables,
            run_id=self.run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    @shielded
    async def on_step_check(
        self,
        stepEntry: Dict[str, Any],
        *,
        stepResponse = None,
        stepRespText: Optional[str] = None,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        await ahandle_event(
            self.handlers,
            "on_step_check",
            "ignore_case_step",
            stepEntry=stepEntry,
            stepResponse=stepResponse,
            stepRespText=stepRespText,
            run_id=self.run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    @shielded
    async def on_step_variables_set(
        self,
        stepEntry: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM generates a new token.

        Args:
            token (str): The new token.
        """
        await ahandle_event(
            self.handlers,
            "on_step_variables_set",
            "ignore_case_step",
            stepEntry=stepEntry,
            run_id=run_id,
            parent_run_id=self.parent_run_id,
            tags=self.tags,
            **kwargs,
        )

    @classmethod
    def configure(
        cls,
        inheritable_callbacks: Callbacks = None,
        local_callbacks: Callbacks = None,
        verbose: bool = False,
        inheritable_tags: Optional[List[str]] = None,
        local_tags: Optional[List[str]] = None,
        inheritable_metadata: Optional[Dict[str, Any]] = None,
        local_metadata: Optional[Dict[str, Any]] = None,
    ) -> AsyncCaseSteoCallbackManager:
    
        callback_manager = super().configure(
            inheritable_callbacks,
            local_callbacks,
            verbose,
            inheritable_tags,
            local_tags,
            inheritable_metadata,
            local_metadata,
        )

        # add default case step handler
        if get_verbose():
            from caseflow.callbacks.stdout import CaseStepStdOutCallbackHandler
            if not any(
                isinstance(handler, CaseStepStdOutCallbackHandler)
                for handler in callback_manager.handlers
            ):
                callback_manager.add_handler(CaseStepStdOutCallbackHandler())
        return callback_manager

    def get_child(self, tag: Optional[str] = None) -> AsyncCaseSteoCallbackManager:
        """Get a child callback manager.

        Args:
            tag (str, optional): The tag for the child callback manager.
                Defaults to None.

        Returns:
            CallbackManager: The child callback manager.
        """
        manager = AsyncCaseSteoCallbackManager(handlers=[], parent_run_id=self.run_id)
        manager.set_handlers(self.inheritable_handlers)
        manager.add_tags(self.inheritable_tags)
        manager.add_metadata(self.inheritable_metadata)
        if tag is not None:
            manager.add_tags([tag], False)
        return manager