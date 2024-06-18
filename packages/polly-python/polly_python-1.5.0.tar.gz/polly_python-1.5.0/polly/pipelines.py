from datetime import datetime

from polly import helpers
from polly import constants as const
from polly.auth import Polly
from polly.help import example
from polly.errors import wrongParamException, error_handler
from polly.tracking import Track


def _add_arguments_to_url(
    url: str,
    run_id: str = None,
    org_id: str = None,
    status: str = None,
    priority: str = None,
    user_id: str = None,
    page_size: int = None,
    page_after: int = None,
):
    """
    This function is used to add query parameters to a provided URL, if provided.
    These query parameters are: run_id, org_id, user_id, page_size, page_after
    Args:
        url (str): The URL in which the query parameters are to be added.
        run_id (str): add run_id to the query parameter
        org_id (str): add org_id to the query parameter
        user_id (str): add user_id to the query parameter
        page_size (str): add page_size to the query parameter
        page_after (str): add page_after to the query parameter

    Returns:
        Returns a string, which is the URL with added query parameters.

    """
    if (
        run_id is not None
        or org_id is not None
        or status is not None
        or priority is not None
        or user_id is not None
        or page_size is not None
        or page_after is not None
    ):
        url = f"{url}?"
        if run_id is not None:
            url = f"{url}filter[run_id]={run_id}&"

        if org_id is not None:
            url = f"{url}filter[org_id]={org_id}&"

        if status is not None:
            url = f"{url}filter[status]={status}&"

        if priority is not None:
            url = f"{url}filter[priority]={priority}&"

        if user_id is not None:
            url = f"{url}filter[user_id]={user_id}&"

        if page_size is not None:
            url = f"{url}page[size]={page_size}&"

        if page_after is not None:
            url = f"{url}filter[after]={page_after}"

    return url


def _generate_run_name():
    return "Run at {:%B-%d-%Y} - {:%H:%M}".format(datetime.now(), datetime.now())


def _generate_job_name():
    return "Job created on {:%B-%d-%Y} at {:%H:%M}".format(
        datetime.now(), datetime.now()
    )


def _filter_response(data: dict):
    if type(data) is list:
        return [_filter_response(item) for item in data]

    if "attributes" in data.keys():
        attributes = data.get("attributes")
        if data.get("type") == "pipelines":
            attributes.pop("parameter_schema", None)

        if data.get("type") == "runs":
            attributes.pop("notification_channels")

        if data.get("type") == "jobs":
            attributes = data.get("attributes")

        data["attributes"] = attributes

    if "links" in data.keys():
        data.pop("links")

    return data


class Pipelines:
    """
    Pipeline class enables users to interact with the functional properties of the Pipelines infrastructure \
    such as create, read or delete pipelines. It can also be used for creating pipeline runs and jobs. \

    Args:
        token (str): token copy from polly.
    Usage:
        from polly.pipelines import Pipeline

        pipeline = Pipeline(token)
    """

    example = classmethod(example)

    def __init__(self, token=None, env="", default_env="polly"):
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://apis.{self.session.env}.elucidata.io"
        self.orchestration_url = f"{self.base_url}/pravaah/orchestration"
        self.monitoring_url = f"{self.base_url}/pravaah/monitoring"

    @Track.track_decorator
    def get_pipelines(self):
        """
        This function returns all the pipelines that the user have access to
        Please use this function with default values for the paramters.\n
        Args:
            None

        Returns:
            It will return a list of JSON objects. (See Examples)
        """
        all_pipelines = []
        default_page_size = 20
        start_url = f"{self.orchestration_url}/pipelines"
        start_url = _add_arguments_to_url(start_url, page_size=default_page_size)
        response = self.session.get(start_url)
        error_handler(response)
        pipelines = response.json().get("data")
        all_pipelines = all_pipelines + pipelines
        next_link = response.json().get("links", {}).get("next")

        while next_link is not None:
            next_endpoint = f"{self.base_url}{next_link}"
            response = self.session.get(next_endpoint)
            error_handler(response)
            response.raise_for_status()
            response_json = response.json()
            all_pipelines = all_pipelines + response_json.get("data")
            next_link = response_json.get("links").get("next")

        data = [_filter_response(pipeline) for pipeline in all_pipelines]
        return data

    @Track.track_decorator
    def get_pipeline(self, pipeline_id: str):
        """
        This function returns the pipeline data of the provided pipeline_id. \n
        Args:
            pipeline_id (str): pipeline_id for required pipeline

        Returns:
            It will return a JSON object with pipeline data. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """

        if pipeline_id is None:
            raise wrongParamException("pipeline_id can not be None")

        if not isinstance(pipeline_id, str):
            raise wrongParamException("pipeline_id should be a string")

        url = f"{self.orchestration_url}/pipelines/{pipeline_id}"
        response = self.session.get(url)
        error_handler(response)
        data = response.json().get("data")
        return _filter_response(data)

    @Track.track_decorator
    def create_run(
        self,
        pipeline_id: str,
        run_name: str = None,
        priority: str = "low",
        tags: dict = {},
        domain_context: dict = {},
    ):
        """
        This function is used to create a Pipeline run.\n
        A run is a collection of jobs, this functions creates an empty run in which the jobs can be added.

        Args:
            pipeline_id (str): pipeline_id for which the run is to be created
            run_name (str): name of the run
            priority (str): priority of the run, can be low | medium | high
            tags (dict): a dict of key-value pair with tag_name -> tag_value mapping
            domain_context (dict): domain context for a run

        Returns:
            It will return a JSON object which is the pipeline run. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        if run_name is None:
            run_name = _generate_run_name()

        if priority not in ["low", "medium", "high"]:
            raise wrongParamException(
                "A run priority can be only one of these values: low | medium | high"
            )

        run_object = {
            "data": {
                "type": "runs",
                "attributes": {
                    "name": run_name,
                    "priority": priority,
                    "domain_context": domain_context,
                    "tags": tags,
                    "pipeline_id": pipeline_id,
                },
            }
        }

        run_url = f"{self.orchestration_url}/runs"
        run = self.session.post(run_url, json=run_object)
        error_handler(run)
        data = run.json().get("data")
        return _filter_response(data)

    @Track.track_decorator
    def submit_job(
        self, run_id: str, parameters: dict, config: dict, job_name: str = None
    ):
        """
        This function is used for creating jobs for a particular run.
        Args:
            run_id (str): run_id in which the job is to be created.
            parameters (dict): a key-value object of all the required parameters of pipeline
            config (dict): config definition for the pipeline job. should be of format \
                            {"infra":  {"cpu": int, "memory": int, "storage": int}}
            job_name (str, Optional): name of the job, auto-generated if not assigned

        Returns:
            It will return a JSON object with pipeline data. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        if parameters is None or config is None:
            raise wrongParamException("The provided arguments can not be of NoneType")

        if job_name is None:
            job_name = _generate_job_name()

        job = {
            "type": "jobs",
            "attributes": {
                "run_id": run_id,
                "name": job_name,
                "config": config,
                "parameters": parameters,
            },
        }

        jobs_object = {"data": [job]}
        jobs_url = f"{self.orchestration_url}/jobs"
        response = self.session.post(jobs_url, json=jobs_object)
        error_handler(response)

        data = response.json().get("data")[0]
        if "error" in data.keys() or "errors" in data.keys():
            raise Exception()

        return _filter_response(data)

    @Track.track_decorator
    def get_runs(
        self,
        status: str = None,
        priority: str = None,
    ):
        """
        This function returns the list of pipeline runs \n
        Args:
            org_id (str, Optional): to filter runs based on the org_id
            user_id (str, Optional): to filter the run_id based on user_id
            page_size (int, Optional): number of runs to be fetched per request, default = 10
            page_after (int, Optional): number of pages to be skipped, default = 0

        Returns:
            It will return a list of JSON object with pipeline runs. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        all_runs = []
        default_page_size = 20
        start_url = _add_arguments_to_url(
            f"{self.orchestration_url}/runs",
            page_size=default_page_size,
            status=status,
            priority=priority,
        )
        response = self.session.get(start_url)
        error_handler(response)
        runs = response.json().get("data")
        all_runs = all_runs + runs
        next_link = response.json().get("links", {}).get("next")

        while next_link is not None:
            next_endpoint = f"{self.base_url}{next_link}"
            response = self.session.get(next_endpoint)
            error_handler(response)

            response.raise_for_status()
            response_json = response.json()
            all_runs = all_runs + response_json.get("data")

            next_link = response_json.get("links").get("next")

        data = [_filter_response(run) for run in all_runs]
        return data

    @Track.track_decorator
    def get_run(self, run_id: str):
        """
        This function returns the pipeline run data \n
        Args:
            run_id (str): the run_id for which the data is required

        Returns:
            It will return a list of JSON object with pipeline run data. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        url = f"{self.orchestration_url}/runs/{run_id}"
        run = self.session.get(url)
        error_handler(run)
        data = run.json().get("data")
        return _filter_response(data)

    @Track.track_decorator
    def get_jobs(self, run_id: str):
        """
        This function returns the list of jobs executed for a run.\n
        Args:
            run_id (str): the run_id for which the jobs are required
            org_id (str, Optional): to filter runs based on the org_id
            user_id (str, Optional): to filter the run_id based on user_id
            page_size (int, Optional): number of runs to be fetched per request, default = 10
            page_after (int, Optional): number of pages to be skipped, default = 0

        Returns:
            It will return a list of JSON object with pipeline runs. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        all_jobs = []
        default_page_size = 20
        start_url = _add_arguments_to_url(
            f"{self.orchestration_url}/jobs", page_size=default_page_size, run_id=run_id
        )
        response = self.session.get(start_url)
        error_handler(response)
        jobs = response.json().get("data")
        all_jobs = all_jobs + jobs
        next_link = response.json().get("links", {}).get("next")

        while next_link is not None:
            next_endpoint = f"{self.base_url}{next_link}"
            response = self.session.get(next_endpoint)
            error_handler(response)
            response.raise_for_status()
            response_json = response.json()
            all_jobs = all_jobs + response_json.get("data")
            next_link = response_json.get("links").get("next")

        data = [_filter_response(job) for job in all_jobs]
        return data

    @Track.track_decorator
    def get_job(self, job_id: str):
        """
        This function returns the job data for the provided job_id \n
        Args:
            job_id (str): the job_id for which the data is required

        Returns:
            It will return a JSON object with pipeline job data. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """
        url = f"{self.orchestration_url}/jobs/{job_id}"
        job = self.session.get(url)
        error_handler(job)
        data = job.json().get("data", job.json())
        return _filter_response(data)
