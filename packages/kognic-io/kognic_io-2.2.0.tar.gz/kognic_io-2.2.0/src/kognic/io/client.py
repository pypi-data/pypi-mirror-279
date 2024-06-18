"""Client for communicating with the Kognic platform."""

import logging
from typing import Optional

from deprecated import deprecated
from kognic.auth import DEFAULT_HOST as DEFAULT_AUTH_HOST
from kognic.auth.requests.auth_session import RequestsAuthSession
from kognic.base_clients.cloud_storage import FileResourceClient
from kognic.base_clients.http_client import HttpClient
from kognic.io.model.hosts import DEFAULT_INPUT_API_HOST, DEFAULT_ORDER_EXECUTION_API_HOST, DEFAULT_SHAPE_INTEGRATION_API_HOST
from kognic.io.resources.annotation.annotation import AnnotationResource
from kognic.io.resources.calibration.calibration import CalibrationResource
from kognic.io.resources.input.input import InputResource
from kognic.io.resources.pre_annotation.pre_annotation import PreAnnotationResource
from kognic.io.resources.project.project import ProjectResource
from kognic.io.resources.scene.aggregated_lidars_and_cameras_seq import AggregatedLidarsAndCamerasSequence
from kognic.io.resources.scene.cameras import Cameras
from kognic.io.resources.scene.cameras_sequence import CamerasSequence
from kognic.io.resources.scene.lidars import Lidars
from kognic.io.resources.scene.lidars_and_cameras import LidarsAndCameras
from kognic.io.resources.scene.lidars_and_cameras_sequence import LidarsAndCamerasSequence
from kognic.io.resources.scene.lidars_sequence import LidarsSequence
from kognic.io.resources.scene.scene import SceneResource

log = logging.getLogger(__name__)


class KognicIOClient:
    """Client to work upload and retrieve data from the Kognic platform"""

    def __init__(
        self,
        *,
        auth=None,
        host: str = DEFAULT_INPUT_API_HOST,
        order_execution_api_host: str = DEFAULT_ORDER_EXECUTION_API_HOST,
        shape_integration_api_host: str = DEFAULT_SHAPE_INTEGRATION_API_HOST,
        auth_host: str = DEFAULT_AUTH_HOST,
        client_organization_id: Optional[int] = None,
        max_retry_attempts: int = 23,
        max_retry_wait_time: int = 60,
        timeout: int = 60,
        max_connections: int = 10,
    ):
        """
        :param auth: auth credentials, see https://developers.kognic.com/docs/kognic-auth
        :param host: Base url for the input api
        :param order_execution_api_host: Base url for the order execution api
        :param shape_integration_api_host: Base url for the shape integration api
        :param auth_host: Base url for the auth server
        :param client_organization_id: Overrides your users organization id. Only works with an Kognic user.
        :param max_upload_retry_attempts: Max number of attempts to retry uploading a file to GCS.
        :param max_upload_retry_wait_time:  Max with time before retrying an upload to GCS.
        :param timeout: Max time to wait for response from server.
        :param max_connections: Max nr network connections to apply to the http client.
        """
        self._auth_session = RequestsAuthSession(host=auth_host, auth=auth)
        self._input_client = HttpClient(
            host=host,
            client_organization_id=client_organization_id,
            timeout=timeout,
            session=self._auth_session,
        )

        self._order_execution_client = HttpClient(
            host=order_execution_api_host,
            client_organization_id=client_organization_id,
            timeout=timeout,
            session=self._auth_session,
        )

        self.shape_integration_api_client = HttpClient(
            host=shape_integration_api_host,
            client_organization_id=client_organization_id,
            timeout=timeout,
            session=self._auth_session,
        )

        self._file_client = FileResourceClient(
            max_retry_attempts=max_retry_attempts,
            max_retry_wait_time=max_retry_wait_time,
            timeout=timeout,
            max_connections=max_connections,
        )

        self.calibration = CalibrationResource(self._input_client, self._file_client)
        self.project = ProjectResource(self._input_client, self._file_client)
        self.annotation = AnnotationResource(self._input_client, self._file_client)
        self.input = InputResource(self._input_client, self._file_client)
        self.pre_annotation = PreAnnotationResource(self._input_client, self._file_client)
        self.scene = SceneResource(self._input_client, self._file_client)

        self.lidars_and_cameras = LidarsAndCameras(self._input_client, self._file_client)
        self.lidars_and_cameras_sequence = LidarsAndCamerasSequence(self._input_client, self._file_client)
        self.cameras = Cameras(self._input_client, self._file_client)
        self.cameras_sequence = CamerasSequence(self._input_client, self._file_client)
        self.lidars = Lidars(self._input_client, self._file_client)
        self.lidars_sequence = LidarsSequence(self._input_client, self._file_client)
        self.aggregated_lidars_and_cameras_seq = AggregatedLidarsAndCamerasSequence(self._input_client, self._file_client)

    @property
    @deprecated(reason="Use `lidars_and_cameras` instead")
    def lidar_and_cameras(self) -> LidarsAndCameras:
        return self.lidars_and_cameras
