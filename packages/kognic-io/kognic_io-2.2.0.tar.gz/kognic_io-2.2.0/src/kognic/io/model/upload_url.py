from typing import Dict

from kognic.io.model.base_serializer import BaseSerializer
from pydantic import Field


class UploadUrls(BaseSerializer):
    files_to_url: Dict[str, str] = Field(alias="files")
    input_uuid: int = Field(alias="jobId")
