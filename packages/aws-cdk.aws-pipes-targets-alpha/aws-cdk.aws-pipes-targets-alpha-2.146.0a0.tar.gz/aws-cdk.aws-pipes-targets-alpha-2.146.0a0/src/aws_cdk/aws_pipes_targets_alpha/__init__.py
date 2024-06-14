'''
# Amazon EventBridge Pipes Targets Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

EventBridge Pipes Targets let you create a target for a EventBridge Pipe.

For more details see the service documentation:

[Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html)

## Targets

Pipe targets are the end point of a EventBridge Pipe.

The following targets are supported:

1. `targets.SqsTarget`: [Send event source to a Queue](#amazon-sqs)
2. `targets.SfnStateMachine`: [Invoke a State Machine from an event source](#aws-step-functions)

### Amazon SQS

A SQS message queue can be used as a target for a pipe. Messages will be pushed to the queue.

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


pipe_target = targets.SqsTarget(target_queue)

pipe = pipes.Pipe(self, "Pipe",
    source=SomeSource(source_queue),
    target=pipe_target
)
```

The target input can be transformed:

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


pipe_target = targets.SqsTarget(target_queue,
    input_transformation=pipes.InputTransformation.from_object({
        "SomeKey": pipes.DynamicInput.from_event_path("$.body")
    })
)

pipe = pipes.Pipe(self, "Pipe",
    source=SomeSource(source_queue),
    target=pipe_target
)
```

### AWS Step Functions State Machine

A State Machine can be used as a target for a pipe. The State Machine will be invoked with the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_state_machine: sfn.IStateMachine


pipe_target = targets.SfnStateMachine(target_state_machine)

pipe = pipes.Pipe(self, "Pipe",
    source=SomeSource(source_queue),
    target=pipe_target
)
```

Specifying the Invocation Type when the target State Machine is invoked:

```python
# source_queue: sqs.Queue
# target_state_machine: sfn.IStateMachine


pipe_target = targets.SfnStateMachine(target_state_machine,
    invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
)

pipe = pipes.Pipe(self, "Pipe",
    source=SomeSource(source_queue),
    target=pipe_target
)
```

The input to the target State Machine can be transformed:

```python
# source_queue: sqs.Queue
# target_state_machine: sfn.IStateMachine


pipe_target = targets.SfnStateMachine(target_state_machine,
    input_transformation=pipes.InputTransformation.from_object({"body": "<$.body>"}),
    invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
)

pipe = pipes.Pipe(self, "Pipe",
    source=SomeSource(source_queue),
    target=pipe_target
)
```
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_pipes_alpha as _aws_cdk_aws_pipes_alpha_c8863edb
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class SfnStateMachine(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SfnStateMachine",
):
    '''(experimental) An EventBridge Pipes target that sends messages to an AWS Step Functions State Machine.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_state_machine: sfn.IStateMachine
        
        
        pipe_target = targets.SfnStateMachine(target_state_machine,
            invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SomeSource(source_queue),
            target=pipe_target
        )
    '''

    def __init__(
        self,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        invocation_type: typing.Optional["StateMachineInvocationType"] = None,
    ) -> None:
        '''
        :param state_machine: -
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: none
        :param invocation_type: (experimental) Specify whether to invoke the State Machine synchronously (``REQUEST_RESPONSE``) or asynchronously (``FIRE_AND_FORGET``). Default: StateMachineInvocationType.FIRE_AND_FORGET

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cddabb332e0b60ec3973a3c36973508988408ffb44951b1b8dcc16215177367)
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        parameters = SfnStateMachineParameters(
            input_transformation=input_transformation, invocation_type=invocation_type
        )

        jsii.create(self.__class__, self, [state_machine, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169a0f99db474ac2020c24c5f65dbcabf638d6c90b8d5dfee693056ea77477bd)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861f71f9df52dbc34295d2606d532fa6d6f532e4a0b5feb1abca7e6c4c4ad3ab)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SfnStateMachineParameters",
    jsii_struct_bases=[],
    name_mapping={
        "input_transformation": "inputTransformation",
        "invocation_type": "invocationType",
    },
)
class SfnStateMachineParameters:
    def __init__(
        self,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        invocation_type: typing.Optional["StateMachineInvocationType"] = None,
    ) -> None:
        '''(experimental) Parameters for the SfnStateMachine target.

        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: none
        :param invocation_type: (experimental) Specify whether to invoke the State Machine synchronously (``REQUEST_RESPONSE``) or asynchronously (``FIRE_AND_FORGET``). Default: StateMachineInvocationType.FIRE_AND_FORGET

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_state_machine: sfn.IStateMachine
            
            
            pipe_target = targets.SfnStateMachine(target_state_machine,
                invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SomeSource(source_queue),
                target=pipe_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6897ef83f36ecfa9f0d5ac9e3856ed5d5408bb83b1937fe3cc5067697aa9126e)
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def invocation_type(self) -> typing.Optional["StateMachineInvocationType"]:
        '''(experimental) Specify whether to invoke the State Machine synchronously (``REQUEST_RESPONSE``) or asynchronously (``FIRE_AND_FORGET``).

        :default: StateMachineInvocationType.FIRE_AND_FORGET

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsqsqueueparameters.html#cfn-pipes-pipe-pipetargetsqsqueueparameters-messagededuplicationid
        :stability: experimental
        '''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional["StateMachineInvocationType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SfnStateMachineParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class SqsTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SqsTarget",
):
    '''(experimental) A EventBridge Pipes target that sends messages to an SQS queue.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_queue: sqs.Queue
        
        
        pipe_target = targets.SqsTarget(target_queue)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SomeSource(source_queue),
            target=pipe_target
        )
    '''

    def __init__(
        self,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param queue: -
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: none
        :param message_deduplication_id: (experimental) This parameter applies only to FIFO (first-in-first-out) queues. The token used for deduplication of sent messages. Default: none
        :param message_group_id: (experimental) The FIFO message group ID to use as the target. Default: none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7b503b3079d9e51045b3114396a73fc627aec339028fa488ab019eb604fff9)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        parameters = SqsTargetParameters(
            input_transformation=input_transformation,
            message_deduplication_id=message_deduplication_id,
            message_group_id=message_group_id,
        )

        jsii.create(self.__class__, self, [queue, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b7cde197ff34e185db774e7f6e4e787c10c737410018f2eae647c30c381734)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf7e2c97f60032a9e2b4a8926850651a42c588ee6eb5c9d5927f02ad257089f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SqsTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "input_transformation": "inputTransformation",
        "message_deduplication_id": "messageDeduplicationId",
        "message_group_id": "messageGroupId",
    },
)
class SqsTargetParameters:
    def __init__(
        self,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) SQS target properties.

        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: none
        :param message_deduplication_id: (experimental) This parameter applies only to FIFO (first-in-first-out) queues. The token used for deduplication of sent messages. Default: none
        :param message_group_id: (experimental) The FIFO message group ID to use as the target. Default: none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_queue: sqs.Queue
            
            
            pipe_target = targets.SqsTarget(target_queue,
                input_transformation=pipes.InputTransformation.from_object({
                    "SomeKey": pipes.DynamicInput.from_event_path("$.body")
                })
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SomeSource(source_queue),
                target=pipe_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860ddbc258740cac07f5dbaa48920ad737f4e849a942863e0e92606f15d6ec0f)
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument message_deduplication_id", value=message_deduplication_id, expected_type=type_hints["message_deduplication_id"])
            check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if message_deduplication_id is not None:
            self._values["message_deduplication_id"] = message_deduplication_id
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def message_deduplication_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) This parameter applies only to FIFO (first-in-first-out) queues.

        The token used for deduplication of sent messages.

        :default: none

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsqsqueueparameters.html#cfn-pipes-pipe-pipetargetsqsqueueparameters-messagededuplicationid
        :stability: experimental
        '''
        result = self._values.get("message_deduplication_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The FIFO message group ID to use as the target.

        :default: none

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsqsqueueparameters.html#cfn-pipes-pipe-pipetargetsqsqueueparameters-messagegroupid
        :stability: experimental
        '''
        result = self._values.get("message_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-targets-alpha.StateMachineInvocationType")
class StateMachineInvocationType(enum.Enum):
    '''(experimental) InvocationType for invoking the State Machine.

    :see: https://docs.aws.amazon.com/eventbridge/latest/pipes-reference/API_PipeTargetStateMachineParameters.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_state_machine: sfn.IStateMachine
        
        
        pipe_target = targets.SfnStateMachine(target_state_machine,
            invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SomeSource(source_queue),
            target=pipe_target
        )
    '''

    FIRE_AND_FORGET = "FIRE_AND_FORGET"
    '''(experimental) Invoke StepFunction asynchronously (``StartExecution``).

    See https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html for more details.

    :stability: experimental
    '''
    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    '''(experimental) Invoke StepFunction synchronously (``StartSyncExecution``) and wait for the execution to complete.

    See https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartSyncExecution.html for more details.

    :stability: experimental
    '''


__all__ = [
    "SfnStateMachine",
    "SfnStateMachineParameters",
    "SqsTarget",
    "SqsTargetParameters",
    "StateMachineInvocationType",
]

publication.publish()

def _typecheckingstub__9cddabb332e0b60ec3973a3c36973508988408ffb44951b1b8dcc16215177367(
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    invocation_type: typing.Optional[StateMachineInvocationType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169a0f99db474ac2020c24c5f65dbcabf638d6c90b8d5dfee693056ea77477bd(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861f71f9df52dbc34295d2606d532fa6d6f532e4a0b5feb1abca7e6c4c4ad3ab(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6897ef83f36ecfa9f0d5ac9e3856ed5d5408bb83b1937fe3cc5067697aa9126e(
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    invocation_type: typing.Optional[StateMachineInvocationType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7b503b3079d9e51045b3114396a73fc627aec339028fa488ab019eb604fff9(
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    message_deduplication_id: typing.Optional[builtins.str] = None,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b7cde197ff34e185db774e7f6e4e787c10c737410018f2eae647c30c381734(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf7e2c97f60032a9e2b4a8926850651a42c588ee6eb5c9d5927f02ad257089f(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860ddbc258740cac07f5dbaa48920ad737f4e849a942863e0e92606f15d6ec0f(
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    message_deduplication_id: typing.Optional[builtins.str] = None,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
