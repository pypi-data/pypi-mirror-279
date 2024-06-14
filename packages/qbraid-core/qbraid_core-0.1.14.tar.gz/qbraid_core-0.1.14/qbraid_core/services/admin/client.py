# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module providing admin client for interacting with qBraid docker build logs.

"""

from typing import Any, Optional

from qbraid_core.client import QbraidClient
from qbraid_core.registry import register_client


@register_client()
class AdminClient(QbraidClient):
    """
    A client for interacting with qBraid's Docker build logs through API calls.

    This client extends the QbraidClient and includes methods to
    get, post, put, and delete Docker build logs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_docker_build_logs(
        self, build_id: Optional[str] = None, query: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Fetch Docker build logs, optionally filtered by a specific build ID.

        Args:
            build_id (Optional[str]): The unique identifier for the docker build to filter logs.
            query (Optional[dict[str, Any]]): Additional query parameters to refine the logs.

        Returns:
            dict[str, Any]: A dictionary containing the docker build logs. If a build_id is
                            specified, returns a specific log; otherwise, returns all logs.

        Raises:
            ValueError: If the provided build_id is not a valid MongoDB ID.
            RequestsApiError: If an API error occurs during the post request.
        """
        params = query or {}

        if build_id:
            if not self._is_valid_object_id(build_id):
                raise ValueError("Invalid MongoDB ID.")
            params["_id"] = build_id

        response = self.session.get("/dev/docker-build-logs/", params=params)
        return response.json()

    def post_docker_build_logs(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Post a new Docker build log to the server.

        Args:
            data (dict[str, Any]): The data of the Docker build log to post.

        Returns:
            dict[str, Any]: A dictionary containing the response from the server.

        Raises:
            RequestsApiError: If an API error occurs during the post request.
        """
        response = self.session.post("/dev/docker-build-logs", json=data)
        return response.json()

    def put_docker_build_logs(self, build_id: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Update an existing Docker build log identified by the build ID.

        Args:
            build_id (str): The unique identifier for the docker build to be updated.
            data (Any): The new data for the Docker build log.

        Returns:
            dict[str, Any]: A dictionary containing the updated build log data.

        Raises:
            ValueError: If the provided build_id is not a valid MongoDB ID.
            RequestsApiError: If an API error occurs during the post request.
        """
        if not self._is_valid_object_id(build_id):
            raise ValueError("Invalid MongoDB ID.")

        response = self.session.put(f"/dev/docker-build-logs/{build_id}", json=data)
        return response.json()

    def delete_docker_build_logs(self, build_id: str) -> dict[str, Any]:
        """
        Delete a Docker build log using a specific build ID.

        Args:
            build_id (str): The unique identifier for the docker build log to be deleted.

        Returns:
            dict: A dictionary containing the response from the server after deletion.

        Raises:
            ValueError: If the provided build_id is not a valid MongoDB ID.
            RequestsApiError: If an API error occurs during the post request.
        """
        if not self._is_valid_object_id(build_id):
            raise ValueError("Invalid MongoDB ID.")

        response = self.session.delete(f"/dev/docker-build-logs/{build_id}")
        return response.json()
