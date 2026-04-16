import structlog

from core.tasks import BaseTask, debug_task, send_email_task


def test_debug_task() -> None:
    assert debug_task() == "pong"


def test_send_email_task() -> None:
    result = send_email_task("test@example.com", "Hello", "This is a test body")
    assert result is True


def test_basetask_on_failure() -> None:
    task = BaseTask()
    task.name = "test_task"

    with structlog.testing.capture_logs() as cap_logs:
        task.on_failure(Exception("Test error"), "123", (), {}, None)

    assert len(cap_logs) == 1
    assert cap_logs[0]["event"] == "task_failed"
    assert cap_logs[0]["task_name"] == "test_task"


def test_basetask_on_success() -> None:
    task = BaseTask()
    task.name = "test_task"

    with structlog.testing.capture_logs() as cap_logs:
        task.on_success("retval", "123", (), {})

    assert len(cap_logs) == 1
    assert cap_logs[0]["event"] == "task_succeeded"
    assert cap_logs[0]["task_name"] == "test_task"
