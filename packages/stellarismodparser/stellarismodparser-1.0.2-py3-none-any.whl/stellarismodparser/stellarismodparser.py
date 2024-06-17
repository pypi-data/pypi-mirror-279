from logging import getLogger
from os import PathLike
from typing import List, Optional

from semver import Version

logger = getLogger(__name__)

class Mod:
    def __init__(
            self,
            name: str,
            path: Optional[PathLike],
            dependencies: Optional[List[str]],
            picture: Optional[PathLike],
            tags: Optional[List[str]],
            version: Optional[str],
            supported_version: Optional[str],
            remote_file_id: Optional[int],
        ) -> None:
        self.name = name
        self.path = path
        self.dependencies = dependencies
        self.picture = picture
        self.tags = tags
        if len(tags) > 10:
            logger.warning(f"Mod {name} has more than 10 tags. This will prevent the mod from being uploaded to the Steam Workshop and Paradox Mods.")
        self.version = version
        self.supported_version = StellarisVersion.parse(supported_version) if supported_version else None
        self.remote_file_id = remote_file_id

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Mod(name={self.name}, path={self.path}, dependencies={self.dependencies}, picture={self.picture}, tags={self.tags}, version={self.version}, supported_version={self.supported_version}, remote_file_id={self.remote_file_id})"

    @classmethod
    def from_dict(cls, mod_dict: dict) -> "Mod":
        return cls(
            mod_dict["name"],
            mod_dict.get("path"),
            mod_dict.get("dependencies"),
            mod_dict.get("picture"),
            mod_dict.get("tags"),
            mod_dict.get("version"),
            mod_dict.get("supported_version"),
            mod_dict.get("remote_file_id"),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "dependencies": self.dependencies,
            "picture": self.picture,
            "tags": self.tags,
            "version": self.version,
            "supported_version": self.supported_version.to_dict() if self.supported_version else None,
            "remote_file_id": self.remote_file_id,
        }

class StellarisVersion(Version):
    def __init__(self, **kwargs) -> None:
        # Build a dictionary of the arguments except prerelease and build
        super().__init__(**kwargs)

    @property
    def codename(self) -> str:
        return self.CODENAME_LIST.get(f"{self.major}.{self.minor}", "Unknown")

    CODENAME_LIST = {
        "1.0": "Release",
        "1.1": "Clarke",
        "1.2": "Asimov",
        "1.3": "Heinlein",
        "1.4": "Kennedy",
        "1.5": "Banks",
        "1.6": "Adams",
        "1.7": "Bradbury",
        "1.8": "Čapek",
        "1.9": "Boulle",
        "2.0": "Cherryh",
        "2.1": "Niven",
        "2.2": "Le Guin",
        "2.3": "Wolfe",
        "2.4": "Lee",
        "2.5": "Shelley",
        "2.6": "Verne",
        "2.7": "Wells",
        "2.8": "Butler",
        "3.0": "Dick", # lol
        "3.1": "Lem",
        "3.2": "Herbert",
        "3.3": "Libra",
        "3.4": "Cepheus",
        "3.5": "Fornax",
        "3.6": "Orion",
        "3.7": "Canis Minor",
        "3.8": "Gemini",
        "3.9": "Caelum",
        "3.10": "Pyxis",
        "3.11": "Eridanus",
        "3.12": "Andromeda",
    }

    def __str__(self) -> str:
        version = self.codename
        version += " %d.%d.%d" % (self.major, self.minor, self.patch)
        if self.prerelease:
            version += "-%s" % self.prerelease
        if self.build:
            version += "+%s" % self.build
        return version

    def to_tuple(self) -> tuple:
        return (self.codename, self.major, self.minor, self.patch, self.prerelease, self.build)

    def to_dict(self) -> dict:
        return dict(
            codename=self.codename,
            major=self.major,
            minor=self.minor,
            patch=self.patch,
            prerelease=self.prerelease,
            build=self.build,
        )

def parse(path: PathLike) -> Mod:
    config = {}
    current_key = None
    in_multiline_value = False
    multiline_value = []

    with open(path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        if in_multiline_value:
            if line == '}':
                in_multiline_value = False
                config[current_key] = multiline_value
            else:
                multiline_value.append(line.strip('"'))
        elif '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"')
            if value == '{':
                in_multiline_value = True
                current_key = key
                multiline_value = []
            else:
                config[key] = value

    return Mod.from_dict(config)
