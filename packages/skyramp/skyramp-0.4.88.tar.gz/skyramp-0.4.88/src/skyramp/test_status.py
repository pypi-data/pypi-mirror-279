"""
TestStatus module
"""

from typing import List, Dict
import json
from abc import ABC


class TesterStatusType:
    """
    TesterStatusType object
    """

    Idle = "idle"
    Initializing = "initializing"
    Waiting = "waiting"
    Running = "running"
    Failed = "failed"
    Skipped = "skipped"
    Stopping = "stopping"
    Stopped = "stopped"
    Finished = "finished"


class TestResultType:
    """
    TestResultType object
    """

    NoneType = ""
    Command = "command"
    Request = "request"
    Scenario = "scenario"
    Load = "load"
    Repeat = "repeat"
    Assert = "assert"
    With = "with"


class TestTimeseriesStat:
    """
    TestTimeseriesStat object
    """

    timestamp: str = ""
    error_rate: str = ""
    rps: str = ""
    avg_latency: str = ""

    def __init__(self, options: dict):
        if "timestamp" in options:
            self.timestamp = options["timestamp"]
        if "errorRate" in options:
            self.error_rate = options["errorRate"]
        if "RPS" in options:
            self.rps = options["RPS"]
        if "avgLatency" in options:
            self.avg_latency = options["avgLatency"]

    def __repr__(self):
        _data = {
            "timestamp": self.timestamp,
            "error_rate": self.error_rate,
            "rps": self.rps,
            "avg_latency": self.avg_latency,
        }
        filtered_data = {k: v for k, v in _data.items() if v is not None and v != ""}
        return f"TestTimeseriesStat({json.dumps(filtered_data, indent=2)})"


class TestStat:
    """
    TestStat object
    """

    description: str = ""
    count: int = 0
    executed: int = 0
    fail: int = 0
    avg_latency: str = ""
    max_latency: str = ""
    min_latency: str = ""
    l99th_latency: str = ""
    l95th_latency: str = ""
    l90th_latency: str = ""
    code_table: dict = None
    log_table: dict = None

    def __init__(self, options: dict):
        if "Description" in options:
            self.description = options["Description"]
        if "Count" in options:
            self.count = options["Count"]
        if "Executed" in options:
            self.executed = options["Executed"]
        if "Fail" in options:
            self.fail = options["Fail"]
        if "AvgLatency" in options:
            self.avg_latency = options["AvgLatency"]
        if "MaxLatency" in options:
            self.max_latency = options["MaxLatency"]
        if "MinLatency" in options:
            self.min_latency = options["MinLatency"]
        if "L99thLatency" in options:
            self.l99th_latency = options["L99thLatency"]
        if "L95thLatency" in options:
            self.l95th_latency = options["L95thLatency"]
        if "L90thLatency" in options:
            self.l90th_latency = options["L90thLatency"]
        if "CodeTable" in options:
            self.code_table = options["CodeTable"]
        if "LogTable" in options:
            self.log_table = options["LogTable"]

    def __repr__(self):
        _data = {
            "description": self.description,
            "count": self.count,
            "executed": self.executed,
            "fail": self.fail,
            "avg_latency": self.avg_latency,
            "max_latency": self.max_latency,
            "min_latency": self.min_latency,
            "l99th_latency": self.l99th_latency,
            "l95th_latency": self.l95th_latency,
            "l90th_latency": self.l90th_latency,
            "code_table": self.code_table,
            "log_table": self.log_table,
        }
        filtered_data = {k: v for k, v in _data.items() if v is not None and v != ""}
        return f"TestStat({json.dumps(filtered_data, indent=2)})"


class RequestLog:
    """
    RequestLog object
    """

    path: str = ""
    method: str = ""
    headers: dict = {}
    cookies: dict = {}
    payload: str = ""
    test_group_id: str = ""

    def __init__(self, options: dict):
        for key in ["path", "method", "headers", "cookies", "payload"]:
            if key in options:
                setattr(self, key, options[key])

    def __repr__(self):
        _data = {
            "path": self.path,
            "method": self.method,
            "headers": self.headers,
            "cookies": self.cookies,
            "payload": self.payload,
            "test_group_id": self.test_group_id,
        }
        filtered_data = {k: v for k, v in _data.items() if v is not None and v != ""}
        return f"RequestLog({json.dumps(filtered_data, indent=2)})"


class TesterState:
    """
    TesterState object
    """

    vars: dict = {}
    scenario_vars: dict = {}
    exports: dict = {}
    blob_overrides: dict = {}

    def __init__(self, options: dict):
        if "vars" in options:
            self.vars = options["vars"]
        if "scenarioVars" in options:
            self.scenario_vars = options["scenarioVars"]
        if "exports" in options:
            self.exports = options["exports"]
        if "blobOverrides" in options:
            self.blob_overrides = options["blobOverrides"]

    def __repr__(self):
        _data = {
            "vars": self.vars,
            "scenario_vars": self.scenario_vars,
            "exports": self.exports,
            "blob_overrides": self.blob_overrides,
        }
        filtered_data = {k: v for k, v in _data.items() if v is not None and v != ""}
        return f"TesterState({json.dumps(filtered_data, indent=2)})"


class ResponseLog:
    """
    ResponseLog object
    """

    status_code: int = 0
    headers: dict = {}
    cookies: dict = {}
    payload: str = ""

    def __init__(self, options: dict):
        if "statusCode" in options:
            self.status_code = options["statusCode"]
        if "headers" in options:
            self.headers = options["headers"]
        if "cookies" in options:
            self.cookies = options["cookies"]
        if "payload" in options:
            self.payload = options["payload"]

    def get_payload(self, key):
        """
        Returns the payload value for the given key
        """
        if key is None:
            return json.loads(self.payload)
        keys = key.split(".")
        value = json.loads(self.payload)
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, None)
            else:
                return None
        return value

    def __repr__(self):
        _data = {
            "status_code": self.status_code,
            "headers": self.headers,
            "cookies": self.cookies,
            "payload": self.payload,
        }
        filtered_data = {k: v for k, v in _data.items() if v is not None and v != ""}
        return f"ResponseLog({json.dumps(filtered_data, indent=2)})"


class TestResult:
    """
    TestResult object
    """

    name: str = ""
    status: str = ""
    description: str = ""
    nested_info: str = ""
    step_description: str = ""
    step_name: str = ""
    parent: str = ""
    executed: bool = None
    error: str = ""
    input: RequestLog = None
    output: ResponseLog = None
    type: TestResultType = ""
    begin: int = None
    end: int = None
    duration: int = None
    timeseries: List[TestTimeseriesStat] = None
    stat: TestStat = None
    state: TesterState = None
    test_case_status: json = "[]"
    test_case_name: str = ""

    # pylint: disable=too-many-branches
    def __init__(self, options: dict):
        if "name" in options:
            self.name = options["name"]
        if "status" in options:
            self.status = options["status"]
        if "description" in options:
            self.description = options["description"]
        if "nestedInfo" in options:
            self.nested_info = options["nestedInfo"]
        if "stepDescription" in options:
            self.step_description = options["stepDescription"]
        if "stepName" in options:
            self.step_name = options["stepName"]
        if "parent" in options:
            self.parent = options["parent"]
        if "executed" in options:
            self.executed = options["executed"]
        if "error" in options:
            self.error = options["error"]
        if "input" in options:
            if options["input"] is not None and "service" in options["input"]:
                options["input"]["service"] = None
            self.input = options["input"]
        if "output" in options:
            self.output = options["output"]
        if "type" in options:
            self.type = options["type"]
        if "begin" in options:
            self.begin = options["begin"]
        if "end" in options:
            self.end = options["end"]
        if "duration" in options and options["duration"] != 0:
            self.duration = options["duration"]
        if "timeseries" in options and options["timeseries"] != []:
            self.timeseries = options["timeseries"]
        if "stat" in options:
            self.stat = options["stat"]
        if "state" in options:
            self.state = options["state"]

    def __str__(self):
        _data = {
            "name": self.name,
        }
        if self.status:
            _data["status"] = self.status
        if self.description:
            _data["description"] = self.description
        if self.step_description:
            _data["step_description"] = self.step_description
        if self.step_name:
            _data["step_name"] = self.step_name
        if self.error:
            _data["error"] = self.error
        return f"TestResult({json.dumps(_data, indent=2)})"

    def __repr__(self):
        _data = {
            "name": self.name,
            "status": self.status,
            "description": self.description,
            "nested_info": self.nested_info,
            "step_description": self.step_description,
            "step_name": self.step_name,
            "parent": self.parent,
            "executed": self.executed,
            "error": self.error,
            "request": self.input,
            "response": self.output,
            "type": self.type,
            "begin": self.begin,
            "end": self.end,
            "duration": self.duration,
            "timeseries": self.timeseries,
            "stat": self.stat,
            "state": self.state,
            "test_case_status": self.test_case_status,
        }
        _data["test_case_status"] = None
        filtered_data = {k: v for k, v in _data.items() if v is not None and v != ""}
        return f"TestResult({json.dumps(filtered_data, indent=2)})"

    def to_html(self):
        """
        Returns HTML text representation of the test status
        """
        html_content = "<div>\n"
        html_content += _html_entry("Step Name", self.name)
        html_content += _html_entry("Step Description", self.step_description)
        if self.error:
            html_content += _html_entry("Error", self.error)
        if self.input:
            html_content += _html_entry("Request", json.dumps(self.input, indent=2))
        if self.output:
            html_content += _html_entry("Response", json.dumps(self.output, indent=2))
        if self.stat:
            html_content += _html_entry("Stat", self.stat)
        if self.state:
            html_content += _html_entry("State", json.dumps(self.state, indent=2))
        if self.timeseries:
            html_content += _html_entry("Timeseries", self.timeseries)
        if self.duration:
            html_content += _html_entry("Duration", self.duration)
        if self.type:
            html_content += _html_entry("Type", self.type)
        if self.begin:
            html_content += _html_entry("Begin", self.begin)
        if self.end:
            html_content += _html_entry("End", self.end)
        html_content += _html_entry("Status", self.status)
        html_content += "</div>\n\n"
        return html_content


def _filtered(data: dict):
    return {k: v for k, v in data.items() if v is not None and v != ""}


def _html_entry(title, data):
    return f"<span><strong>{title}:</strong> {data}</span>\n"


class TestStatus(ABC):
    """
    TestStatus object
    """

    test_results: List[List[TestResult]] = []
    pass_status: bool = True
    index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.test_results):
            result = self.test_results[self.index]
            self.index += 1
            return result
        raise StopIteration

    def __getitem__(self, index):
        return self.test_results[index]

    def __len__(self):
        return len(self.test_results)

    def passed(self):
        """
        Returns True if all the tests passed
        """
        return self.pass_status

    def failed(self):
        """
        Returns True if any of the tests failed
        """
        failed_json = []
        for result in self.test_results:
            for step in result:
                if step.status == TesterStatusType.Failed and step.error != "":
                    failed_json.append(
                        {
                            "name": step.name,
                            "step_description": step.step_description,
                            "request": step.input,
                            "response": step.output,
                            "status": step.status,
                            "error": step.error,
                        }
                    )
        return json.dumps(failed_json, indent=2)


class TestStatusV1(TestStatus):
    """
    TestStatusV1 object
    """

    def __init__(self, options: dict):
        self.test_results = []
        results = options.get("test_results", [])
        # iterate over the results and create TestResult objects
        if len(results) > 0 and "results" in results and len(results["results"]) > 0:
            for test_result in results["results"][1:]:
                result = TestResult(test_result)
                result_list = []
                # if the result is an assert, add it to the previous result
                if result.name == "assert":
                    result_list = self.test_results.pop()
                # merge all the repeat request into one test case
                if (
                    ".repeat." in result.description
                    and ".repeat.0" not in result.description
                ):
                    result_list = self.test_results.pop()

                # if first result in the result_list update the test case name, status and error
                if len(result_list) == 0:
                    result.test_case_name = result.step_name
                    if result.step_name == "":
                        result.test_case_name = result.name
                # add the result to the result_list
                result_list.append(result)

                if result.error != "":
                    self.pass_status = False
                    data = json.loads(result_list[0].test_case_status)
                    data.append(result.error)
                    result_list[0].test_case_status = json.dumps(data)
                # update the test_results list
                self.test_results.append(result_list)

    def __repr__(self):
        return f"TestStatusV1(test_results={self.test_results})"


class TestStatusV2(TestStatus):
    """
    TestStatusV2 object
    """

    def __init__(self, options: dict):
        self.test_results = []
        results = options.get("test_results", [])
        for result in results:
            scenario_data = []
            for step in result:
                test_result = TestResult(step)
                if test_result.error != "":
                    self.pass_status = False
                scenario_data.append(test_result)
            self.test_results.append(scenario_data)

    def __repr__(self):
        return f"TestStatusV2(test_results={self.test_results})"


class ScenarioStatus:
    """
    ScenarioStatus object
    """

    overall_status: TestResult = {}
    request_list: List[TestResult] = []
    child_scenarios: List[TestResult] = {}

    def get_request_status(self, request_name):
        """
        Returns the request status for the given request name
        """
        for req in self.request_list:
            if req.name == request_name:
                return req
        return None

    def get_child_scenario_status(self, scenario_name):
        """
        Returns the child scenario status for the given scenario name
        """
        for val in self.child_scenarios:
            if val.name == scenario_name:
                return val
        return None

    def __repr__(self):
        return (
            "ScenarioStatus("
            f"overall_status='{self.overall_status}',"
            f"request_status='{self.request_list}',"
            f"child_scenarios= '{self.child_scenarios}' )"
        )


class TestStatusV3:
    """
    TestStatusV3 object
    """

    scenario_dict: Dict[str, TestResult] = {}
    request_dict: Dict[str, Dict[str, TestResult]] = {}
    child_scenarios_dict: Dict[str, Dict[str, TestResult]] = {}

    # pylint: disable=too-many-locals
    def __init__(self, options: dict):
        results = options.test_results
        for res in results:
            for result in res:
                result_type = result.type
                nested_info = result.nested_info
                parent = result.parent
                # if the result is a scenario, add it to the scenario_dict
                if result_type == TestResultType.Scenario:
                    # get the scenario name
                    path_list = result.description.split(".")
                    scenario_name = path_list[-1]
                    result.name = scenario_name
                    result.description = None
                    if parent == "":
                        self.scenario_dict[nested_info] = result
                    else:
                        self.scenario_dict[nested_info] = result
                        if parent not in self.scenario_dict:
                            self.scenario_dict[parent] = {}
                        if self.child_scenarios_dict.get(parent) is None:
                            self.child_scenarios_dict[parent] = {}
                        self.child_scenarios_dict[parent][nested_info] = result
                elif result_type == TestResultType.Request:
                    if self.request_dict.get(parent) is None:
                        self.request_dict[parent] = {}
                    self.request_dict[parent][nested_info] = result

    def get_scenario_status(self, scenario_name) -> ScenarioStatus:
        """
        Returns the scenario status for the given scenario name
        """
        for val in self.scenario_dict.values():
            if val.name == scenario_name:
                scenario_status = ScenarioStatus()
                scenario_status.overall_status = val

                # get the request status for the scenario
                req_list = self.request_dict.get(val.nested_info, {})
                request_list = []
                for value in req_list.values():
                    request_list.append(
                        TestResult(
                            options={
                                "name": value.name,
                                "input": value.input,
                                "output": value.output,
                            }
                        )
                    )
                scenario_status.request_list = request_list

                # get the child scenario status for the scenario
                child_scenarios = self.child_scenarios_dict.get(val.nested_info, {})
                child_scenario_list = []
                for value in child_scenarios.values():
                    child_scenario_list.append(
                        TestResult(
                            options={
                                "name": value.name,
                                "status": value.status,
                                "error": value.error,
                            }
                        )
                    )
                    if value.error != "":
                        if scenario_status.overall_status.error == "":
                            scenario_status.overall_status.error = (
                                "'" + value.error + "'"
                            )
                        else:
                            scenario_status.overall_status.error += (
                                ", '" + value.error + "'"
                            )

                scenario_status.child_scenarios = child_scenario_list
                return scenario_status
        return None

    def __repr__(self):
        return "TestStatusV3(" f"scenarios='{self.scenario_dict.values()}' )"
