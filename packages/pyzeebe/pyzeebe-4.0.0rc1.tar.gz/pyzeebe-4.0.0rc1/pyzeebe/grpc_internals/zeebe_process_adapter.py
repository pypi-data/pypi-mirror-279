import json
import os
from typing import Any, Dict, Iterable, NoReturn, Optional, Tuple, cast

import aiofiles
import grpc
from typing_extensions import deprecated
from zeebe_grpc.gateway_pb2 import (
    CancelProcessInstanceRequest,
    CreateProcessInstanceRequest,
    CreateProcessInstanceWithResultRequest,
    DeployProcessRequest,
    DeployProcessResponse,
    DeployResourceRequest,
    DeployResourceResponse,
    ProcessRequestObject,
    Resource,
)

from pyzeebe.errors import (
    InvalidJSONError,
    ProcessDefinitionHasNoStartEventError,
    ProcessDefinitionNotFoundError,
    ProcessInstanceNotFoundError,
    ProcessInvalidError,
    ProcessTimeoutError,
)
from pyzeebe.grpc_internals.grpc_utils import is_error_status
from pyzeebe.grpc_internals.zeebe_adapter_base import ZeebeAdapterBase
from pyzeebe.types import Variables


class ZeebeProcessAdapter(ZeebeAdapterBase):
    async def create_process_instance(
        self,
        bpmn_process_id: str,
        version: int,
        variables: Variables,
        tenant_id: Optional[str] = None,
    ) -> int:
        try:
            response = await self._gateway_stub.CreateProcessInstance(
                CreateProcessInstanceRequest(
                    bpmnProcessId=bpmn_process_id,
                    version=version,
                    variables=json.dumps(variables),
                    tenantId=tenant_id,
                )
            )
        except grpc.aio.AioRpcError as grpc_error:
            await self._create_process_errors(grpc_error, bpmn_process_id, version, variables)
        return cast(int, response.processInstanceKey)

    async def create_process_instance_with_result(
        self,
        bpmn_process_id: str,
        version: int,
        variables: Variables,
        timeout: int,
        variables_to_fetch: Iterable[str],
        tenant_id: Optional[str] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            response = await self._gateway_stub.CreateProcessInstanceWithResult(
                CreateProcessInstanceWithResultRequest(
                    request=CreateProcessInstanceRequest(
                        bpmnProcessId=bpmn_process_id,
                        version=version,
                        variables=json.dumps(variables),
                        tenantId=tenant_id,
                    ),
                    requestTimeout=timeout,
                    fetchVariables=variables_to_fetch,
                )
            )
        except grpc.aio.AioRpcError as grpc_error:
            await self._create_process_errors(grpc_error, bpmn_process_id, version, variables)
        return response.processInstanceKey, json.loads(response.variables)

    async def _create_process_errors(
        self, grpc_error: grpc.aio.AioRpcError, bpmn_process_id: str, version: int, variables: Dict[str, Any]
    ) -> NoReturn:
        if is_error_status(grpc_error, grpc.StatusCode.NOT_FOUND):
            raise ProcessDefinitionNotFoundError(bpmn_process_id=bpmn_process_id, version=version) from grpc_error
        elif is_error_status(grpc_error, grpc.StatusCode.INVALID_ARGUMENT):
            raise InvalidJSONError(
                f"Cannot start process: {bpmn_process_id} with version {version}. Variables: {variables}"
            ) from grpc_error
        elif is_error_status(grpc_error, grpc.StatusCode.FAILED_PRECONDITION):
            raise ProcessDefinitionHasNoStartEventError(bpmn_process_id=bpmn_process_id) from grpc_error
        elif is_error_status(grpc_error, grpc.StatusCode.DEADLINE_EXCEEDED):
            raise ProcessTimeoutError(bpmn_process_id) from grpc_error
        await self._handle_grpc_error(grpc_error)

    async def cancel_process_instance(self, process_instance_key: int) -> None:
        try:
            await self._gateway_stub.CancelProcessInstance(
                CancelProcessInstanceRequest(processInstanceKey=process_instance_key)
            )
        except grpc.aio.AioRpcError as grpc_error:
            if is_error_status(grpc_error, grpc.StatusCode.NOT_FOUND):
                raise ProcessInstanceNotFoundError(process_instance_key=process_instance_key) from grpc_error
            await self._handle_grpc_error(grpc_error)

    @deprecated("Deprecated since Zeebe 8.0. Use deploy_resource instead")
    async def deploy_process(self, *process_file_path: str) -> DeployProcessResponse:
        try:
            return await self._gateway_stub.DeployProcess(
                DeployProcessRequest(
                    processes=[await result for result in map(_create_process_request, process_file_path)]
                )
            )
        except grpc.aio.AioRpcError as grpc_error:
            if is_error_status(grpc_error, grpc.StatusCode.INVALID_ARGUMENT):
                raise ProcessInvalidError() from grpc_error
            await self._handle_grpc_error(grpc_error)

    async def deploy_resource(
        self, *resource_file_path: str, tenant_id: Optional[str] = None
    ) -> DeployResourceResponse:
        try:
            return await self._gateway_stub.DeployResource(
                DeployResourceRequest(
                    resources=[await result for result in map(_create_resource_request, resource_file_path)],
                    tenantId=tenant_id,
                )
            )
        except grpc.aio.AioRpcError as grpc_error:
            if is_error_status(grpc_error, grpc.StatusCode.INVALID_ARGUMENT):
                raise ProcessInvalidError() from grpc_error
            await self._handle_grpc_error(grpc_error)


async def _create_process_request(process_file_path: str) -> ProcessRequestObject:
    async with aiofiles.open(process_file_path, "rb") as file:
        return ProcessRequestObject(name=os.path.basename(process_file_path), definition=await file.read())


async def _create_resource_request(resource_file_path: str) -> Resource:
    async with aiofiles.open(resource_file_path, "rb") as file:
        return Resource(name=os.path.basename(resource_file_path), content=await file.read())
