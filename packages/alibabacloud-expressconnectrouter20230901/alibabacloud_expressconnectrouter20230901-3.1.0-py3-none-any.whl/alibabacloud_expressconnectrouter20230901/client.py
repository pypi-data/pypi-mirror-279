# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_expressconnectrouter20230901 import models as express_connect_router_20230901_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'regional'
        self.check_config(config)
        self._endpoint = self.get_endpoint('expressconnectrouter', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def attach_express_connect_router_child_instance_with_options(
        self,
        request: express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceResponse:
        """
        @param request: AttachExpressConnectRouterChildInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: AttachExpressConnectRouterChildInstanceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.child_instance_id):
            body['ChildInstanceId'] = request.child_instance_id
        if not UtilClient.is_unset(request.child_instance_owner_id):
            body['ChildInstanceOwnerId'] = request.child_instance_owner_id
        if not UtilClient.is_unset(request.child_instance_region_id):
            body['ChildInstanceRegionId'] = request.child_instance_region_id
        if not UtilClient.is_unset(request.child_instance_type):
            body['ChildInstanceType'] = request.child_instance_type
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AttachExpressConnectRouterChildInstance',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def attach_express_connect_router_child_instance_with_options_async(
        self,
        request: express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceResponse:
        """
        @param request: AttachExpressConnectRouterChildInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: AttachExpressConnectRouterChildInstanceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.child_instance_id):
            body['ChildInstanceId'] = request.child_instance_id
        if not UtilClient.is_unset(request.child_instance_owner_id):
            body['ChildInstanceOwnerId'] = request.child_instance_owner_id
        if not UtilClient.is_unset(request.child_instance_region_id):
            body['ChildInstanceRegionId'] = request.child_instance_region_id
        if not UtilClient.is_unset(request.child_instance_type):
            body['ChildInstanceType'] = request.child_instance_type
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AttachExpressConnectRouterChildInstance',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def attach_express_connect_router_child_instance(
        self,
        request: express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceRequest,
    ) -> express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceResponse:
        """
        @param request: AttachExpressConnectRouterChildInstanceRequest
        @return: AttachExpressConnectRouterChildInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.attach_express_connect_router_child_instance_with_options(request, runtime)

    async def attach_express_connect_router_child_instance_async(
        self,
        request: express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceRequest,
    ) -> express_connect_router_20230901_models.AttachExpressConnectRouterChildInstanceResponse:
        """
        @param request: AttachExpressConnectRouterChildInstanceRequest
        @return: AttachExpressConnectRouterChildInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.attach_express_connect_router_child_instance_with_options_async(request, runtime)

    def check_add_region_to_express_connect_router_with_options(
        self,
        request: express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterResponse:
        """
        @param request: CheckAddRegionToExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CheckAddRegionToExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.fresh_region_id):
            body['FreshRegionId'] = request.fresh_region_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CheckAddRegionToExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterResponse(),
            self.call_api(params, req, runtime)
        )

    async def check_add_region_to_express_connect_router_with_options_async(
        self,
        request: express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterResponse:
        """
        @param request: CheckAddRegionToExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CheckAddRegionToExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.fresh_region_id):
            body['FreshRegionId'] = request.fresh_region_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CheckAddRegionToExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def check_add_region_to_express_connect_router(
        self,
        request: express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterResponse:
        """
        @param request: CheckAddRegionToExpressConnectRouterRequest
        @return: CheckAddRegionToExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.check_add_region_to_express_connect_router_with_options(request, runtime)

    async def check_add_region_to_express_connect_router_async(
        self,
        request: express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.CheckAddRegionToExpressConnectRouterResponse:
        """
        @param request: CheckAddRegionToExpressConnectRouterRequest
        @return: CheckAddRegionToExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.check_add_region_to_express_connect_router_with_options_async(request, runtime)

    def create_express_connect_router_with_options(
        self,
        request: express_connect_router_20230901_models.CreateExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.CreateExpressConnectRouterResponse:
        """
        @param request: CreateExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.alibaba_side_asn):
            body['AlibabaSideAsn'] = request.alibaba_side_asn
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.resource_group_id):
            body['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.tags):
            body['Tags'] = request.tags
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.CreateExpressConnectRouterResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_express_connect_router_with_options_async(
        self,
        request: express_connect_router_20230901_models.CreateExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.CreateExpressConnectRouterResponse:
        """
        @param request: CreateExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.alibaba_side_asn):
            body['AlibabaSideAsn'] = request.alibaba_side_asn
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.resource_group_id):
            body['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.tags):
            body['Tags'] = request.tags
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.CreateExpressConnectRouterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_express_connect_router(
        self,
        request: express_connect_router_20230901_models.CreateExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.CreateExpressConnectRouterResponse:
        """
        @param request: CreateExpressConnectRouterRequest
        @return: CreateExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_express_connect_router_with_options(request, runtime)

    async def create_express_connect_router_async(
        self,
        request: express_connect_router_20230901_models.CreateExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.CreateExpressConnectRouterResponse:
        """
        @param request: CreateExpressConnectRouterRequest
        @return: CreateExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_express_connect_router_with_options_async(request, runtime)

    def create_express_connect_router_association_with_options(
        self,
        request: express_connect_router_20230901_models.CreateExpressConnectRouterAssociationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.CreateExpressConnectRouterAssociationResponse:
        """
        @param request: CreateExpressConnectRouterAssociationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateExpressConnectRouterAssociationResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.allowed_prefixes):
            body['AllowedPrefixes'] = request.allowed_prefixes
        if not UtilClient.is_unset(request.association_region_id):
            body['AssociationRegionId'] = request.association_region_id
        if not UtilClient.is_unset(request.cen_id):
            body['CenId'] = request.cen_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.create_attachment):
            body['CreateAttachment'] = request.create_attachment
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.transit_router_id):
            body['TransitRouterId'] = request.transit_router_id
        if not UtilClient.is_unset(request.transit_router_owner_id):
            body['TransitRouterOwnerId'] = request.transit_router_owner_id
        if not UtilClient.is_unset(request.vpc_id):
            body['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.vpc_owner_id):
            body['VpcOwnerId'] = request.vpc_owner_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateExpressConnectRouterAssociation',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.CreateExpressConnectRouterAssociationResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_express_connect_router_association_with_options_async(
        self,
        request: express_connect_router_20230901_models.CreateExpressConnectRouterAssociationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.CreateExpressConnectRouterAssociationResponse:
        """
        @param request: CreateExpressConnectRouterAssociationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateExpressConnectRouterAssociationResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.allowed_prefixes):
            body['AllowedPrefixes'] = request.allowed_prefixes
        if not UtilClient.is_unset(request.association_region_id):
            body['AssociationRegionId'] = request.association_region_id
        if not UtilClient.is_unset(request.cen_id):
            body['CenId'] = request.cen_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.create_attachment):
            body['CreateAttachment'] = request.create_attachment
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.transit_router_id):
            body['TransitRouterId'] = request.transit_router_id
        if not UtilClient.is_unset(request.transit_router_owner_id):
            body['TransitRouterOwnerId'] = request.transit_router_owner_id
        if not UtilClient.is_unset(request.vpc_id):
            body['VpcId'] = request.vpc_id
        if not UtilClient.is_unset(request.vpc_owner_id):
            body['VpcOwnerId'] = request.vpc_owner_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateExpressConnectRouterAssociation',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.CreateExpressConnectRouterAssociationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_express_connect_router_association(
        self,
        request: express_connect_router_20230901_models.CreateExpressConnectRouterAssociationRequest,
    ) -> express_connect_router_20230901_models.CreateExpressConnectRouterAssociationResponse:
        """
        @param request: CreateExpressConnectRouterAssociationRequest
        @return: CreateExpressConnectRouterAssociationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.create_express_connect_router_association_with_options(request, runtime)

    async def create_express_connect_router_association_async(
        self,
        request: express_connect_router_20230901_models.CreateExpressConnectRouterAssociationRequest,
    ) -> express_connect_router_20230901_models.CreateExpressConnectRouterAssociationResponse:
        """
        @param request: CreateExpressConnectRouterAssociationRequest
        @return: CreateExpressConnectRouterAssociationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.create_express_connect_router_association_with_options_async(request, runtime)

    def delete_express_connect_router_with_options(
        self,
        request: express_connect_router_20230901_models.DeleteExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DeleteExpressConnectRouterResponse:
        """
        @param request: DeleteExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DeleteExpressConnectRouterResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_express_connect_router_with_options_async(
        self,
        request: express_connect_router_20230901_models.DeleteExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DeleteExpressConnectRouterResponse:
        """
        @param request: DeleteExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DeleteExpressConnectRouterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_express_connect_router(
        self,
        request: express_connect_router_20230901_models.DeleteExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.DeleteExpressConnectRouterResponse:
        """
        @param request: DeleteExpressConnectRouterRequest
        @return: DeleteExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_express_connect_router_with_options(request, runtime)

    async def delete_express_connect_router_async(
        self,
        request: express_connect_router_20230901_models.DeleteExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.DeleteExpressConnectRouterResponse:
        """
        @param request: DeleteExpressConnectRouterRequest
        @return: DeleteExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_express_connect_router_with_options_async(request, runtime)

    def delete_express_connect_router_association_with_options(
        self,
        request: express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationResponse:
        """
        @param request: DeleteExpressConnectRouterAssociationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteExpressConnectRouterAssociationResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.delete_attachment):
            body['DeleteAttachment'] = request.delete_attachment
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteExpressConnectRouterAssociation',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_express_connect_router_association_with_options_async(
        self,
        request: express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationResponse:
        """
        @param request: DeleteExpressConnectRouterAssociationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteExpressConnectRouterAssociationResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.delete_attachment):
            body['DeleteAttachment'] = request.delete_attachment
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DeleteExpressConnectRouterAssociation',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_express_connect_router_association(
        self,
        request: express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationRequest,
    ) -> express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationResponse:
        """
        @param request: DeleteExpressConnectRouterAssociationRequest
        @return: DeleteExpressConnectRouterAssociationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.delete_express_connect_router_association_with_options(request, runtime)

    async def delete_express_connect_router_association_async(
        self,
        request: express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationRequest,
    ) -> express_connect_router_20230901_models.DeleteExpressConnectRouterAssociationResponse:
        """
        @param request: DeleteExpressConnectRouterAssociationRequest
        @return: DeleteExpressConnectRouterAssociationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.delete_express_connect_router_association_with_options_async(request, runtime)

    def describe_disabled_express_connect_router_route_entries_with_options(
        self,
        request: express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DescribeDisabledExpressConnectRouterRouteEntriesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeDisabledExpressConnectRouterRouteEntriesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeDisabledExpressConnectRouterRouteEntries',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_disabled_express_connect_router_route_entries_with_options_async(
        self,
        request: express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DescribeDisabledExpressConnectRouterRouteEntriesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeDisabledExpressConnectRouterRouteEntriesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeDisabledExpressConnectRouterRouteEntries',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_disabled_express_connect_router_route_entries(
        self,
        request: express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesRequest,
    ) -> express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DescribeDisabledExpressConnectRouterRouteEntriesRequest
        @return: DescribeDisabledExpressConnectRouterRouteEntriesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_disabled_express_connect_router_route_entries_with_options(request, runtime)

    async def describe_disabled_express_connect_router_route_entries_async(
        self,
        request: express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesRequest,
    ) -> express_connect_router_20230901_models.DescribeDisabledExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DescribeDisabledExpressConnectRouterRouteEntriesRequest
        @return: DescribeDisabledExpressConnectRouterRouteEntriesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_disabled_express_connect_router_route_entries_with_options_async(request, runtime)

    def describe_express_connect_router_with_options(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterResponse:
        """
        @param request: DescribeExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.resource_group_id):
            body['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.tag_models):
            body['TagModels'] = request.tag_models
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_express_connect_router_with_options_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterResponse:
        """
        @param request: DescribeExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.resource_group_id):
            body['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.tag_models):
            body['TagModels'] = request.tag_models
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_express_connect_router(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterResponse:
        """
        @param request: DescribeExpressConnectRouterRequest
        @return: DescribeExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_express_connect_router_with_options(request, runtime)

    async def describe_express_connect_router_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterResponse:
        """
        @param request: DescribeExpressConnectRouterRequest
        @return: DescribeExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_express_connect_router_with_options_async(request, runtime)

    def describe_express_connect_router_allowed_prefix_history_with_options(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryResponse:
        """
        @param request: DescribeExpressConnectRouterAllowedPrefixHistoryRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterAllowedPrefixHistoryResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.instance_id):
            body['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_type):
            body['InstanceType'] = request.instance_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterAllowedPrefixHistory',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_express_connect_router_allowed_prefix_history_with_options_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryResponse:
        """
        @param request: DescribeExpressConnectRouterAllowedPrefixHistoryRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterAllowedPrefixHistoryResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.instance_id):
            body['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_type):
            body['InstanceType'] = request.instance_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterAllowedPrefixHistory',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_express_connect_router_allowed_prefix_history(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryResponse:
        """
        @param request: DescribeExpressConnectRouterAllowedPrefixHistoryRequest
        @return: DescribeExpressConnectRouterAllowedPrefixHistoryResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_express_connect_router_allowed_prefix_history_with_options(request, runtime)

    async def describe_express_connect_router_allowed_prefix_history_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterAllowedPrefixHistoryResponse:
        """
        @param request: DescribeExpressConnectRouterAllowedPrefixHistoryRequest
        @return: DescribeExpressConnectRouterAllowedPrefixHistoryResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_express_connect_router_allowed_prefix_history_with_options_async(request, runtime)

    def describe_express_connect_router_association_with_options(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationResponse:
        """
        @param request: DescribeExpressConnectRouterAssociationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterAssociationResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.association_node_type):
            body['AssociationNodeType'] = request.association_node_type
        if not UtilClient.is_unset(request.association_region_id):
            body['AssociationRegionId'] = request.association_region_id
        if not UtilClient.is_unset(request.cen_id):
            body['CenId'] = request.cen_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.transit_router_id):
            body['TransitRouterId'] = request.transit_router_id
        if not UtilClient.is_unset(request.vpc_id):
            body['VpcId'] = request.vpc_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterAssociation',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_express_connect_router_association_with_options_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationResponse:
        """
        @param request: DescribeExpressConnectRouterAssociationRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterAssociationResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.association_node_type):
            body['AssociationNodeType'] = request.association_node_type
        if not UtilClient.is_unset(request.association_region_id):
            body['AssociationRegionId'] = request.association_region_id
        if not UtilClient.is_unset(request.cen_id):
            body['CenId'] = request.cen_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.transit_router_id):
            body['TransitRouterId'] = request.transit_router_id
        if not UtilClient.is_unset(request.vpc_id):
            body['VpcId'] = request.vpc_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterAssociation',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_express_connect_router_association(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationResponse:
        """
        @param request: DescribeExpressConnectRouterAssociationRequest
        @return: DescribeExpressConnectRouterAssociationResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_express_connect_router_association_with_options(request, runtime)

    async def describe_express_connect_router_association_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterAssociationResponse:
        """
        @param request: DescribeExpressConnectRouterAssociationRequest
        @return: DescribeExpressConnectRouterAssociationResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_express_connect_router_association_with_options_async(request, runtime)

    def describe_express_connect_router_child_instance_with_options(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceResponse:
        """
        @param request: DescribeExpressConnectRouterChildInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterChildInstanceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.child_instance_id):
            body['ChildInstanceId'] = request.child_instance_id
        if not UtilClient.is_unset(request.child_instance_region_id):
            body['ChildInstanceRegionId'] = request.child_instance_region_id
        if not UtilClient.is_unset(request.child_instance_type):
            body['ChildInstanceType'] = request.child_instance_type
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterChildInstance',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_express_connect_router_child_instance_with_options_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceResponse:
        """
        @param request: DescribeExpressConnectRouterChildInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterChildInstanceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.child_instance_id):
            body['ChildInstanceId'] = request.child_instance_id
        if not UtilClient.is_unset(request.child_instance_region_id):
            body['ChildInstanceRegionId'] = request.child_instance_region_id
        if not UtilClient.is_unset(request.child_instance_type):
            body['ChildInstanceType'] = request.child_instance_type
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterChildInstance',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_express_connect_router_child_instance(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceResponse:
        """
        @param request: DescribeExpressConnectRouterChildInstanceRequest
        @return: DescribeExpressConnectRouterChildInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_express_connect_router_child_instance_with_options(request, runtime)

    async def describe_express_connect_router_child_instance_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterChildInstanceResponse:
        """
        @param request: DescribeExpressConnectRouterChildInstanceRequest
        @return: DescribeExpressConnectRouterChildInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_express_connect_router_child_instance_with_options_async(request, runtime)

    def describe_express_connect_router_inter_region_transit_mode_with_options(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeResponse:
        """
        @param request: DescribeExpressConnectRouterInterRegionTransitModeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterInterRegionTransitModeResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterInterRegionTransitMode',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_express_connect_router_inter_region_transit_mode_with_options_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeResponse:
        """
        @param request: DescribeExpressConnectRouterInterRegionTransitModeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterInterRegionTransitModeResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterInterRegionTransitMode',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_express_connect_router_inter_region_transit_mode(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeResponse:
        """
        @param request: DescribeExpressConnectRouterInterRegionTransitModeRequest
        @return: DescribeExpressConnectRouterInterRegionTransitModeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_express_connect_router_inter_region_transit_mode_with_options(request, runtime)

    async def describe_express_connect_router_inter_region_transit_mode_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterInterRegionTransitModeResponse:
        """
        @param request: DescribeExpressConnectRouterInterRegionTransitModeRequest
        @return: DescribeExpressConnectRouterInterRegionTransitModeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_express_connect_router_inter_region_transit_mode_with_options_async(request, runtime)

    def describe_express_connect_router_region_with_options(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRegionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterRegionResponse:
        """
        @param request: DescribeExpressConnectRouterRegionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterRegionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterRegion',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterRegionResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_express_connect_router_region_with_options_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRegionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterRegionResponse:
        """
        @param request: DescribeExpressConnectRouterRegionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterRegionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterRegion',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterRegionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_express_connect_router_region(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRegionRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterRegionResponse:
        """
        @param request: DescribeExpressConnectRouterRegionRequest
        @return: DescribeExpressConnectRouterRegionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_express_connect_router_region_with_options(request, runtime)

    async def describe_express_connect_router_region_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRegionRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterRegionResponse:
        """
        @param request: DescribeExpressConnectRouterRegionRequest
        @return: DescribeExpressConnectRouterRegionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_express_connect_router_region_with_options_async(request, runtime)

    def describe_express_connect_router_route_entries_with_options(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DescribeExpressConnectRouterRouteEntriesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterRouteEntriesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.as_path):
            body['AsPath'] = request.as_path
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.community):
            body['Community'] = request.community
        if not UtilClient.is_unset(request.destination_cidr_block):
            body['DestinationCidrBlock'] = request.destination_cidr_block
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.nexthop_instance_id):
            body['NexthopInstanceId'] = request.nexthop_instance_id
        if not UtilClient.is_unset(request.query_region_id):
            body['QueryRegionId'] = request.query_region_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterRouteEntries',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_express_connect_router_route_entries_with_options_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DescribeExpressConnectRouterRouteEntriesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeExpressConnectRouterRouteEntriesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.as_path):
            body['AsPath'] = request.as_path
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.community):
            body['Community'] = request.community
        if not UtilClient.is_unset(request.destination_cidr_block):
            body['DestinationCidrBlock'] = request.destination_cidr_block
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.nexthop_instance_id):
            body['NexthopInstanceId'] = request.nexthop_instance_id
        if not UtilClient.is_unset(request.query_region_id):
            body['QueryRegionId'] = request.query_region_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeExpressConnectRouterRouteEntries',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_express_connect_router_route_entries(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DescribeExpressConnectRouterRouteEntriesRequest
        @return: DescribeExpressConnectRouterRouteEntriesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_express_connect_router_route_entries_with_options(request, runtime)

    async def describe_express_connect_router_route_entries_async(
        self,
        request: express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesRequest,
    ) -> express_connect_router_20230901_models.DescribeExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DescribeExpressConnectRouterRouteEntriesRequest
        @return: DescribeExpressConnectRouterRouteEntriesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_express_connect_router_route_entries_with_options_async(request, runtime)

    def describe_instance_granted_to_express_connect_router_with_options(
        self,
        request: express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterResponse:
        """
        @param request: DescribeInstanceGrantedToExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeInstanceGrantedToExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.instance_id):
            body['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_owner_id):
            body['InstanceOwnerId'] = request.instance_owner_id
        if not UtilClient.is_unset(request.instance_region_id):
            body['InstanceRegionId'] = request.instance_region_id
        if not UtilClient.is_unset(request.instance_type):
            body['InstanceType'] = request.instance_type
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.resource_group_id):
            body['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.tag_models):
            body['TagModels'] = request.tag_models
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeInstanceGrantedToExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterResponse(),
            self.call_api(params, req, runtime)
        )

    async def describe_instance_granted_to_express_connect_router_with_options_async(
        self,
        request: express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterResponse:
        """
        @param request: DescribeInstanceGrantedToExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DescribeInstanceGrantedToExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.instance_id):
            body['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_owner_id):
            body['InstanceOwnerId'] = request.instance_owner_id
        if not UtilClient.is_unset(request.instance_region_id):
            body['InstanceRegionId'] = request.instance_region_id
        if not UtilClient.is_unset(request.instance_type):
            body['InstanceType'] = request.instance_type
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.resource_group_id):
            body['ResourceGroupId'] = request.resource_group_id
        if not UtilClient.is_unset(request.tag_models):
            body['TagModels'] = request.tag_models
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DescribeInstanceGrantedToExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def describe_instance_granted_to_express_connect_router(
        self,
        request: express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterResponse:
        """
        @param request: DescribeInstanceGrantedToExpressConnectRouterRequest
        @return: DescribeInstanceGrantedToExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.describe_instance_granted_to_express_connect_router_with_options(request, runtime)

    async def describe_instance_granted_to_express_connect_router_async(
        self,
        request: express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.DescribeInstanceGrantedToExpressConnectRouterResponse:
        """
        @param request: DescribeInstanceGrantedToExpressConnectRouterRequest
        @return: DescribeInstanceGrantedToExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.describe_instance_granted_to_express_connect_router_with_options_async(request, runtime)

    def detach_express_connect_router_child_instance_with_options(
        self,
        request: express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceResponse:
        """
        @param request: DetachExpressConnectRouterChildInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DetachExpressConnectRouterChildInstanceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.child_instance_id):
            body['ChildInstanceId'] = request.child_instance_id
        if not UtilClient.is_unset(request.child_instance_type):
            body['ChildInstanceType'] = request.child_instance_type
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DetachExpressConnectRouterChildInstance',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceResponse(),
            self.call_api(params, req, runtime)
        )

    async def detach_express_connect_router_child_instance_with_options_async(
        self,
        request: express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceResponse:
        """
        @param request: DetachExpressConnectRouterChildInstanceRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DetachExpressConnectRouterChildInstanceResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.child_instance_id):
            body['ChildInstanceId'] = request.child_instance_id
        if not UtilClient.is_unset(request.child_instance_type):
            body['ChildInstanceType'] = request.child_instance_type
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DetachExpressConnectRouterChildInstance',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def detach_express_connect_router_child_instance(
        self,
        request: express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceRequest,
    ) -> express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceResponse:
        """
        @param request: DetachExpressConnectRouterChildInstanceRequest
        @return: DetachExpressConnectRouterChildInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.detach_express_connect_router_child_instance_with_options(request, runtime)

    async def detach_express_connect_router_child_instance_async(
        self,
        request: express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceRequest,
    ) -> express_connect_router_20230901_models.DetachExpressConnectRouterChildInstanceResponse:
        """
        @param request: DetachExpressConnectRouterChildInstanceRequest
        @return: DetachExpressConnectRouterChildInstanceResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.detach_express_connect_router_child_instance_with_options_async(request, runtime)

    def disable_express_connect_router_route_entries_with_options(
        self,
        request: express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DisableExpressConnectRouterRouteEntriesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DisableExpressConnectRouterRouteEntriesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.destination_cidr_block):
            body['DestinationCidrBlock'] = request.destination_cidr_block
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.nexthop_instance_id):
            body['NexthopInstanceId'] = request.nexthop_instance_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DisableExpressConnectRouterRouteEntries',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesResponse(),
            self.call_api(params, req, runtime)
        )

    async def disable_express_connect_router_route_entries_with_options_async(
        self,
        request: express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DisableExpressConnectRouterRouteEntriesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: DisableExpressConnectRouterRouteEntriesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.destination_cidr_block):
            body['DestinationCidrBlock'] = request.destination_cidr_block
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.nexthop_instance_id):
            body['NexthopInstanceId'] = request.nexthop_instance_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DisableExpressConnectRouterRouteEntries',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def disable_express_connect_router_route_entries(
        self,
        request: express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesRequest,
    ) -> express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DisableExpressConnectRouterRouteEntriesRequest
        @return: DisableExpressConnectRouterRouteEntriesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.disable_express_connect_router_route_entries_with_options(request, runtime)

    async def disable_express_connect_router_route_entries_async(
        self,
        request: express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesRequest,
    ) -> express_connect_router_20230901_models.DisableExpressConnectRouterRouteEntriesResponse:
        """
        @param request: DisableExpressConnectRouterRouteEntriesRequest
        @return: DisableExpressConnectRouterRouteEntriesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.disable_express_connect_router_route_entries_with_options_async(request, runtime)

    def enable_express_connect_router_route_entries_with_options(
        self,
        request: express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesResponse:
        """
        @param request: EnableExpressConnectRouterRouteEntriesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: EnableExpressConnectRouterRouteEntriesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.destination_cidr_block):
            body['DestinationCidrBlock'] = request.destination_cidr_block
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.nexthop_instance_id):
            body['NexthopInstanceId'] = request.nexthop_instance_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EnableExpressConnectRouterRouteEntries',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesResponse(),
            self.call_api(params, req, runtime)
        )

    async def enable_express_connect_router_route_entries_with_options_async(
        self,
        request: express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesResponse:
        """
        @param request: EnableExpressConnectRouterRouteEntriesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: EnableExpressConnectRouterRouteEntriesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.destination_cidr_block):
            body['DestinationCidrBlock'] = request.destination_cidr_block
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.nexthop_instance_id):
            body['NexthopInstanceId'] = request.nexthop_instance_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EnableExpressConnectRouterRouteEntries',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def enable_express_connect_router_route_entries(
        self,
        request: express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesRequest,
    ) -> express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesResponse:
        """
        @param request: EnableExpressConnectRouterRouteEntriesRequest
        @return: EnableExpressConnectRouterRouteEntriesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.enable_express_connect_router_route_entries_with_options(request, runtime)

    async def enable_express_connect_router_route_entries_async(
        self,
        request: express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesRequest,
    ) -> express_connect_router_20230901_models.EnableExpressConnectRouterRouteEntriesResponse:
        """
        @param request: EnableExpressConnectRouterRouteEntriesRequest
        @return: EnableExpressConnectRouterRouteEntriesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.enable_express_connect_router_route_entries_with_options_async(request, runtime)

    def force_delete_express_connect_router_with_options(
        self,
        request: express_connect_router_20230901_models.ForceDeleteExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ForceDeleteExpressConnectRouterResponse:
        """
        @param request: ForceDeleteExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ForceDeleteExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ForceDeleteExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ForceDeleteExpressConnectRouterResponse(),
            self.call_api(params, req, runtime)
        )

    async def force_delete_express_connect_router_with_options_async(
        self,
        request: express_connect_router_20230901_models.ForceDeleteExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ForceDeleteExpressConnectRouterResponse:
        """
        @param request: ForceDeleteExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ForceDeleteExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ForceDeleteExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ForceDeleteExpressConnectRouterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def force_delete_express_connect_router(
        self,
        request: express_connect_router_20230901_models.ForceDeleteExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.ForceDeleteExpressConnectRouterResponse:
        """
        @param request: ForceDeleteExpressConnectRouterRequest
        @return: ForceDeleteExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.force_delete_express_connect_router_with_options(request, runtime)

    async def force_delete_express_connect_router_async(
        self,
        request: express_connect_router_20230901_models.ForceDeleteExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.ForceDeleteExpressConnectRouterResponse:
        """
        @param request: ForceDeleteExpressConnectRouterRequest
        @return: ForceDeleteExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.force_delete_express_connect_router_with_options_async(request, runtime)

    def grant_instance_to_express_connect_router_with_options(
        self,
        request: express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterResponse:
        """
        @param request: GrantInstanceToExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GrantInstanceToExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.ecr_owner_ali_uid):
            body['EcrOwnerAliUid'] = request.ecr_owner_ali_uid
        if not UtilClient.is_unset(request.instance_id):
            body['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_region_id):
            body['InstanceRegionId'] = request.instance_region_id
        if not UtilClient.is_unset(request.instance_type):
            body['InstanceType'] = request.instance_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GrantInstanceToExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterResponse(),
            self.call_api(params, req, runtime)
        )

    async def grant_instance_to_express_connect_router_with_options_async(
        self,
        request: express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterResponse:
        """
        @param request: GrantInstanceToExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: GrantInstanceToExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.ecr_owner_ali_uid):
            body['EcrOwnerAliUid'] = request.ecr_owner_ali_uid
        if not UtilClient.is_unset(request.instance_id):
            body['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_region_id):
            body['InstanceRegionId'] = request.instance_region_id
        if not UtilClient.is_unset(request.instance_type):
            body['InstanceType'] = request.instance_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GrantInstanceToExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def grant_instance_to_express_connect_router(
        self,
        request: express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterResponse:
        """
        @param request: GrantInstanceToExpressConnectRouterRequest
        @return: GrantInstanceToExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.grant_instance_to_express_connect_router_with_options(request, runtime)

    async def grant_instance_to_express_connect_router_async(
        self,
        request: express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.GrantInstanceToExpressConnectRouterResponse:
        """
        @param request: GrantInstanceToExpressConnectRouterRequest
        @return: GrantInstanceToExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.grant_instance_to_express_connect_router_with_options_async(request, runtime)

    def list_express_connect_router_supported_region_with_options(
        self,
        request: express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionResponse:
        """
        @param request: ListExpressConnectRouterSupportedRegionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListExpressConnectRouterSupportedRegionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.node_type):
            body['NodeType'] = request.node_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ListExpressConnectRouterSupportedRegion',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_express_connect_router_supported_region_with_options_async(
        self,
        request: express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionResponse:
        """
        @param request: ListExpressConnectRouterSupportedRegionRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListExpressConnectRouterSupportedRegionResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.node_type):
            body['NodeType'] = request.node_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ListExpressConnectRouterSupportedRegion',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_express_connect_router_supported_region(
        self,
        request: express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionRequest,
    ) -> express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionResponse:
        """
        @param request: ListExpressConnectRouterSupportedRegionRequest
        @return: ListExpressConnectRouterSupportedRegionResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_express_connect_router_supported_region_with_options(request, runtime)

    async def list_express_connect_router_supported_region_async(
        self,
        request: express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionRequest,
    ) -> express_connect_router_20230901_models.ListExpressConnectRouterSupportedRegionResponse:
        """
        @param request: ListExpressConnectRouterSupportedRegionRequest
        @return: ListExpressConnectRouterSupportedRegionResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_express_connect_router_supported_region_with_options_async(request, runtime)

    def list_tag_resources_with_options(
        self,
        request: express_connect_router_20230901_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ListTagResourcesResponse:
        """
        @param request: ListTagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListTagResourcesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.resource_id):
            body['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag):
            body['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ListTagResources',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ListTagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def list_tag_resources_with_options_async(
        self,
        request: express_connect_router_20230901_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ListTagResourcesResponse:
        """
        @param request: ListTagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ListTagResourcesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.max_results):
            body['MaxResults'] = request.max_results
        if not UtilClient.is_unset(request.next_token):
            body['NextToken'] = request.next_token
        if not UtilClient.is_unset(request.resource_id):
            body['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag):
            body['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ListTagResources',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ListTagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def list_tag_resources(
        self,
        request: express_connect_router_20230901_models.ListTagResourcesRequest,
    ) -> express_connect_router_20230901_models.ListTagResourcesResponse:
        """
        @param request: ListTagResourcesRequest
        @return: ListTagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.list_tag_resources_with_options(request, runtime)

    async def list_tag_resources_async(
        self,
        request: express_connect_router_20230901_models.ListTagResourcesRequest,
    ) -> express_connect_router_20230901_models.ListTagResourcesResponse:
        """
        @param request: ListTagResourcesRequest
        @return: ListTagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.list_tag_resources_with_options_async(request, runtime)

    def modify_express_connect_router_with_options(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterResponse:
        """
        @param request: ModifyExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ModifyExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ModifyExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ModifyExpressConnectRouterResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_express_connect_router_with_options_async(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterResponse:
        """
        @param request: ModifyExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ModifyExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.description):
            body['Description'] = request.description
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.name):
            body['Name'] = request.name
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ModifyExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ModifyExpressConnectRouterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_express_connect_router(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterResponse:
        """
        @param request: ModifyExpressConnectRouterRequest
        @return: ModifyExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.modify_express_connect_router_with_options(request, runtime)

    async def modify_express_connect_router_async(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterResponse:
        """
        @param request: ModifyExpressConnectRouterRequest
        @return: ModifyExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.modify_express_connect_router_with_options_async(request, runtime)

    def modify_express_connect_router_association_allowed_prefix_with_options(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixResponse:
        """
        @param request: ModifyExpressConnectRouterAssociationAllowedPrefixRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ModifyExpressConnectRouterAssociationAllowedPrefixResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.allowed_prefixes):
            body['AllowedPrefixes'] = request.allowed_prefixes
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.owner_account):
            body['OwnerAccount'] = request.owner_account
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ModifyExpressConnectRouterAssociationAllowedPrefix',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_express_connect_router_association_allowed_prefix_with_options_async(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixResponse:
        """
        @param request: ModifyExpressConnectRouterAssociationAllowedPrefixRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ModifyExpressConnectRouterAssociationAllowedPrefixResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.allowed_prefixes):
            body['AllowedPrefixes'] = request.allowed_prefixes
        if not UtilClient.is_unset(request.association_id):
            body['AssociationId'] = request.association_id
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.owner_account):
            body['OwnerAccount'] = request.owner_account
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ModifyExpressConnectRouterAssociationAllowedPrefix',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_express_connect_router_association_allowed_prefix(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixRequest,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixResponse:
        """
        @param request: ModifyExpressConnectRouterAssociationAllowedPrefixRequest
        @return: ModifyExpressConnectRouterAssociationAllowedPrefixResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.modify_express_connect_router_association_allowed_prefix_with_options(request, runtime)

    async def modify_express_connect_router_association_allowed_prefix_async(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixRequest,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterAssociationAllowedPrefixResponse:
        """
        @param request: ModifyExpressConnectRouterAssociationAllowedPrefixRequest
        @return: ModifyExpressConnectRouterAssociationAllowedPrefixResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.modify_express_connect_router_association_allowed_prefix_with_options_async(request, runtime)

    def modify_express_connect_router_inter_region_transit_mode_with_options(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeResponse:
        """
        @param request: ModifyExpressConnectRouterInterRegionTransitModeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ModifyExpressConnectRouterInterRegionTransitModeResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.transit_mode_list):
            body['TransitModeList'] = request.transit_mode_list
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ModifyExpressConnectRouterInterRegionTransitMode',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeResponse(),
            self.call_api(params, req, runtime)
        )

    async def modify_express_connect_router_inter_region_transit_mode_with_options_async(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeResponse:
        """
        @param request: ModifyExpressConnectRouterInterRegionTransitModeRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: ModifyExpressConnectRouterInterRegionTransitModeResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.transit_mode_list):
            body['TransitModeList'] = request.transit_mode_list
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ModifyExpressConnectRouterInterRegionTransitMode',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def modify_express_connect_router_inter_region_transit_mode(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeRequest,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeResponse:
        """
        @param request: ModifyExpressConnectRouterInterRegionTransitModeRequest
        @return: ModifyExpressConnectRouterInterRegionTransitModeResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.modify_express_connect_router_inter_region_transit_mode_with_options(request, runtime)

    async def modify_express_connect_router_inter_region_transit_mode_async(
        self,
        request: express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeRequest,
    ) -> express_connect_router_20230901_models.ModifyExpressConnectRouterInterRegionTransitModeResponse:
        """
        @param request: ModifyExpressConnectRouterInterRegionTransitModeRequest
        @return: ModifyExpressConnectRouterInterRegionTransitModeResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.modify_express_connect_router_inter_region_transit_mode_with_options_async(request, runtime)

    def move_resource_group_with_options(
        self,
        request: express_connect_router_20230901_models.MoveResourceGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.MoveResourceGroupResponse:
        """
        @param request: MoveResourceGroupRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: MoveResourceGroupResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.new_resource_group_id):
            body['NewResourceGroupId'] = request.new_resource_group_id
        if not UtilClient.is_unset(request.resource_id):
            body['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='MoveResourceGroup',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.MoveResourceGroupResponse(),
            self.call_api(params, req, runtime)
        )

    async def move_resource_group_with_options_async(
        self,
        request: express_connect_router_20230901_models.MoveResourceGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.MoveResourceGroupResponse:
        """
        @param request: MoveResourceGroupRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: MoveResourceGroupResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.new_resource_group_id):
            body['NewResourceGroupId'] = request.new_resource_group_id
        if not UtilClient.is_unset(request.resource_id):
            body['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='MoveResourceGroup',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.MoveResourceGroupResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def move_resource_group(
        self,
        request: express_connect_router_20230901_models.MoveResourceGroupRequest,
    ) -> express_connect_router_20230901_models.MoveResourceGroupResponse:
        """
        @param request: MoveResourceGroupRequest
        @return: MoveResourceGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.move_resource_group_with_options(request, runtime)

    async def move_resource_group_async(
        self,
        request: express_connect_router_20230901_models.MoveResourceGroupRequest,
    ) -> express_connect_router_20230901_models.MoveResourceGroupResponse:
        """
        @param request: MoveResourceGroupRequest
        @return: MoveResourceGroupResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.move_resource_group_with_options_async(request, runtime)

    def revoke_instance_from_express_connect_router_with_options(
        self,
        request: express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterResponse:
        """
        @param request: RevokeInstanceFromExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RevokeInstanceFromExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.ecr_owner_ali_uid):
            body['EcrOwnerAliUid'] = request.ecr_owner_ali_uid
        if not UtilClient.is_unset(request.instance_id):
            body['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_region_id):
            body['InstanceRegionId'] = request.instance_region_id
        if not UtilClient.is_unset(request.instance_type):
            body['InstanceType'] = request.instance_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='RevokeInstanceFromExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterResponse(),
            self.call_api(params, req, runtime)
        )

    async def revoke_instance_from_express_connect_router_with_options_async(
        self,
        request: express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterResponse:
        """
        @param request: RevokeInstanceFromExpressConnectRouterRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: RevokeInstanceFromExpressConnectRouterResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        if not UtilClient.is_unset(request.ecr_owner_ali_uid):
            body['EcrOwnerAliUid'] = request.ecr_owner_ali_uid
        if not UtilClient.is_unset(request.instance_id):
            body['InstanceId'] = request.instance_id
        if not UtilClient.is_unset(request.instance_region_id):
            body['InstanceRegionId'] = request.instance_region_id
        if not UtilClient.is_unset(request.instance_type):
            body['InstanceType'] = request.instance_type
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='RevokeInstanceFromExpressConnectRouter',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def revoke_instance_from_express_connect_router(
        self,
        request: express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterResponse:
        """
        @param request: RevokeInstanceFromExpressConnectRouterRequest
        @return: RevokeInstanceFromExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.revoke_instance_from_express_connect_router_with_options(request, runtime)

    async def revoke_instance_from_express_connect_router_async(
        self,
        request: express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterRequest,
    ) -> express_connect_router_20230901_models.RevokeInstanceFromExpressConnectRouterResponse:
        """
        @param request: RevokeInstanceFromExpressConnectRouterRequest
        @return: RevokeInstanceFromExpressConnectRouterResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.revoke_instance_from_express_connect_router_with_options_async(request, runtime)

    def synchronize_express_connect_router_inter_region_bandwidth_with_options(
        self,
        request: express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthResponse:
        """
        @param request: SynchronizeExpressConnectRouterInterRegionBandwidthRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SynchronizeExpressConnectRouterInterRegionBandwidthResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SynchronizeExpressConnectRouterInterRegionBandwidth',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthResponse(),
            self.call_api(params, req, runtime)
        )

    async def synchronize_express_connect_router_inter_region_bandwidth_with_options_async(
        self,
        request: express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthResponse:
        """
        @param request: SynchronizeExpressConnectRouterInterRegionBandwidthRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: SynchronizeExpressConnectRouterInterRegionBandwidthResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.ecr_id):
            body['EcrId'] = request.ecr_id
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SynchronizeExpressConnectRouterInterRegionBandwidth',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def synchronize_express_connect_router_inter_region_bandwidth(
        self,
        request: express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthRequest,
    ) -> express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthResponse:
        """
        @param request: SynchronizeExpressConnectRouterInterRegionBandwidthRequest
        @return: SynchronizeExpressConnectRouterInterRegionBandwidthResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.synchronize_express_connect_router_inter_region_bandwidth_with_options(request, runtime)

    async def synchronize_express_connect_router_inter_region_bandwidth_async(
        self,
        request: express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthRequest,
    ) -> express_connect_router_20230901_models.SynchronizeExpressConnectRouterInterRegionBandwidthResponse:
        """
        @param request: SynchronizeExpressConnectRouterInterRegionBandwidthRequest
        @return: SynchronizeExpressConnectRouterInterRegionBandwidthResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.synchronize_express_connect_router_inter_region_bandwidth_with_options_async(request, runtime)

    def tag_resources_with_options(
        self,
        request: express_connect_router_20230901_models.TagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.TagResourcesResponse:
        """
        @param request: TagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: TagResourcesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.resource_id):
            body['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag):
            body['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TagResources',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.TagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def tag_resources_with_options_async(
        self,
        request: express_connect_router_20230901_models.TagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.TagResourcesResponse:
        """
        @param request: TagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: TagResourcesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.resource_id):
            body['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag):
            body['Tag'] = request.tag
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TagResources',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.TagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def tag_resources(
        self,
        request: express_connect_router_20230901_models.TagResourcesRequest,
    ) -> express_connect_router_20230901_models.TagResourcesResponse:
        """
        @param request: TagResourcesRequest
        @return: TagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.tag_resources_with_options(request, runtime)

    async def tag_resources_async(
        self,
        request: express_connect_router_20230901_models.TagResourcesRequest,
    ) -> express_connect_router_20230901_models.TagResourcesResponse:
        """
        @param request: TagResourcesRequest
        @return: TagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.tag_resources_with_options_async(request, runtime)

    def untag_resources_with_options(
        self,
        request: express_connect_router_20230901_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.UntagResourcesResponse:
        """
        @param request: UntagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UntagResourcesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.all):
            body['All'] = request.all
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.resource_id):
            body['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag_key):
            body['TagKey'] = request.tag_key
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UntagResources',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.UntagResourcesResponse(),
            self.call_api(params, req, runtime)
        )

    async def untag_resources_with_options_async(
        self,
        request: express_connect_router_20230901_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> express_connect_router_20230901_models.UntagResourcesResponse:
        """
        @param request: UntagResourcesRequest
        @param runtime: runtime options for this request RuntimeOptions
        @return: UntagResourcesResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.all):
            body['All'] = request.all
        if not UtilClient.is_unset(request.client_token):
            body['ClientToken'] = request.client_token
        if not UtilClient.is_unset(request.dry_run):
            body['DryRun'] = request.dry_run
        if not UtilClient.is_unset(request.resource_id):
            body['ResourceId'] = request.resource_id
        if not UtilClient.is_unset(request.resource_type):
            body['ResourceType'] = request.resource_type
        if not UtilClient.is_unset(request.tag_key):
            body['TagKey'] = request.tag_key
        req = open_api_models.OpenApiRequest(
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='UntagResources',
            version='2023-09-01',
            protocol='HTTPS',
            pathname='/',
            method='POST',
            auth_type='AK',
            style='RPC',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            express_connect_router_20230901_models.UntagResourcesResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def untag_resources(
        self,
        request: express_connect_router_20230901_models.UntagResourcesRequest,
    ) -> express_connect_router_20230901_models.UntagResourcesResponse:
        """
        @param request: UntagResourcesRequest
        @return: UntagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return self.untag_resources_with_options(request, runtime)

    async def untag_resources_async(
        self,
        request: express_connect_router_20230901_models.UntagResourcesRequest,
    ) -> express_connect_router_20230901_models.UntagResourcesResponse:
        """
        @param request: UntagResourcesRequest
        @return: UntagResourcesResponse
        """
        runtime = util_models.RuntimeOptions()
        return await self.untag_resources_with_options_async(request, runtime)
