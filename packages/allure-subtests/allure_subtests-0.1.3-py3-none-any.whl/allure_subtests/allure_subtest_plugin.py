from __future__ import annotations

import doctest
import sys
import time
import traceback
from contextlib import contextmanager
from contextlib import nullcontext
from typing import Any
from typing import Callable
from typing import ContextManager
from typing import Generator
from typing import Mapping
from typing import TYPE_CHECKING
from unittest import TestCase

import allure
import attr
import pluggy
import pytest
from _pytest._code import ExceptionInfo
from _pytest.capture import CaptureFixture
from _pytest.capture import FDCapture
from _pytest.capture import SysCapture
from _pytest.fixtures import SubRequest
from _pytest.logging import LogCaptureHandler
from _pytest.logging import catching_logs
from _pytest.outcomes import OutcomeException
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from _pytest.runner import check_interactive_exception
from _pytest.unittest import TestCaseFunction
from allure_commons.model2 import TestResult, Status, Label, StatusDetails
from allure_commons.reporter import AllureReporter
from allure_commons.types import LabelType, AttachmentType
from allure_pytest.listener import ItemCache
from loguru import logger

if TYPE_CHECKING:
    from types import TracebackType

    if sys.version_info < (3, 8):
        from typing_extensions import Literal
    else:
        from typing import Literal


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("subtests")
    existing_options = [option.dest for option in group.options]
    if "no_subtests_shortletter" not in existing_options:
        group.addoption(
            "--no-subtests-shortletter",
            action="store_true",
            dest="no_subtests_shortletter",
            default=False,
            help="Disables subtest output 'dots' in non-verbose mode (EXPERIMENTAL)",
        )


@attr.s
class SubTestContext:
    msg: str | None = attr.ib()
    kwargs: dict[str, Any] = attr.ib()


@attr.s(init=False)
class SubTestReport(TestReport):  # type: ignore[misc]
    context: SubTestContext = attr.ib()

    @property
    def head_line(self) -> str:
        _, _, domain = self.location
        return f"{domain} {self.sub_test_description()}"

    def sub_test_description(self) -> str:
        parts = []
        if isinstance(self.context.msg, str):
            parts.append(f"[{self.context.msg}]")
        if self.context.kwargs:
            params_desc = ", ".join(
                f"{k}={v!r}" for (k, v) in sorted(self.context.kwargs.items())
            )
            parts.append(f"({params_desc})")
        return " ".join(parts) or "(<subtest>)"

    def _to_json(self) -> dict:
        data = super()._to_json()
        del data["context"]
        data["_report_type"] = "SubTestReport"
        data["_subtest.context"] = attr.asdict(self.context)
        return data

    @classmethod
    def _from_json(cls, reportdict: dict[str, Any]) -> SubTestReport:
        report = super()._from_json(reportdict)
        context_data = reportdict["_subtest.context"]
        report.context = SubTestContext(
            msg=context_data["msg"], kwargs=context_data["kwargs"]
        )
        return report

    @classmethod
    def _from_test_report(cls, test_report: TestReport) -> SubTestReport:
        try:
            test_report_json = test_report._to_json()
        except:
            test_report_json = {
                'nodeid': test_report.nodeid,
                'location': test_report.location,
                'keywords': test_report.keywords,
                'outcome': test_report.outcome,
                'longrepr': test_report.longreprtext,
                'when': test_report.when,
                'user_properties': test_report.user_properties,
                'sections': test_report.sections,
                'duration': test_report.duration,
            }
        return super()._from_json(test_report_json)


def _addSubTest(
    self: TestCaseFunction,
    test_case: Any,
    test: TestCase,
    exc_info: tuple[type[BaseException], BaseException, TracebackType] | None,
) -> None:
    if exc_info is not None:
        msg = test._message if isinstance(test._message, str) else None  # type: ignore[attr-defined]
        call_info = make_call_info(
            ExceptionInfo(exc_info, _ispytest=True),
            start=0,
            stop=0,
            duration=0,
            when="call",
        )
        report = self.ihook.pytest_runtest_makereport(item=self, call=call_info)
        sub_report = SubTestReport._from_test_report(report)
        sub_report.context = SubTestContext(msg, dict(test.params))  # type: ignore[attr-defined]
        self.ihook.pytest_runtest_logreport(report=sub_report)
        if check_interactive_exception(call_info, sub_report):
            self.ihook.pytest_exception_interact(
                node=self, call=call_info, report=sub_report
            )


def pytest_configure(config: pytest.Config) -> None:
    TestCaseFunction.addSubTest = _addSubTest  # type: ignore[attr-defined]
    TestCaseFunction.failfast = False  # type: ignore[attr-defined]

    # Hack (#86): the terminal does not know about the "subtests"
    # status, so it will by default turn the output to yellow.
    # This forcibly adds the new 'subtests' status.
    import _pytest.terminal

    new_types = tuple(
        f"subtests {outcome}" for outcome in ("passed", "failed", "skipped")
    )
    # We need to check if we are not re-adding because we run our own tests
    # with pytester in-process mode, so this will be called multiple times.
    if new_types[0] not in _pytest.terminal.KNOWN_TYPES:
        _pytest.terminal.KNOWN_TYPES = _pytest.terminal.KNOWN_TYPES + new_types  # type: ignore[assignment]

    _pytest.terminal._color_for_type.update(
        {
            f"subtests {outcome}": _pytest.terminal._color_for_type[outcome]
            for outcome in ("passed", "failed", "skipped")
            if outcome in _pytest.terminal._color_for_type
        }
    )


def pytest_unconfigure() -> None:
    if hasattr(TestCaseFunction, "addSubTest"):
        del TestCaseFunction.addSubTest
    if hasattr(TestCaseFunction, "failfast"):
        del TestCaseFunction.failfast


@pytest.fixture
def allure_subtests(request: SubRequest) -> Generator[AllureSubTests, None, None]:
    capmam = request.node.config.pluginmanager.get_plugin("capturemanager")
    if capmam is not None:
        suspend_capture_ctx = capmam.global_and_fixture_disabled
    else:
        suspend_capture_ctx = nullcontext

    try:
        from pytest_check import check
        pytest_enabled = True
    except:
        pytest_enabled = False

    yield AllureSubTests(request.node.ihook, suspend_capture_ctx, request, pytest_enabled)


def now():
    return int(round(1000 * time.time()))


def _exception_brokes_test(exception):
    return not type(exception) in (
        AssertionError,
        pytest.fail.Exception,
        doctest.DocTestFailure
    )

@attr.s
class AllureSubTests:
    ihook: pluggy.HookRelay = attr.ib()
    suspend_capture_ctx: Callable[[], ContextManager] = attr.ib()
    request: SubRequest = attr.ib()
    pytest_enabled: bool = attr.ib()

    _cache = ItemCache()
    allure_logger = AllureReporter()

    def add_label(self, label_type, labels):
        test_result = self.allure_logger.get_test(None)
        for label in labels if test_result else ():
            test_result.labels.append(Label(label_type, label))


    @property
    def item(self) -> pytest.Item:
        return self.request.node

    @contextmanager
    def _capturing_output(self) -> Generator[Captured, None, None]:
        option = self.request.config.getoption("capture", None)

        # capsys or capfd are active, subtest should not capture

        capman = self.request.config.pluginmanager.getplugin("capturemanager")
        capture_fixture_active = getattr(capman, "_capture_fixture", None)

        if option == "sys" and not capture_fixture_active:
            with ignore_pytest_private_warning():
                fixture = CaptureFixture(SysCapture, self.request)
        elif option == "fd" and not capture_fixture_active:
            with ignore_pytest_private_warning():
                fixture = CaptureFixture(FDCapture, self.request)
        else:
            fixture = None

        if fixture is not None:
            fixture._start()

        captured = Captured()
        try:
            yield captured
        finally:
            if fixture is not None:
                out, err = fixture.readouterr()
                fixture.close()
                captured.out = out
                captured.err = err

    @contextmanager
    def _capturing_logs(self) -> Generator[CapturedLogs | NullCapturedLogs, None, None]:
        logging_plugin = self.request.config.pluginmanager.getplugin("logging-plugin")
        if logging_plugin is None:
            yield NullCapturedLogs()
        else:
            handler = LogCaptureHandler()
            handler.setFormatter(logging_plugin.formatter)

            captured_logs = CapturedLogs(handler)
            with catching_logs(handler):
                yield captured_logs

    @contextmanager
    def test(
        self,
        subtest_name: str | None = None,
        **kwargs: Any,
    ) -> Generator[None, None, None]:
        start = time.time()
        precise_start = time.perf_counter()
        exc_info = None

        with self._capturing_output() as captured_output, self._capturing_logs() as captured_logs:
            stack_trace_str = ''

            case_uuid = self._cache.push(subtest_name)
            logger.info(f'subtest {case_uuid=}')
            test_result = TestResult(name=subtest_name, uuid=case_uuid, start=now(), stop=now())
            self.allure_logger.schedule_test(case_uuid, test_result)
            # self.item._nodeid = msg

            self.add_label(LabelType.SUB_SUITE, [self.item.name])
            self.add_label(LabelType.SUITE, [self.item.parent.name])

            if self.item.parent.parent:
                parent_suite_name = self.item.parent.parent.name
            else:
                parent_suite_name = self.item.module.__name__
            self.add_label(LabelType.PARENT_SUITE, [parent_suite_name])

            try:
                yield self
            except (Exception, OutcomeException):
                exc_info = ExceptionInfo.from_current()
                exc_type, exc_value, exc_traceback = sys.exc_info()
                stack_trace_list = traceback.extract_tb(exc_traceback)
                filtered_stack_trace = stack_trace_list[1:]
                stack_trace_str = ''.join(traceback.format_list(filtered_stack_trace))

            log_list = [record.getMessage() for record in captured_logs._handler.records]
            if log_list:
                log_txt = '\n'.join(log_list)
                allure.attach(log_txt, name='log', attachment_type=AttachmentType.TEXT, extension=None)

            self.update_subtest_status(exc_info, subtest_name, stack_trace_str)

        precise_stop = time.perf_counter()
        duration = precise_stop - precise_start
        stop = time.time()

        call_info = make_call_info(
            exc_info, start=start, stop=stop, duration=duration, when="call"
        )
        report = self.ihook.pytest_runtest_makereport(item=self.item, call=call_info)

        # self.update_subtest_status(exc_info, subtest_name, stack_trace_str, call_info)

        sub_report = SubTestReport._from_test_report(report)
        sub_report.context = SubTestContext(subtest_name, kwargs.copy())

        sub_report.nodeid = subtest_name
        captured_output.update_report(sub_report)
        captured_logs.update_report(sub_report)

        with self.suspend_capture_ctx():
            self.ihook.pytest_runtest_logreport(report=sub_report)

        if check_interactive_exception(call_info, sub_report):
            self.ihook.pytest_exception_interact(
                node=self.item, call=call_info, report=sub_report
            )

    def update_subtest_status(self, exc_info, msg, stack_trace_str, call_info=None):
        uuid = self._cache.pop(msg)
        if not uuid:
            return

        test_result = self.allure_logger.get_test(uuid)
        if not test_result:
            return

        # if sub_report.longreprtext != '':
        #     test_result.status = Status.FAILED
        #     test_result.statusDetails = sub_report.longreprtext
        if exc_info is not None and _exception_brokes_test(exc_info.value):
            test_result.status = Status.BROKEN
        elif exc_info is not None:
            test_result.status = Status.FAILED
        elif call_info is not None and call_info.excinfo is not None:
            test_result.status = Status.FAILED
            test_result.statusDetails = call_info.excinfo.exconly()
        else:
            test_result.status = Status.PASSED

        if exc_info is not None:
            message = exc_info.exconly()
            status_details = StatusDetails(message=message, trace=stack_trace_str)
            test_result.statusDetails = status_details

        if self.pytest_enabled:
            import pytest_check
            failures = pytest_check.check_log.get_failures()
            if failures:
                test_result.status = Status.FAILED
                if failures and len(failures) >= 1:
                    failure_lines = failures[0].split("\n")
                    message = failure_lines[0]
                else:
                    message = 'AssertionError'
                status_details = StatusDetails(message=message, trace="\n".join(failures))
                test_result.statusDetails = status_details

        self.allure_logger.close_test(uuid)


def make_call_info(
    exc_info: ExceptionInfo[BaseException] | None,
    *,
    start: float,
    stop: float,
    duration: float,
    when: Literal["collect", "setup", "call", "teardown"],
) -> CallInfo:
    return CallInfo(
        None,
        exc_info,
        start=start,
        stop=stop,
        duration=duration,
        when=when,
        _ispytest=True,
    )


@contextmanager
def ignore_pytest_private_warning() -> Generator[None, None, None]:
    import warnings

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            "A private pytest class or function was used.",
            category=pytest.PytestDeprecationWarning,
        )
        yield


@attr.s
class Captured:
    out = attr.ib(default="", type=str)
    err = attr.ib(default="", type=str)

    def update_report(self, report: pytest.TestReport) -> None:
        if self.out:
            report.sections.append(("Captured stdout call", self.out))
        if self.err:
            report.sections.append(("Captured stderr call", self.err))


class CapturedLogs:
    def __init__(self, handler: LogCaptureHandler) -> None:
        self._handler = handler

    def update_report(self, report: pytest.TestReport) -> None:
        report.sections.append(("Captured log call", self._handler.stream.getvalue()))


class NullCapturedLogs:
    def update_report(self, report: pytest.TestReport) -> None:
        pass


def pytest_report_to_serializable(report: pytest.TestReport) -> dict[str, Any] | None:
    if isinstance(report, SubTestReport):
        return report._to_json()
    return None


def pytest_report_from_serializable(data: dict[str, Any]) -> SubTestReport | None:
    if data.get("_report_type") == "SubTestReport":
        return SubTestReport._from_json(data)
    return None


@pytest.hookimpl(tryfirst=True)
def pytest_report_teststatus(
    report: pytest.TestReport,
    config: pytest.Config,
) -> tuple[str, str, str | Mapping[str, bool]] | None:
    if report.when != "call" or not isinstance(report, SubTestReport):
        return None

    if hasattr(report, "wasxfail"):
        return None

    outcome = report.outcome
    description = report.sub_test_description()
    if report.passed:
        short = "" if config.option.no_subtests_shortletter else ","
        return f"subtests {outcome}", short, f"{description} SUBPASS"
    elif report.skipped:
        short = "" if config.option.no_subtests_shortletter else "-"
        return outcome, short, f"{description} SUBSKIP"
    elif outcome == "failed":
        short = "" if config.option.no_subtests_shortletter else "u"
        return outcome, short, f"{description} SUBFAIL"

    return None
