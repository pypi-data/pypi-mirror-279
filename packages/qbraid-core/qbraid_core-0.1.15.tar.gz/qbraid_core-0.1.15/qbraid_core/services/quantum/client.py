# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module providing client for interacting with qBraid quantum services.

"""
import base64
import sys
from typing import Any, Optional

from qbraid_core.client import QbraidClient
from qbraid_core.exceptions import RequestsApiError
from qbraid_core.registry import register_client
from qbraid_core.system.executables import get_active_python_path, python_paths_equivalent

from .adapter import transform_device_data
from .exceptions import QuantumServiceRequestError
from .proxy import SUPPORTED_QJOB_LIBS, quantum_lib_proxy_state


@register_client()
class QuantumClient(QbraidClient):
    """Client for interacting with qBraid quantum services."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_device(self, data: dict[str, Any]) -> dict[str, Any]:
        """Updates a quantum device with the given data."""
        try:
            return self.session.put("/quantum-devices", json=data).json()
        except RequestsApiError as err:
            raise QuantumServiceRequestError("Failed to update device") from err

    def update_job(self, data: dict[str, Any]) -> dict[str, Any]:
        """Updates a quantum job with the given data."""
        try:
            return self.session.put("/quantum-jobs", json=data).json()
        except RequestsApiError as err:
            raise QuantumServiceRequestError("Failed to update job") from err

    def search_devices(self, query: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Returns a list of quantum devices that match the given query filters."""
        query = query or {}

        # forward compatibility for casing transition
        if query.get("type") == "SIMULATOR":
            query["type"] = "Simulator"

        try:
            devices = self.session.get("/quantum-devices", params=query).json()
        except RequestsApiError as err:
            raise QuantumServiceRequestError("Failed to retrieve device data") from err

        return [transform_device_data(device) for device in devices]

    def search_jobs(self, query: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Returns a list of quantum jobs run by the user that match the given query filters."""
        query = query or {}

        max_results = query.pop("maxResults", None)
        if max_results is not None:
            query["resultsPerPage"] = max_results

        try:
            jobs_data = self.session.get("/quantum-jobs", params=query).json()
            if "jobsArray" in jobs_data:
                jobs_data = jobs_data["jobsArray"]
            return jobs_data
        except RequestsApiError as err:
            raise QuantumServiceRequestError("Failed to retrieve job data") from err

    def get_device(
        self,
        qbraid_id: Optional[str] = None,
        vendor_id: Optional[str] = None,
        object_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Returns the metadata corresponding to the specified quantum device."""
        query = {}
        if qbraid_id is not None:
            query["qbraid_id"] = qbraid_id
        if vendor_id is not None:
            query["objArg"] = vendor_id
        if object_id is not None:
            if not self._is_valid_object_id(object_id):
                raise ValueError(
                    "Invalid object_id format: expected a 24-character hexadecimal string"
                )
            query["_id"] = object_id
        if len(query) == 0:
            raise ValueError("Must provide either qbraid_id, vendor_id, or object_id")

        devices = self.search_devices(query=query)

        if len(devices) == 0:
            raise QuantumServiceRequestError("No devices found matching given criteria")

        device = devices[0]
        return transform_device_data(device)

    def get_job(
        self,
        qbraid_id: Optional[str] = None,
        vendor_id: Optional[str] = None,
        object_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Returns the metadata corresponding to the specified quantum job."""
        query = {}
        if qbraid_id is not None:
            query["qbraidJobId"] = qbraid_id
        if vendor_id is not None:
            query["vendorJobId"] = vendor_id
        if object_id is not None:
            if not self._is_valid_object_id(object_id):
                raise ValueError(
                    "Invalid object_id format: expected a 24-character hexadecimal string"
                )
            query["_id"] = object_id
        if len(query) == 0:
            raise ValueError("Must provide either qbraid_id, vendor_id, or object_id")

        jobs = self.search_jobs(query=query)

        if not jobs:
            raise QuantumServiceRequestError("No jobs found matching given criteria")

        job_data = jobs[0]

        return job_data

    def create_job(self, data: dict[str, Any]) -> dict[str, Any]:
        """Creates a new quantum job with the given data."""
        bitcode = data.get("bitcode")

        if bitcode is not None:
            data["bitcode"] = base64.b64encode(bitcode).decode("utf-8")

        try:
            return self.session.post("/quantum-jobs", json=data).json()
        except RequestsApiError as err:
            raise QuantumServiceRequestError("Failed to create job") from err

    def cancel_job(
        self,
        qbraid_id: Optional[str] = None,
        object_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Cancels the quantum job with the given qBraid ID."""
        if not qbraid_id and not object_id:
            raise ValueError("Must provide either qbraid_id or object_id")

        if qbraid_id and object_id:
            raise ValueError("Must provide either qbraid_id or object_id, not both")

        if qbraid_id:
            job_data = self.get_job(qbraid_id=qbraid_id)
            object_id = job_data.get("_id")

        if not self._is_valid_object_id(object_id):
            raise ValueError("Invalid object_id format: expected a 24-character hexadecimal string")

        try:
            return self.session.put(f"/quantum-jobs/cancel/{object_id}").json()
        except RequestsApiError as err:
            raise QuantumServiceRequestError("Failed to cancel job") from err

    @staticmethod
    def qbraid_jobs_state(device_lib: Optional[str] = None) -> dict[str, Any]:
        """
        Checks if qBraid Quantum Jobs are enabled in the current environment for the
        specified device library.

        Args:
            device_lib (Optional[str]): The name of the quantum device library. If None,
                                        checks all supported libraries.

        Returns:
            dict[str, Any]: A dictionary containing the system's executable path and the states
                            of libraries relevant to qBraid Quantum Jobs. The libraries' states
                            include whether they are supported and enabled.
        """
        python_exe = get_active_python_path()
        environment_state = {"exe": str(python_exe)}
        is_default_python = python_paths_equivalent(sys.executable, str(python_exe))

        check_libs = [device_lib] if device_lib else list(SUPPORTED_QJOB_LIBS.keys())

        libs_state = {
            lib: quantum_lib_proxy_state(lib, is_default_python=is_default_python)
            for lib in check_libs
        }

        environment_state["libs"] = libs_state

        return environment_state
