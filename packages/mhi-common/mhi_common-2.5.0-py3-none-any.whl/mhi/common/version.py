"""
Version numbers
"""

from typing import Optional

__all__ = ['Version', 'InvalidVersion']

class InvalidVersion(ValueError):
    """Raised when a version string is not a valid version.

    >>> Version("invalid")
    Traceback (most recent call last):
        ...
    mhi.common.version.InvalidVersion: Invalid version: 'invalid'
    """


class Version:
    """
    Support for ##.## and ##.##.## version identifiers

    Ordering:
       1.0 < 1.0.0 < 1.0.1 < 1.1 < 1.1.0 < 1.1.1
    """

    @staticmethod
    def valid(ver: str) -> bool:
        """
        Validate a version number as parsable
        """

        try:
            Version(ver)
            return True
        except InvalidVersion:
            return False

    def __init__(self, ver):

        try:
            parts = list(map(int, ver.split('.')))
            if len(parts) not in {2, 3}:
                raise ValueError("Expected 2 or 3 parts")

            if any(part not in range(0, 100) for part in parts):
                raise ValueError("Part outside of range 0..99")

            self._version = tuple(parts)

        except ValueError:
            raise InvalidVersion("Invalid version: %r" % ver) from None

    def __lt__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._version < other._version

    def __le__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._version <= other._version

    def __eq__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._version == other._version

    def __ge__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._version >= other._version

    def __gt__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._version > other._version

    def __ne__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented

        return self._version != other._version

    @property
    def major(self) -> int:
        """
        The Version's major number (read-only)
        """
        return self._version[0]

    @property
    def minor(self) -> int:
        """
        The Version's minor number (read-only)
        """
        return self._version[1]

    @property
    def patch(self) -> Optional[int]:
        """
        The Version's patch number (optional, read-only)
        """
        return self._version[2] if len(self._version) == 3 else None

    @property
    def dev(self) -> bool:
        """
        Development flag (read-only)
        """
        return len(self._version) == 2

    def __repr__(self) -> str:
        return "Version('%s')" % self

    def __str__(self) -> str:
        return ".".join(map(str, self._version))

    def __hash__(self) -> int:
        return hash(self._version)
