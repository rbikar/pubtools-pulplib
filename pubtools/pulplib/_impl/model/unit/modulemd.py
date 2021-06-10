import re

from .base import Unit, unit_type

from ..attr import pulp_attrib
from ... import compat_attr as attr
from ..frozenlist import frozenlist_or_none_converter


@unit_type("modulemd")
@attr.s(kw_only=True, frozen=True)
class ModulemdUnit(Unit):
    """A :class:`~pubtools.pulplib.Unit` representing a modulemd document.

    .. versionadded:: 1.5.0
    """

    name = pulp_attrib(type=str, pulp_field="name")
    """The name of this module.

    Example: the name of javapackages-tools:201801:20180813043155:dca7b4a4:aarch64
    is "javapackages-tools".
    """

    stream = pulp_attrib(type=str, pulp_field="stream")
    """The stream of this module.

    Example: the stream of javapackages-tools:201801:20180813043155:dca7b4a4:aarch64
    is "201801".
    """

    version = pulp_attrib(type=int, pulp_field="version")
    """The version of this module.

    Example: the version of javapackages-tools:201801:20180813043155:dca7b4a4:aarch64
    is 20180813043155.
    """

    context = pulp_attrib(type=str, pulp_field="context")
    """The context of this module.

    Example: the context of javapackages-tools:201801:20180813043155:dca7b4a4:aarch64
    is "dca7b4a4".
    """

    arch = pulp_attrib(type=str, pulp_field="arch")
    """The architecture of this module.

    Example: the arch of javapackages-tools:201801:20180813043155:dca7b4a4:aarch64
    is "aarch64.
    """

    content_type_id = pulp_attrib(
        default="modulemd", type=str, pulp_field="_content_type_id"
    )

    repository_memberships = pulp_attrib(
        default=None,
        type=list,
        converter=frozenlist_or_none_converter,
        pulp_field="repository_memberships",
    )
    """IDs of repositories containing the unit, or ``None`` if this information is unavailable.

    .. versionadded:: 2.6.0
    """
    artifacts = pulp_attrib(
        default=None,
        type=list,
        converter=frozenlist_or_none_converter,
        pulp_field="artifacts",
    )
    """List of artifacts related to the given module, usually it's a list
    rpms in nevra format without '.rpm' extension and consist of binary, debug and source
    rpms as well.

    Example:
    ["perl-version-7:0.99.24-441.module+el8.3.0+6718+7f269185.src",
     "perl-version-7:0.99.24-441.module+el8.3.0+6718+7f269185.x86_64",
    ]
    """

    profiles = pulp_attrib(type=dict, pulp_field="profiles", default=None)
    """The profiles of this modulemd unit."""

    @property
    def artifacts_filenames(self):
        """
        Artifacts are typically stored as a list of rpms of nevra format without '.rpm' extension,
        this method removes the epoch and returns set of actual rpm filenames.
        """
        regex = r"\d+:"
        reg = re.compile(regex)

        out = set()
        for rpm_nevra in self.artifacts or []:
            out.add(reg.sub("", rpm_nevra, count=1) + ".rpm")
        return out
