"""Versioning value objects for platform entities and contracts."""

import re
from dataclasses import dataclass

from backend.core.exceptions import ValidationError

SEMVER_REGEX = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?$"
)


@dataclass(frozen=True)
class Version:
    """Immutable monotonic integer version value object.

    Attributes:
        number: Non-negative version integer.
    """

    number: int

    def __post_init__(self) -> None:
        """Validate that version number is a non-negative integer."""
        if not isinstance(self.number, int) or self.number < 0:
            raise ValidationError("Version number must be a non-negative integer.")

    def next_version(self) -> "Version":
        """Return the next incremented Version instance."""
        return Version(self.number + 1)

    def __str__(self) -> str:
        """Return string representation of Version."""
        return str(self.number)


@dataclass(frozen=True)
class SemanticVersion:
    """Immutable Semantic Versioning (SemVer 2.0.0) value object.

    Attributes:
        major: Major version number for breaking changes.
        minor: Minor version number for backwards-compatible features.
        patch: Patch version number for backwards-compatible bug fixes.
        prerelease: Optional prerelease tag (e.g., 'alpha.1', 'rc2').
    """

    major: int
    minor: int
    patch: int
    prerelease: str | None = None

    def __post_init__(self) -> None:
        """Validate SemVer component non-negativity."""
        if (
            not isinstance(self.major, int)
            or self.major < 0
            or not isinstance(self.minor, int)
            or self.minor < 0
            or not isinstance(self.patch, int)
            or self.patch < 0
        ):
            raise ValidationError(
                "SemVer components must be non-negative integers."
            )

    @classmethod
    def parse(cls, version_str: str) -> "SemanticVersion":
        """Parse a SemVer string into a SemanticVersion value object.

        Args:
            version_str: SemVer string (e.g., '1.2.3' or '2.0.0-alpha.1').

        Returns:
            SemanticVersion instance.

        Raises:
            ValidationError: If version_str is not valid SemVer format.
        """
        match = SEMVER_REGEX.match(version_str)
        if not match:
            raise ValidationError(
                f"Invalid Semantic Version string: '{version_str}'."
            )

        groups = match.groupdict()
        return cls(
            major=int(groups["major"]),
            minor=int(groups["minor"]),
            patch=int(groups["patch"]),
            prerelease=groups.get("prerelease"),
        )

    def __str__(self) -> str:
        """Return canonical SemVer string representation."""
        base = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            return f"{base}-{self.prerelease}"
        return base
