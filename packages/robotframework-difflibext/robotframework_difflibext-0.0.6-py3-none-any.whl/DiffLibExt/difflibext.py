import os
import re
import time
import json
import difflib
from pathlib import Path
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from dataclasses import asdict, is_dataclass


class JSONEncoderExt(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        elif hasattr(o, "__dict__"):
            return o.__dict__
        return json.JSONEncoder.default(self, o)


class DiffLibExt:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
    DIFF_OUT_DIR_NAME = "__diff__"

    def __init__(self, line_wrap_len: int = 100):
        self.line_wrap_len = line_wrap_len
        self._builtin_lib = BuiltIn()

    @keyword
    def file_should_be_equal(self, expected_file_path: str, actual_file_path: str):
        try:
            expected_file_text = Path(expected_file_path).read_text(encoding="utf8")
        except UnicodeDecodeError as e:
            raise AssertionError(f"{expected_file_path} is not a text file.") from e

        try:
            actual_file_text = Path(actual_file_path).read_text(encoding="utf8")
        except UnicodeDecodeError as e:
            raise AssertionError(f"{actual_file_path} is not a text file.") from e

        if expected_file_text != actual_file_text:
            self._report_diff(expected_file_text, actual_file_text)

    def _report_diff(self, expected_text: str, actual_text: str):
        html_diff = difflib.HtmlDiff(wrapcolumn=self.line_wrap_len).make_file(
            expected_text.splitlines(),
            actual_text.splitlines(),
            fromdesc="Expected:",
            todesc="Actual:",
        )
        output_dir = self._builtin_lib.get_variable_value("${OUTPUT DIR}")
        pabot_out_regex = r".*(\\|\/)(pabot_results(\\|\/)\d+$)"
        matcher = re.match(pabot_out_regex, output_dir)
        path_suffix = None
        if matcher is not None:
            path_suffix = matcher.group(2)
        diff_html_name = f"diff_{time.time_ns()}.html"
        diff_out_dir = os.path.join(output_dir, self.DIFF_OUT_DIR_NAME)
        os.makedirs(diff_out_dir, exist_ok=True)
        output_diff_html = os.path.join(diff_out_dir, diff_html_name)
        output_diff_rel_path = os.path.join(self.DIFF_OUT_DIR_NAME, diff_html_name)
        if path_suffix:
            output_diff_rel_path = os.path.join(path_suffix, output_diff_rel_path)
        Path(output_diff_html).write_text(html_diff, encoding="utf8")
        error_msg = (
            f"*HTML* <b><a href='{output_diff_rel_path}'>Differences Found</a></b>"
        )
        self._builtin_lib.fail(error_msg)

    @keyword
    def text_should_be_equal(self, expected_text: str, actual_text: str):
        if expected_text != actual_text:
            self._report_diff(expected_text, actual_text)

    @keyword
    def object_should_be_equal(self, expected_obj, actual_obj):
        if expected_obj != actual_obj:
            expected_json_text = json.dumps(expected_obj, indent=2, cls=JSONEncoderExt)
            actual_json_text = json.dumps(actual_obj, indent=2, cls=JSONEncoderExt)
            self._report_diff(expected_json_text, actual_json_text)
