"""DBT Cloud mixin for dapi_validator"""

# pylint: disable=too-few-public-methods, too-many-locals

import logging
import os
import time
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urlencode, urljoin

import requests

logger = logging.getLogger(__name__)


DBT_CLOUD_RUN_SUCCESS_STATUS = 10  # This means that the job has completed

try:
    import click

    secho = click.secho
except ImportError:  # pragma: no cover

    def secho(*args, **kwargs):  # pylint: disable=unused-argument
        """Temporary wrapper for secho if click is not installed"""
        print(*args)


@dataclass
class DBTCloudProject:
    """DBT Cloud project"""

    project_id: int
    account_id: int
    repo_name: str
    subdirectory: Optional[str] = None


class DBTCloudMixin:
    """
    A mixin plugin used for adding dbt_cloud support to DBT DAPI validator.
    This plugin helps with downloading the dbt models from dbt cloud.
    """

    def _dbt_cloud_request(self, uri_path: str) -> requests.Response:
        """Make a request to the DBT Cloud API"""
        dbt_cloud_url = os.environ.get("DAPI_DBT_CLOUD_URL")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {os.environ.get('DAPI_DBT_CLOUD_API_TOKEN')}",
        }

        response = requests.get(
            urljoin(dbt_cloud_url, uri_path), headers=headers, timeout=10
        )
        response.raise_for_status()
        return response

    def _validate_json_response(self, response: requests.Response) -> None:
        response = response.json()

        if response["status"]["code"] != 200 or not response["status"]["is_success"]:
            logger.error("DBT Cloud API request failed: %s", response)
            raise RuntimeError("DBT Cloud API request failed")

    def _dbt_cloud_api_request(self, uri_path: str) -> Dict:
        response = self._dbt_cloud_request(uri_path)
        self._validate_json_response(response)
        return response.json()["data"]

    def _get_all_dbt_cloud_projects(self) -> Dict[str, DBTCloudProject]:
        """Get the DBT Cloud projects"""
        dbt_cloud_projects = []
        accounts = self._dbt_cloud_api_request("/api/v2/accounts/")
        current_repo_name = os.environ.get("GITHUB_REPOSITORY")

        for account in accounts:
            projects = self._dbt_cloud_api_request(
                f"/api/v2/accounts/{account['id']}/projects/"
            )

            for project in projects:
                repo_name = project.get("repository", {}).get("full_name")
                repo_subdirectory = project.get("dbt_project_subdirectory")

                if repo_name != current_repo_name:
                    continue

                dbt_cloud_projects.append(
                    DBTCloudProject(
                        project_id=project["id"],
                        account_id=account["id"],
                        repo_name=repo_name,
                        subdirectory=repo_subdirectory or "",
                    )
                )

        return dbt_cloud_projects

    def _sync_dbt_cloud_artifacts(self, projects: Dict[str, "DBTProject"]) -> bool:
        """Sync the dbt projects from dbt cloud"""

        count = 0
        dbt_cloud_projects = self._get_all_dbt_cloud_projects()
        for dbt_cloud_project in dbt_cloud_projects:
            for project in projects.values():
                if not project.full_path.endswith(dbt_cloud_project.subdirectory):
                    continue

                base_url = f"/api/v2/accounts/{dbt_cloud_project.account_id}/runs"
                params = {
                    "project_id": dbt_cloud_project.project_id,
                    "status": DBT_CLOUD_RUN_SUCCESS_STATUS,
                    "order_by": "-created_at",
                    "limit": 10,
                }
                runs = self._dbt_cloud_api_request(base_url + "/?" + urlencode(params))

                for run in runs:
                    if run["git_sha"] != os.environ.get("GITHUB_HEAD_SHA"):
                        continue

                    artifacts_url = f"{base_url}/{run['id']}/artifacts/"
                    artifacts = self._dbt_cloud_api_request(artifacts_url)

                    for artifact in artifacts:
                        artifact_url = f"{artifacts_url}{artifact}"
                        content = self._dbt_cloud_request(artifact_url).text
                        artifact_path = os.path.join(
                            project.full_path, project.artifacts_dir, artifact
                        )

                        if os.path.exists(artifact_path):
                            secho(
                                f"Artifact exists. Overwriting: {artifact_path}",
                                fg="yellow",
                            )

                        os.makedirs(os.path.dirname(artifact_path), exist_ok=True)

                        secho(f"Downloading artifact to {artifact_path}")
                        with open(artifact_path, "w", encoding="utf-8") as fp:
                            fp.write(content)

                    count += 1
                    break

        return count == len(dbt_cloud_projects)

    def sync_dbt_cloud_artifacts(self, projects: Dict[str, "DBTProject"]) -> bool:
        """Sync the dbt projects from dbt cloud with a retry"""

        if not os.environ.get("DAPI_DBT_CLOUD_API_TOKEN") or not os.environ.get(
            "DAPI_DBT_CLOUD_URL"
        ):
            logger.info("DBT Cloud API token or URL not found")
            return False

        # Keep retrying for a bit till we get the artifacts
        # By default, we will retry every 30 seconds for 15 minutes
        retry_count = int(os.environ.get("DAPI_DBT_CLOUD_RETRY_COUNT") or 30)
        retry_count = 0 if retry_count < 0 else retry_count
        retry_wait_secs = int(os.environ.get("DAPI_DBT_CLOUD_RETRY_INTERVAL") or 30)

        while retry_count >= 0:
            secho("Attempting to sync dbt cloud artifacts")

            if self._sync_dbt_cloud_artifacts(projects):
                return True

            secho("Couldn't find any artifacts")
            if retry_count > 0:
                secho(f"Retrying {retry_count} more time(s)")
                time.sleep(retry_wait_secs)

            retry_count -= 1

        return False
