from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .compute_provision_strategy import ComputeProvisionStrategy
from .compute_requirement_status import ComputeRequirementStatus
from .compute_requirement_supported_operations import ComputeRequirementSupportedOperations
from .identified import Identified
from .named import Named
from .tagged import Tagged


@dataclass
class ComputeRequirement(Identified, Named, Tagged):
    """
    Defines the requirement for compute resource and chosen options for how to provision it.

    This class is the main model object within the YellowDog Compute API.
    It is passed between the service and clients in order to request compute resource and to monitor the state of that resource.
    """

    id: Optional[str] = field(default=None, init=False)
    """The ID of this compute requirement that is generated by YellowDog Compute when the requirement is first submitted."""
    createdTime: Optional[datetime] = field(default=None, init=False)
    """The date and time when this compute requirement was first submitted to YellowDog Compute."""
    createdById: Optional[str] = field(default=None, init=False)
    """The ID of the User or Application that first submitted this compute requirement."""
    createdFromId: Optional[str] = field(default=None, init=False)
    """Gets the ID of the requirement template if this requirement was created from a template."""
    statusChangedTime: Optional[datetime] = field(default=None, init=False)
    """The date and time when the status or nextStatus last changed"""
    supportedOperations: Optional[ComputeRequirementSupportedOperations] = field(default=None, init=False)
    status: Optional[ComputeRequirementStatus] = field(default=None, init=False)
    """The status of this compute requirement."""
    namespace: str
    """The user allocated namespace used to group compute requirements and other objects together."""
    name: str
    """The user allocated name used to uniquely identify this compute requirement within its namespace."""
    provisionStrategy: ComputeProvisionStrategy
    """The compute provision strategy that YellowDog Compute must use when provisioning instances to meet this requirement."""
    tag: Optional[str] = None
    targetInstanceCount: int = 0
    """The number of instances to be provisioned to meet this compute requirement."""
    expectedInstanceCount: int = 0
    """The number of alive instances expected based on existing instances and the most recent provision action."""
    maintainInstanceCount: bool = False
    """Indicates if the Compute Service should automatically attempt to provision new instances if the number of RUNNING instances is below the specified targetInstanceCount"""
    nextStatus: Optional[ComputeRequirementStatus] = None
    """The next status of this compute requirement when a status transition is being requested."""
