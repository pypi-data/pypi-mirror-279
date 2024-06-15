'''
# `launchdarkly_metric`

Refer to the Terraform Registry for docs: [`launchdarkly_metric`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class Metric(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.metric.Metric",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric launchdarkly_metric}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key: builtins.str,
        kind: builtins.str,
        name: builtins.str,
        project_key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        event_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintainer_id: typing.Optional[builtins.str] = None,
        randomization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
        selector: typing.Optional[builtins.str] = None,
        success_criteria: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        unit: typing.Optional[builtins.str] = None,
        urls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MetricUrls", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric launchdarkly_metric} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key: The unique key that references the metric. A change in this field will force the destruction of the existing resource and the creation of a new one. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#key Metric#key}
        :param kind: The metric type. Available choices are ``click``, ``custom``, and ``pageview``. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#kind Metric#kind}
        :param name: The human-friendly name for the metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#name Metric#name}
        :param project_key: The metrics's project key. A change in this field will force the destruction of the existing resource and the creation of a new one. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#project_key Metric#project_key}
        :param description: The description of the metric's purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#description Metric#description}
        :param event_key: The event key for your metric (if custom metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#event_key Metric#event_key}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#id Metric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_active: Whether a metric is a active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#is_active Metric#is_active}
        :param is_numeric: Whether a ``custom`` metric is a numeric metric or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#is_numeric Metric#is_numeric}
        :param maintainer_id: The LaunchDarkly member ID of the member who will maintain the metric. If not set, the API will automatically apply the member associated with your Terraform API key or the most recently-set maintainer Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#maintainer_id Metric#maintainer_id}
        :param randomization_units: A set of one or more context kinds that this metric can measure events from. Metrics can only use context kinds marked as "Available for experiments." For more information, read `Allocating experiment audiences <https://docs.launchdarkly.com/home/creating-experiments/allocation>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#randomization_units Metric#randomization_units}
        :param selector: The CSS selector for your metric (if click metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#selector Metric#selector}
        :param success_criteria: The success criteria for your metric (if numeric metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#success_criteria Metric#success_criteria}
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#tags Metric#tags}
        :param unit: (Required for kind ``custom``) The unit for numeric ``custom`` metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#unit Metric#unit}
        :param urls: urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#urls Metric#urls}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9718b4ae616c7d5730cfdba41f3d30aa916186d136e5fbc3e6ee1017050183df)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MetricConfig(
            key=key,
            kind=kind,
            name=name,
            project_key=project_key,
            description=description,
            event_key=event_key,
            id=id,
            is_active=is_active,
            is_numeric=is_numeric,
            maintainer_id=maintainer_id,
            randomization_units=randomization_units,
            selector=selector,
            success_criteria=success_criteria,
            tags=tags,
            unit=unit,
            urls=urls,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Metric resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Metric to import.
        :param import_from_id: The id of the existing Metric that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Metric to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a238e8c4f1e0a87d2ca34026e7028f96b8e9e355bbdb808c9343d34164c6bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putUrls")
    def put_urls(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MetricUrls", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84db6d1f8221e5a2261dfa4061513cf45213996c075310924411f57a78201960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUrls", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEventKey")
    def reset_event_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventKey", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsActive")
    def reset_is_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsActive", []))

    @jsii.member(jsii_name="resetIsNumeric")
    def reset_is_numeric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsNumeric", []))

    @jsii.member(jsii_name="resetMaintainerId")
    def reset_maintainer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainerId", []))

    @jsii.member(jsii_name="resetRandomizationUnits")
    def reset_randomization_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRandomizationUnits", []))

    @jsii.member(jsii_name="resetSelector")
    def reset_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelector", []))

    @jsii.member(jsii_name="resetSuccessCriteria")
    def reset_success_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessCriteria", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetUnit")
    def reset_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnit", []))

    @jsii.member(jsii_name="resetUrls")
    def reset_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrls", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="urls")
    def urls(self) -> "MetricUrlsList":
        return typing.cast("MetricUrlsList", jsii.get(self, "urls"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventKeyInput")
    def event_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isActiveInput")
    def is_active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isActiveInput"))

    @builtins.property
    @jsii.member(jsii_name="isNumericInput")
    def is_numeric_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isNumericInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="maintainerIdInput")
    def maintainer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintainerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKeyInput")
    def project_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="randomizationUnitsInput")
    def randomization_units_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "randomizationUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorInput")
    def selector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectorInput"))

    @builtins.property
    @jsii.member(jsii_name="successCriteriaInput")
    def success_criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "successCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="urlsInput")
    def urls_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MetricUrls"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MetricUrls"]]], jsii.get(self, "urlsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f187ac51e97f200c05e86341be0b048891b4fdefecaeaf0a7abc60d956337c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="eventKey")
    def event_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventKey"))

    @event_key.setter
    def event_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e728b8a6575d50410407277d89850b5a6d461f151e187c0a71b90006f673a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventKey", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb308bd076026572ed3b5bcda0c13d3450257c996cb6b3bdc4f078e124b2ecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isActive")
    def is_active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isActive"))

    @is_active.setter
    def is_active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d6d49dca264039bbbbe8ad568df8119cf5f59084729fc8f7a92eafa61a7619f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isActive", value)

    @builtins.property
    @jsii.member(jsii_name="isNumeric")
    def is_numeric(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isNumeric"))

    @is_numeric.setter
    def is_numeric(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd10147c31ea0979c854e735053032b3073067008fa265ed78f5c6a2ef825e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isNumeric", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5fb4f6ab3b779556cb958bfe9aa71dbe7767157ca673adef1c3c346bb627c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa0335a08d7114627e79c41e5c039e446eae32a97cfab4ac5117d86ebc3ae8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value)

    @builtins.property
    @jsii.member(jsii_name="maintainerId")
    def maintainer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainerId"))

    @maintainer_id.setter
    def maintainer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c67cd3e5f1e2bad730eb7c24e71ede00db1f7bb76286b5963eac3e7da0aaa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainerId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018dfe8c40d7f417505628c65ac575c2ebded02be876c612f165e92854e20595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0edb4ab79bcda0e31119dd3525c68fa2f129614b5aeeb2ed3cc0e71f8eae229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value)

    @builtins.property
    @jsii.member(jsii_name="randomizationUnits")
    def randomization_units(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "randomizationUnits"))

    @randomization_units.setter
    def randomization_units(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51e0d5dc9a7000c413528345f826bc5fe99dbc522e4f712f219f5e73b00f477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "randomizationUnits", value)

    @builtins.property
    @jsii.member(jsii_name="selector")
    def selector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selector"))

    @selector.setter
    def selector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fcc2263713d7a8b0cc3a334b657509387811bdffe150a9d69904e7182f90611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selector", value)

    @builtins.property
    @jsii.member(jsii_name="successCriteria")
    def success_criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "successCriteria"))

    @success_criteria.setter
    def success_criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783ba82a84cf21f796b923a3b8d60c9bcec8e04ea0ebe6aaf1731422a1a8a11f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successCriteria", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e25b1026b52768f5bbfd56af0559081f3af0b0bb766495352f08c6da5d6a8e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe79168d7cf07aa6d7928c76522031aac5898d5b581ded34f71140dcc908463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.metric.MetricConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key": "key",
        "kind": "kind",
        "name": "name",
        "project_key": "projectKey",
        "description": "description",
        "event_key": "eventKey",
        "id": "id",
        "is_active": "isActive",
        "is_numeric": "isNumeric",
        "maintainer_id": "maintainerId",
        "randomization_units": "randomizationUnits",
        "selector": "selector",
        "success_criteria": "successCriteria",
        "tags": "tags",
        "unit": "unit",
        "urls": "urls",
    },
)
class MetricConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: builtins.str,
        kind: builtins.str,
        name: builtins.str,
        project_key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        event_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintainer_id: typing.Optional[builtins.str] = None,
        randomization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
        selector: typing.Optional[builtins.str] = None,
        success_criteria: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        unit: typing.Optional[builtins.str] = None,
        urls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MetricUrls", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key: The unique key that references the metric. A change in this field will force the destruction of the existing resource and the creation of a new one. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#key Metric#key}
        :param kind: The metric type. Available choices are ``click``, ``custom``, and ``pageview``. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#kind Metric#kind}
        :param name: The human-friendly name for the metric. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#name Metric#name}
        :param project_key: The metrics's project key. A change in this field will force the destruction of the existing resource and the creation of a new one. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#project_key Metric#project_key}
        :param description: The description of the metric's purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#description Metric#description}
        :param event_key: The event key for your metric (if custom metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#event_key Metric#event_key}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#id Metric#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_active: Whether a metric is a active. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#is_active Metric#is_active}
        :param is_numeric: Whether a ``custom`` metric is a numeric metric or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#is_numeric Metric#is_numeric}
        :param maintainer_id: The LaunchDarkly member ID of the member who will maintain the metric. If not set, the API will automatically apply the member associated with your Terraform API key or the most recently-set maintainer Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#maintainer_id Metric#maintainer_id}
        :param randomization_units: A set of one or more context kinds that this metric can measure events from. Metrics can only use context kinds marked as "Available for experiments." For more information, read `Allocating experiment audiences <https://docs.launchdarkly.com/home/creating-experiments/allocation>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#randomization_units Metric#randomization_units}
        :param selector: The CSS selector for your metric (if click metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#selector Metric#selector}
        :param success_criteria: The success criteria for your metric (if numeric metric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#success_criteria Metric#success_criteria}
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#tags Metric#tags}
        :param unit: (Required for kind ``custom``) The unit for numeric ``custom`` metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#unit Metric#unit}
        :param urls: urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#urls Metric#urls}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7cac13f5219f12a99cd83049cfcaff852eed75dcf965f55118e2d716bd2eda)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_key", value=event_key, expected_type=type_hints["event_key"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            check_type(argname="argument is_numeric", value=is_numeric, expected_type=type_hints["is_numeric"])
            check_type(argname="argument maintainer_id", value=maintainer_id, expected_type=type_hints["maintainer_id"])
            check_type(argname="argument randomization_units", value=randomization_units, expected_type=type_hints["randomization_units"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
            check_type(argname="argument success_criteria", value=success_criteria, expected_type=type_hints["success_criteria"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument urls", value=urls, expected_type=type_hints["urls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "kind": kind,
            "name": name,
            "project_key": project_key,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if description is not None:
            self._values["description"] = description
        if event_key is not None:
            self._values["event_key"] = event_key
        if id is not None:
            self._values["id"] = id
        if is_active is not None:
            self._values["is_active"] = is_active
        if is_numeric is not None:
            self._values["is_numeric"] = is_numeric
        if maintainer_id is not None:
            self._values["maintainer_id"] = maintainer_id
        if randomization_units is not None:
            self._values["randomization_units"] = randomization_units
        if selector is not None:
            self._values["selector"] = selector
        if success_criteria is not None:
            self._values["success_criteria"] = success_criteria
        if tags is not None:
            self._values["tags"] = tags
        if unit is not None:
            self._values["unit"] = unit
        if urls is not None:
            self._values["urls"] = urls

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The unique key that references the metric.

        A change in this field will force the destruction of the existing resource and the creation of a new one. A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#key Metric#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''The metric type.

        Available choices are ``click``, ``custom``, and ``pageview``. A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#kind Metric#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The human-friendly name for the metric.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#name Metric#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_key(self) -> builtins.str:
        '''The metrics's project key.

        A change in this field will force the destruction of the existing resource and the creation of a new one. A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#project_key Metric#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the metric's purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#description Metric#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_key(self) -> typing.Optional[builtins.str]:
        '''The event key for your metric (if custom metric).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#event_key Metric#event_key}
        '''
        result = self._values.get("event_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#id Metric#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether a metric is a active.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#is_active Metric#is_active}
        '''
        result = self._values.get("is_active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_numeric(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether a ``custom`` metric is a numeric metric or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#is_numeric Metric#is_numeric}
        '''
        result = self._values.get("is_numeric")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def maintainer_id(self) -> typing.Optional[builtins.str]:
        '''The LaunchDarkly member ID of the member who will maintain the metric.

        If not set, the API will automatically apply the member associated with your Terraform API key or the most recently-set maintainer

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#maintainer_id Metric#maintainer_id}
        '''
        result = self._values.get("maintainer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def randomization_units(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of one or more context kinds that this metric can measure events from.

        Metrics can only use context kinds marked as "Available for experiments." For more information, read `Allocating experiment audiences <https://docs.launchdarkly.com/home/creating-experiments/allocation>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#randomization_units Metric#randomization_units}
        '''
        result = self._values.get("randomization_units")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def selector(self) -> typing.Optional[builtins.str]:
        '''The CSS selector for your metric (if click metric).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#selector Metric#selector}
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def success_criteria(self) -> typing.Optional[builtins.str]:
        '''The success criteria for your metric (if numeric metric).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#success_criteria Metric#success_criteria}
        '''
        result = self._values.get("success_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags associated with your resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#tags Metric#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        '''(Required for kind ``custom``) The unit for numeric ``custom`` metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#unit Metric#unit}
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def urls(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MetricUrls"]]]:
        '''urls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#urls Metric#urls}
        '''
        result = self._values.get("urls")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MetricUrls"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.metric.MetricUrls",
    jsii_struct_bases=[],
    name_mapping={
        "kind": "kind",
        "pattern": "pattern",
        "substring": "substring",
        "url": "url",
    },
)
class MetricUrls:
    def __init__(
        self,
        *,
        kind: builtins.str,
        pattern: typing.Optional[builtins.str] = None,
        substring: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kind: The URL type. Available choices are ``exact``, ``canonical``, ``substring`` and ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#kind Metric#kind}
        :param pattern: (Required for kind ``regex``) The regex pattern to match by. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#pattern Metric#pattern}
        :param substring: (Required for kind ``substring``) The URL substring to match by. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#substring Metric#substring}
        :param url: (Required for kind ``exact`` and ``canonical``) The exact or canonical URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#url Metric#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941ff69f5b9f18fc592a8e5b1561eb5a1ba864e6cf32bab45cb6df1623b19842)
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument substring", value=substring, expected_type=type_hints["substring"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kind": kind,
        }
        if pattern is not None:
            self._values["pattern"] = pattern
        if substring is not None:
            self._values["substring"] = substring
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def kind(self) -> builtins.str:
        '''The URL type. Available choices are ``exact``, ``canonical``, ``substring`` and ``regex``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#kind Metric#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''(Required for kind ``regex``) The regex pattern to match by.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#pattern Metric#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def substring(self) -> typing.Optional[builtins.str]:
        '''(Required for kind ``substring``) The URL substring to match by.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#substring Metric#substring}
        '''
        result = self._values.get("substring")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''(Required for kind ``exact`` and ``canonical``) The exact or canonical URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.19.0/docs/resources/metric#url Metric#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetricUrlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.metric.MetricUrlsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f3d217b508610a18035a5217f323b89e479cd5a157eb253d9c29901a74bad8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MetricUrlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbcaa3a7f4afe74c4d2eebeac98f24d32030b44d079b4028abf1404316e8684)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MetricUrlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592fc9d3a7e22e24d1c2ba83eca83bf0f2dffe36f1a0f82be98cc321cf4a940c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd647efe183cd2627987fcecd63f36d1496cf67b6e0105f334c34d139f568ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b32c1d0311663ba3f157142f424f4c18f470167a078af9cf0527f76c933edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MetricUrls]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MetricUrls]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MetricUrls]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a961b04deceb2d30a12d0a5e30926a6d35f9ce9be8b5e0c0b105de9f5405a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MetricUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.metric.MetricUrlsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc17642b03aa32e656f5d2a71ae51263c436876fe1add6e9d2e1226e4622dc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @jsii.member(jsii_name="resetSubstring")
    def reset_substring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubstring", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="substringInput")
    def substring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "substringInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31fb4bf369628bc2e622796b0ef47fbc3f5d233d9ec04c01a9efa90c675f4544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value)

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5bb0e2ae67ed2a8724d0bcb4bad25c971e5646f9363e97fae2ea78865365be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value)

    @builtins.property
    @jsii.member(jsii_name="substring")
    def substring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "substring"))

    @substring.setter
    def substring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f6390d094677080d1dffcba76d3c238dceb5906283ebaa3429f0159c20ce47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "substring", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3df76cbb6c1cebd649d2355d3605165dd8bf4706d85503e1c38a52d9261b063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MetricUrls]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MetricUrls]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MetricUrls]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac0ad11feae93786717d9abef0bdf6025bdd10fefd401c024be78304eebb815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Metric",
    "MetricConfig",
    "MetricUrls",
    "MetricUrlsList",
    "MetricUrlsOutputReference",
]

publication.publish()

def _typecheckingstub__9718b4ae616c7d5730cfdba41f3d30aa916186d136e5fbc3e6ee1017050183df(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key: builtins.str,
    kind: builtins.str,
    name: builtins.str,
    project_key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    event_key: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maintainer_id: typing.Optional[builtins.str] = None,
    randomization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
    selector: typing.Optional[builtins.str] = None,
    success_criteria: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    unit: typing.Optional[builtins.str] = None,
    urls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MetricUrls, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a238e8c4f1e0a87d2ca34026e7028f96b8e9e355bbdb808c9343d34164c6bb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84db6d1f8221e5a2261dfa4061513cf45213996c075310924411f57a78201960(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MetricUrls, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f187ac51e97f200c05e86341be0b048891b4fdefecaeaf0a7abc60d956337c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e728b8a6575d50410407277d89850b5a6d461f151e187c0a71b90006f673a03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb308bd076026572ed3b5bcda0c13d3450257c996cb6b3bdc4f078e124b2ecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d6d49dca264039bbbbe8ad568df8119cf5f59084729fc8f7a92eafa61a7619f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd10147c31ea0979c854e735053032b3073067008fa265ed78f5c6a2ef825e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5fb4f6ab3b779556cb958bfe9aa71dbe7767157ca673adef1c3c346bb627c5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa0335a08d7114627e79c41e5c039e446eae32a97cfab4ac5117d86ebc3ae8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c67cd3e5f1e2bad730eb7c24e71ede00db1f7bb76286b5963eac3e7da0aaa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018dfe8c40d7f417505628c65ac575c2ebded02be876c612f165e92854e20595(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0edb4ab79bcda0e31119dd3525c68fa2f129614b5aeeb2ed3cc0e71f8eae229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51e0d5dc9a7000c413528345f826bc5fe99dbc522e4f712f219f5e73b00f477(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fcc2263713d7a8b0cc3a334b657509387811bdffe150a9d69904e7182f90611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783ba82a84cf21f796b923a3b8d60c9bcec8e04ea0ebe6aaf1731422a1a8a11f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e25b1026b52768f5bbfd56af0559081f3af0b0bb766495352f08c6da5d6a8e4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe79168d7cf07aa6d7928c76522031aac5898d5b581ded34f71140dcc908463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7cac13f5219f12a99cd83049cfcaff852eed75dcf965f55118e2d716bd2eda(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: builtins.str,
    kind: builtins.str,
    name: builtins.str,
    project_key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    event_key: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maintainer_id: typing.Optional[builtins.str] = None,
    randomization_units: typing.Optional[typing.Sequence[builtins.str]] = None,
    selector: typing.Optional[builtins.str] = None,
    success_criteria: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    unit: typing.Optional[builtins.str] = None,
    urls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MetricUrls, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941ff69f5b9f18fc592a8e5b1561eb5a1ba864e6cf32bab45cb6df1623b19842(
    *,
    kind: builtins.str,
    pattern: typing.Optional[builtins.str] = None,
    substring: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f3d217b508610a18035a5217f323b89e479cd5a157eb253d9c29901a74bad8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbcaa3a7f4afe74c4d2eebeac98f24d32030b44d079b4028abf1404316e8684(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592fc9d3a7e22e24d1c2ba83eca83bf0f2dffe36f1a0f82be98cc321cf4a940c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd647efe183cd2627987fcecd63f36d1496cf67b6e0105f334c34d139f568ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b32c1d0311663ba3f157142f424f4c18f470167a078af9cf0527f76c933edd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a961b04deceb2d30a12d0a5e30926a6d35f9ce9be8b5e0c0b105de9f5405a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MetricUrls]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc17642b03aa32e656f5d2a71ae51263c436876fe1add6e9d2e1226e4622dc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fb4bf369628bc2e622796b0ef47fbc3f5d233d9ec04c01a9efa90c675f4544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5bb0e2ae67ed2a8724d0bcb4bad25c971e5646f9363e97fae2ea78865365be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f6390d094677080d1dffcba76d3c238dceb5906283ebaa3429f0159c20ce47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3df76cbb6c1cebd649d2355d3605165dd8bf4706d85503e1c38a52d9261b063(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac0ad11feae93786717d9abef0bdf6025bdd10fefd401c024be78304eebb815(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MetricUrls]],
) -> None:
    """Type checking stubs"""
    pass
