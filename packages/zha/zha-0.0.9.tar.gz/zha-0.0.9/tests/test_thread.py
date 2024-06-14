"""Test ZHA thread utils."""

import asyncio
from unittest.mock import Mock, patch

import pytest

from zha import async_
from zha.application.gateway import Gateway
from zha.async_ import ThreadWithException, run_callback_threadsafe


async def test_thread_with_exception_invalid(zha_gateway: Gateway) -> None:
    """Test throwing an invalid thread exception."""

    finish_event = asyncio.Event()

    def _do_nothing(*_):
        run_callback_threadsafe(zha_gateway.loop, finish_event.set)

    test_thread = ThreadWithException(target=_do_nothing)
    test_thread.start()
    await asyncio.wait_for(finish_event.wait(), timeout=0.1)

    with pytest.raises(TypeError):
        test_thread.raise_exc(_EmptyClass())
    test_thread.join()


async def test_thread_not_started(zha_gateway: Gateway) -> None:
    """Test throwing when the thread is not started."""

    test_thread = ThreadWithException(target=lambda *_: None)

    with pytest.raises(AssertionError):
        test_thread.raise_exc(TimeoutError)


async def test_thread_fails_raise(zha_gateway: Gateway) -> None:
    """Test throwing after already ended."""

    finish_event = asyncio.Event()

    def _do_nothing(*_):
        run_callback_threadsafe(zha_gateway.loop, finish_event.set)

    test_thread = ThreadWithException(target=_do_nothing)
    test_thread.start()
    await asyncio.wait_for(finish_event.wait(), timeout=0.1)
    test_thread.join()

    with pytest.raises(SystemError):
        test_thread.raise_exc(ValueError)


class _EmptyClass:
    """An empty class."""


async def test_deadlock_safe_shutdown_no_threads() -> None:
    """Test we can shutdown without deadlock without any threads to join."""

    dead_thread_mock = Mock(
        join=Mock(), daemon=False, is_alive=Mock(return_value=False)
    )
    daemon_thread_mock = Mock(
        join=Mock(), daemon=True, is_alive=Mock(return_value=True)
    )
    mock_threads = [
        dead_thread_mock,
        daemon_thread_mock,
    ]

    with patch("threading.enumerate", return_value=mock_threads):
        async_.deadlock_safe_shutdown()

    assert not dead_thread_mock.join.called
    assert not daemon_thread_mock.join.called


async def test_deadlock_safe_shutdown() -> None:
    """Test we can shutdown without deadlock."""

    normal_thread_mock = Mock(
        join=Mock(), daemon=False, is_alive=Mock(return_value=True)
    )
    dead_thread_mock = Mock(
        join=Mock(), daemon=False, is_alive=Mock(return_value=False)
    )
    daemon_thread_mock = Mock(
        join=Mock(), daemon=True, is_alive=Mock(return_value=True)
    )
    exception_thread_mock = Mock(
        join=Mock(side_effect=Exception), daemon=False, is_alive=Mock(return_value=True)
    )
    mock_threads = [
        normal_thread_mock,
        dead_thread_mock,
        daemon_thread_mock,
        exception_thread_mock,
    ]

    with patch("threading.enumerate", return_value=mock_threads):
        async_.deadlock_safe_shutdown()

    expected_timeout = async_.THREADING_SHUTDOWN_TIMEOUT / 2

    assert normal_thread_mock.join.call_args[0] == (expected_timeout,)
    assert not dead_thread_mock.join.called
    assert not daemon_thread_mock.join.called
    assert exception_thread_mock.join.call_args[0] == (expected_timeout,)
