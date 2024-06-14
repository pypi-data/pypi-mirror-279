'''
# replace this
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8


class VpcPattern(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudscouts/cdk-vpc-pattern.VpcPattern",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        azs: typing.Sequence[builtins.str],
        cidr: builtins.str,
        name: builtins.str,
        private_subnets: typing.Sequence[builtins.str],
        public_subnets: typing.Sequence[builtins.str],
        database_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_kubernenetes: typing.Optional[builtins.bool] = None,
        kubernetes_cluster_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param azs: 
        :param cidr: 
        :param name: 
        :param private_subnets: 
        :param public_subnets: 
        :param database_subnets: 
        :param enable_kubernenetes: 
        :param kubernetes_cluster_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac6742ae841e9d82ad49d5233c981839035c065822f64614985a71918db41e2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpcProps(
            azs=azs,
            cidr=cidr,
            name=name,
            private_subnets=private_subnets,
            public_subnets=public_subnets,
            database_subnets=database_subnets,
            enable_kubernenetes=enable_kubernenetes,
            kubernetes_cluster_name=kubernetes_cluster_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="databaseSubnets")
    def database_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.get(self, "databaseSubnets"))

    @database_subnets.setter
    def database_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5b26c1050450afeeaefe0f67de6a485ee4f54aec6c510697eec03d4ad875e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseSubnets", value)

    @builtins.property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.get(self, "privateSubnets"))

    @private_subnets.setter
    def private_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2c13ddb48b89e29628cef8375c1a5ca6f77e3cb81e3deb1f5351997b80a2a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateSubnets", value)

    @builtins.property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet], jsii.get(self, "publicSubnets"))

    @public_subnets.setter
    def public_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c53642f01b762fe31cc755a63fe1163b498e55221cd666c647e7a8d9253f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicSubnets", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: _aws_cdk_aws_ec2_ceddda9d.IVpc) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9783cfc94bc6e71bbde11d460bfa01f59b5309bf316a8179f277084dfa2cba9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)


@jsii.data_type(
    jsii_type="@cloudscouts/cdk-vpc-pattern.VpcProps",
    jsii_struct_bases=[],
    name_mapping={
        "azs": "azs",
        "cidr": "cidr",
        "name": "name",
        "private_subnets": "privateSubnets",
        "public_subnets": "publicSubnets",
        "database_subnets": "databaseSubnets",
        "enable_kubernenetes": "enableKubernenetes",
        "kubernetes_cluster_name": "kubernetesClusterName",
    },
)
class VpcProps:
    def __init__(
        self,
        *,
        azs: typing.Sequence[builtins.str],
        cidr: builtins.str,
        name: builtins.str,
        private_subnets: typing.Sequence[builtins.str],
        public_subnets: typing.Sequence[builtins.str],
        database_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_kubernenetes: typing.Optional[builtins.bool] = None,
        kubernetes_cluster_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param azs: 
        :param cidr: 
        :param name: 
        :param private_subnets: 
        :param public_subnets: 
        :param database_subnets: 
        :param enable_kubernenetes: 
        :param kubernetes_cluster_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8972cfcdd317a8f99d8231d993ade5bea254fc748aa46acb98d9048929966e9a)
            check_type(argname="argument azs", value=azs, expected_type=type_hints["azs"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument private_subnets", value=private_subnets, expected_type=type_hints["private_subnets"])
            check_type(argname="argument public_subnets", value=public_subnets, expected_type=type_hints["public_subnets"])
            check_type(argname="argument database_subnets", value=database_subnets, expected_type=type_hints["database_subnets"])
            check_type(argname="argument enable_kubernenetes", value=enable_kubernenetes, expected_type=type_hints["enable_kubernenetes"])
            check_type(argname="argument kubernetes_cluster_name", value=kubernetes_cluster_name, expected_type=type_hints["kubernetes_cluster_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "azs": azs,
            "cidr": cidr,
            "name": name,
            "private_subnets": private_subnets,
            "public_subnets": public_subnets,
        }
        if database_subnets is not None:
            self._values["database_subnets"] = database_subnets
        if enable_kubernenetes is not None:
            self._values["enable_kubernenetes"] = enable_kubernenetes
        if kubernetes_cluster_name is not None:
            self._values["kubernetes_cluster_name"] = kubernetes_cluster_name

    @builtins.property
    def azs(self) -> typing.List[builtins.str]:
        result = self._values.get("azs")
        assert result is not None, "Required property 'azs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cidr(self) -> builtins.str:
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_subnets(self) -> typing.List[builtins.str]:
        result = self._values.get("private_subnets")
        assert result is not None, "Required property 'private_subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def public_subnets(self) -> typing.List[builtins.str]:
        result = self._values.get("public_subnets")
        assert result is not None, "Required property 'public_subnets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def database_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("database_subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_kubernenetes(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_kubernenetes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def kubernetes_cluster_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kubernetes_cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "VpcPattern",
    "VpcProps",
]

publication.publish()

def _typecheckingstub__eac6742ae841e9d82ad49d5233c981839035c065822f64614985a71918db41e2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    azs: typing.Sequence[builtins.str],
    cidr: builtins.str,
    name: builtins.str,
    private_subnets: typing.Sequence[builtins.str],
    public_subnets: typing.Sequence[builtins.str],
    database_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_kubernenetes: typing.Optional[builtins.bool] = None,
    kubernetes_cluster_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5b26c1050450afeeaefe0f67de6a485ee4f54aec6c510697eec03d4ad875e9(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2c13ddb48b89e29628cef8375c1a5ca6f77e3cb81e3deb1f5351997b80a2a9(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c53642f01b762fe31cc755a63fe1163b498e55221cd666c647e7a8d9253f45(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.ISubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9783cfc94bc6e71bbde11d460bfa01f59b5309bf316a8179f277084dfa2cba9b(
    value: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8972cfcdd317a8f99d8231d993ade5bea254fc748aa46acb98d9048929966e9a(
    *,
    azs: typing.Sequence[builtins.str],
    cidr: builtins.str,
    name: builtins.str,
    private_subnets: typing.Sequence[builtins.str],
    public_subnets: typing.Sequence[builtins.str],
    database_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_kubernenetes: typing.Optional[builtins.bool] = None,
    kubernetes_cluster_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
