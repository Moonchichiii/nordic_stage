from typing import Any

import structlog
from celery import Task, shared_task

logger = structlog.get_logger(__name__)


class BaseTask(Task):  # type: ignore[misc]
    """
    Base Celery task providing standardized logging and error handling.
    """

    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = True

    def on_failure(
        self,
        exc: Exception,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        einfo: Any,
    ) -> None:
        logger.error(
            "task_failed",
            task_name=self.name,
            task_id=task_id,
            exc_info=exc,
        )
        super().on_failure(exc, task_id, args, kwargs, einfo)

    def on_success(
        self,
        retval: Any,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> None:
        logger.info(
            "task_succeeded",
            task_name=self.name,
            task_id=task_id,
        )
        super().on_success(retval, task_id, args, kwargs)


@shared_task(base=BaseTask, name="core.tasks.debug_task")  # type: ignore[untyped-decorator]
def debug_task() -> str:
    """A simple task for checking if workers are running."""
    logger.info("executing_debug_task")
    return "pong"


@shared_task(base=BaseTask, name="core.tasks.send_email_task")  # type: ignore[untyped-decorator]
def send_email_task(recipient: str, subject: str, body: str) -> bool:
    """Placeholder for an asynchronous email task."""
    logger.info(
        "executing_send_email_task",
        recipient=recipient,
        subject=subject,
    )
    # Placeholder logic
    return True
