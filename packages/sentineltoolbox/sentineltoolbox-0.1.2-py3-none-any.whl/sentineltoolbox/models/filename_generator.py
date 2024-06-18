import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import partial
from pathlib import Path
from string import ascii_letters
from typing import Any, Callable

from sentineltoolbox.exceptions import DataSemanticConversionError
from sentineltoolbox.typedefs import (
    FileNameGenerator,
    L_DataFileNamePattern,
    T_DateTime,
    T_TimeDelta,
    fix_datetime,
    fix_timedelta,
)

from .s2_legacy_pdi_filename import PDILogicalFilename
from .s2_legacy_product_name import S2MSIL1CProductURI

__all__ = ["detect_filename_pattern", "FileNameGenerator"]

DATE_FORMAT = r"%Y%m%dT%H%M%S"


RE_PATTERNS = dict(
    ext_L=r"(?:\.SAFE|\.SEN3)",  # .SAFE
    ext=r"(?:\.zarr\.zip|\.zarr|\.json\.zip|\.json)",  # .zarr.zip
    mission2=r"S[0-9]{2}",  # S03
    mission1=r"S[0-9]{1}",  # S3
    mission=r"S[0-9]{1,2}",  # S3, S03
    platform=r"[A-Z_]",  # A, _
    level=r"(?:0|1|2)",  # 1
    level_L=r"(?:0|1|2|_)",  # 1
    level_S2=r"L[1-2][A-C]",  # L1C
    sensor=r"[A-Z]{3}",  # OLC, MSI, SLS
    sensor_S3L=r"(?:OL|SL|SY)",  # OL
    sensor_S3ADFL=r"(?:OL|SL|SY|AX)",  # OL
    sensor_S2L=r"(?:)",  # ??
    prod_S3L=r"[A-Z0-9]{3}",  # EFR, CR0
    adf_S3L=r"[A-Z0-9_]{6}",  # CLUTAX, CLM_AX
    adf_semantic=r"[A-Z]{5}",  # OLINS
    prod=r"[A-Z0-9]{3}",  # EFR, CR0
    date=r"[0-9]{8}T[0-9]{6,8}",  # 20160216T000000,
    duration=r"[0-9]{4}",  # 0180
    cycle=r"[0-9]{3}",
    orbit=r"[0-9]{3}",
    consolidation=r"(?:X|T|S)",
    eopf_hash=r"[0-9]{3}",
    processing_center=r"[A-Z0-9]{3}",
    timeliness=r"[A-Z]{2}",
    baseline=r"[0-9]{3}",
)


RE_ADF: re.Pattern[str] = re.compile("S[0-9]{1}[A-Z_]_ADF_[0-9A-Z]{5}")
RE_PRODUCT: re.Pattern[str] = re.compile("S[0-9]{1}[A-Z_]{3}[A-Z0-9_]{3}")

# S3A_OL_0_EFR____20221101T162118_20221101T162318_20221101T180111_0119_091_311______PS1_O_NR_002.SEN3
# S3A_OL_0_CR0____20220511T202328_20220511T202413_20220511T213302_0045_085_142______PS1_O_NR_002.SEN3
RE_PRODUCT_S3_LEGACY = r"_".join(
    [
        RE_PATTERNS["mission1"] + RE_PATTERNS["platform"],
        RE_PATTERNS["sensor_S3L"],
        RE_PATTERNS["level"],
        RE_PATTERNS["prod_S3L"],
        r"_*",  # TODO
        RE_PATTERNS["date"],
        RE_PATTERNS["date"],
        RE_PATTERNS["date"],
        RE_PATTERNS["duration"],
        RE_PATTERNS["cycle"],
        RE_PATTERNS["orbit"],
        r"____",
        RE_PATTERNS["processing_center"],
        RE_PATTERNS["platform"],
        RE_PATTERNS["timeliness"],
        RE_PATTERNS["baseline"] + RE_PATTERNS["ext_L"],
    ],
)

# S3__AX___CLM_AX_20000101T000000_20991231T235959_20151214T120000___________________MPC_O_AL_001.SEN3
# S3A_OL_1_CLUTAX_20160425T095210_20991231T235959_20160525T120000___________________MPC_O_AL_003.SEN3
RE_ADF_S3_LEGACY = (
    r"_".join(
        [
            RE_PATTERNS["mission1"] + RE_PATTERNS["platform"],  # S3_
            RE_PATTERNS["sensor_S3ADFL"],  # OL, AX
            RE_PATTERNS["level_L"],  #
            RE_PATTERNS["adf_S3L"],
            RE_PATTERNS["date"],
            RE_PATTERNS["date"],
            RE_PATTERNS["date"],
            r"_________________",
            RE_PATTERNS["processing_center"],
            RE_PATTERNS["platform"],
            RE_PATTERNS["timeliness"],
            RE_PATTERNS["baseline"],
        ],
    )
) + RE_PATTERNS["ext_L"]

# S2A_MSIL1C_20231001T094031_N0509_R036_T33RUJ_20231002T065101.SAFE",
RE_PRODUCT_S2_LEGACY = (
    (
        r"_".join(
            [
                RE_PATTERNS["mission1"] + RE_PATTERNS["platform"],
                r"MSI" + RE_PATTERNS["level_S2"],
                RE_PATTERNS["date"],
                r".*",
            ],
        )
    )
) + RE_PATTERNS["ext_L"]

# OLCEFR_20230506T015316_0180_B117_T931.zarr
RE_PRODUCT_EOPF_COMMON = (
    "_".join(
        [
            RE_PATTERNS["sensor"] + RE_PATTERNS["prod"],
            RE_PATTERNS["date"],
            RE_PATTERNS["duration"],
            RE_PATTERNS["platform"] + RE_PATTERNS["orbit"],
            RE_PATTERNS["consolidation"] + RE_PATTERNS["eopf_hash"],
        ],
    )
) + RE_PATTERNS["ext"]

# S3OLCEFR_20230506T015316_0180_B117_T931.zarr
RE_PRODUCT_EOPF_LEGACY = RE_PATTERNS["mission1"] + RE_PRODUCT_EOPF_COMMON

# S03OLCEFR_20230506T015316_0180_B117_T931.zarr
RE_PRODUCT_EOPF = RE_PATTERNS["mission2"] + RE_PRODUCT_EOPF_COMMON

# S03OLCEFR_test
RE_PRODUCT_PERMISSIVE = (RE_PATTERNS["mission2"] + RE_PATTERNS["sensor"] + RE_PATTERNS["prod"]) + r"\.*"

# ADF_OLEOP_20160216T000000_20991231T235959_20231030T154253
RE_ADF_EOPF_COMMON: str = (
    "_".join(
        [
            RE_PATTERNS["platform"],
            "ADF",
            RE_PATTERNS["adf_semantic"],
            RE_PATTERNS["date"],
            RE_PATTERNS["date"],
            RE_PATTERNS["date"],
        ],
    )
) + RE_PATTERNS["ext"]

# S3A_ADF_OLEOP_20160216T000000_20991231T235959_20231030T154253.zarr
RE_ADF_EOPF_LEGACY = RE_PATTERNS["mission1"] + RE_ADF_EOPF_COMMON

# S03A_ADF_OLEOP_20160216T000000_20991231T235959_20231030T154253.zarr
RE_ADF_EOPF = RE_PATTERNS["mission2"] + RE_ADF_EOPF_COMMON

# ADF_OLINS_test
RE_ADF_PERMISSIVE = "(?:%s_){0,1}ADF_[A-Z0-9]{5}.*" % (RE_PATTERNS["mission"] + RE_PATTERNS["platform"])


def is_s2_legacy_adf(filename: str) -> bool:
    try:
        PDILogicalFilename.from_string(Path(filename).stem)
    except ValueError:
        return False
    else:
        return True


PATTERNS: dict[L_DataFileNamePattern, str | Callable[..., bool]] = {
    "product/s3-legacy": RE_PRODUCT_S3_LEGACY,
    "product/s2-legacy": RE_PRODUCT_S2_LEGACY,
    "product/eopf": RE_PRODUCT_EOPF,
    "product/eopf-legacy": RE_PRODUCT_EOPF_LEGACY,
    "adf/s3-legacy": RE_ADF_S3_LEGACY,
    "adf/s2-legacy": is_s2_legacy_adf,
    "adf/eopf": RE_ADF_EOPF,
    "adf/eopf-legacy": RE_ADF_EOPF_LEGACY,
    "product/permissive": RE_PRODUCT_PERMISSIVE,
    "adf/permissive": RE_ADF_PERMISSIVE,
}

PATTERN_ORDER: list[L_DataFileNamePattern] = [
    "product/s3-legacy",
    "product/s2-legacy",
    "product/eopf",
    "product/eopf-legacy",
    "adf/s3-legacy",
    "adf/eopf",
    "adf/eopf-legacy",
    # Put permissive patterns at the end to catch it only if all valid patterns has failed
    "adf/s2-legacy",
    "product/permissive",
    "adf/permissive",
]

DETECTION_FUNCTIONS: dict[str, Callable[..., bool]] = {}


def match_pattern(filename: str, pattern: str) -> bool:
    co = re.compile(pattern)
    if co.match(filename):
        return True
    else:
        return False


for fmt, pattern_or_func in PATTERNS.items():
    if isinstance(pattern_or_func, str):
        pattern: str = pattern_or_func

        DETECTION_FUNCTIONS[fmt] = partial(match_pattern, pattern=pattern)
    else:
        func = pattern_or_func
        DETECTION_FUNCTIONS[fmt] = func


def detect_filename_pattern(filename: str) -> L_DataFileNamePattern:
    for fmt in PATTERN_ORDER:
        match = DETECTION_FUNCTIONS[fmt]
        if match(filename):
            return fmt
    return "unknown/unknown"


def two_digit_mission(mission: str) -> str:
    if len(mission) == 3:
        return mission
    elif len(mission) == 2:
        mission_num = int(mission[1:2])
        mission_name = mission[0]
        return "%s%02d" % (mission_name, mission_num)
    else:
        raise ValueError(f"mission {mission!r} is not valid")


def timeliness_to_consolidation(timeliness: str) -> str:
    if timeliness == "NT":
        consolidation = "S"
    elif timeliness == "NR":
        consolidation = "T"
    else:
        consolidation = "_"
    return consolidation


def _convert_semantic(fmt: str, old_semantic: str, **kwargs: Any) -> str:
    legacy_fmts: list[L_DataFileNamePattern] = [
        "adf/s2-legacy",
        "adf/s3-legacy",
        "product/s2-legacy",
        "product/s3-legacy",
    ]
    if fmt in legacy_fmts:
        if "semantic" not in kwargs:
            raise DataSemanticConversionError("Cannot convert legacy 'semantic' to DPR 'semantic'")
        else:
            return kwargs["semantic"]
    else:
        return old_semantic


def _extract_data_from_product_filename(filename: str, **kwargs: Any) -> dict[str, Any]:
    """return a dictionnary containing data extracted from filename.

    Parameters
    ----------
    filename
        filename to parse

    Returns
    -------
        dictionnary with keys compatible with DataFileName constructor
    """
    mission = "???"
    platform = "?"
    semantic = "?????"

    start: datetime = fix_datetime(0)
    stop: datetime = fix_datetime(0)
    orbit_number = -1
    consolidation = "?"
    fmt = detect_filename_pattern(filename)

    if fmt.startswith("product/eopf"):
        # S03OLCEFR_20230506T015316_0180_A117_T931.zarr
        if fmt == "product/eopf-legacy":
            i = 2
        else:
            i = 3
        mission = two_digit_mission(filename[:i])
        platform = filename[i + 28]
        semantic = filename[i : i + 6]  # noqa: E203
        duration = fix_timedelta(int(filename[i + 23 : i + 27]))  # noqa: E203
        orbit_number = int(filename[i + 29 : i + 32])  # noqa: E203
        consolidation = filename[i + 33]
        start = fix_datetime(filename[i + 7 : i + 22])  # noqa: E203
        stop = start + duration

    elif fmt == "product/s2-legacy":
        s2prod = S2MSIL1CProductURI.from_string(filename)
        mission = two_digit_mission(s2prod.mission_id[0:2])
        platform = s2prod.mission_id[-1]
        semantic = s2prod.product_level
        start = fix_datetime(s2prod.product_discriminator_time_str)
        try:
            duration = fix_timedelta(kwargs["duration"])
        except KeyError:
            raise ValueError("Cannot get duration. Please specify duration=<int>")
        orbit_number = int(s2prod.relative_orbit_number[1:])
        consolidation = kwargs.get("consolidation", "T")

    elif fmt == "product/s3-legacy":
        # S3A_OL_0_EFR____20221101T162118_20221101T162318_20221101T180111_0119_091_311______PS1_O_NR_002.SEN3
        mission = two_digit_mission(filename[0:2])
        platform = filename[2]
        old_semantic = filename[4:15]
        semantic = _convert_semantic(fmt, old_semantic, **kwargs)
        start = fix_datetime(filename[16:31])
        stop = fix_datetime(filename[32:47])
        duration = stop - start
        orbit_number = int(filename[73:76])
        consolidation = timeliness_to_consolidation(filename[88:90])
    elif fmt == "product/permissive":
        # S03OLCEFR_test
        mission = filename[0:3]
        semantic = filename[3:9]
        duration = fix_timedelta(0)
    else:
        raise NotImplementedError(fmt)

    return dict(
        mission=mission,
        platform=platform,
        semantic=semantic,
        start=start,
        duration=duration,
        orbit_number=orbit_number,
        consolidation=consolidation,
    )


def _extract_data_from_adf_filename(filename: str, **kwargs: Any) -> dict[str, Any]:
    """return a dictionnary containing data extracted from filename.

    Parameters
    ----------
    filename
        filename to parse

    Returns
    -------
        dictionnary with keys compatible with DataFileName constructor
    """
    mission = "???"
    platform = "?"
    semantic = "?????"

    start: datetime = fix_datetime(0)
    stop: datetime = fix_datetime(0)
    fmt = detect_filename_pattern(filename)
    if fmt == "adf/s2-legacy":
        # S2A_OPER_GIP_BLINDP_MPC__20150605T094736_V20150622T000000_21000101T000000_B00.SAFE
        s2adf = PDILogicalFilename.from_string(Path(filename).stem)
        mission = two_digit_mission(s2adf.mission_id[0:2])
        platform = s2adf.mission_id[-1]
        old_semantic = s2adf.file_class + "_" + s2adf.file_type.file_category + s2adf.file_type.semantic_descriptor
        semantic = _convert_semantic(fmt, old_semantic, **kwargs)
        period = s2adf.instance_id.optional_suffix.applicability_time_period
        if period:
            if isinstance(period["start"], datetime):
                start = period["start"]
            if isinstance(period["stop"], datetime):
                stop = period["stop"]

    elif fmt == "adf/s3-legacy":
        # S3A_OL_1_CLUTAX_20160425T095210_20991231T235959_20160525T120000___________________MPC_O_AL_003.SEN3
        mission = two_digit_mission(filename[0:2])
        platform = filename[2]
        old_semantic = filename[4:15]
        semantic = _convert_semantic(fmt, old_semantic, **kwargs)
        start = fix_datetime(filename[16:31])
        stop = fix_datetime(filename[32:47])
    elif fmt.startswith("adf/eopf"):
        # S03OLCEFR_20230506T015316_0180_A117_T931.zarr
        # S03A_ADF_OLINS_20241231T000102_20241231T000302_20240331T121200.zarr
        if fmt == "adf/eopf-legacy":
            i = 2
        else:
            i = 3
        mission = two_digit_mission(filename[:i])
        platform = filename[i]
        semantic = filename[i + 6 : i + 11]  # noqa: E203
        start = fix_datetime(filename[i + 12 : i + 27])  # noqa: E203
        stop = fix_datetime(filename[i + 28 : i + 43])  # noqa: E203
    else:
        raise NotImplementedError(fmt)

    return dict(
        mission=mission,
        platform=platform,
        semantic=semantic,
        start=start,
        stop=stop,
    )


@dataclass
class SentinelFileNameGenerator(FileNameGenerator):

    mission: str  # MMM. For example S03
    platform: str  # For example A, _
    semantic: str  # XXXXXX. For example OLINS, OLCEFR
    fmt: L_DataFileNamePattern

    def __post_init__(self) -> None:
        self.mission = self.mission.upper()
        self.mission = two_digit_mission(self.mission)
        self.platform = self.platform.upper()

    def stac(self) -> dict[str, Any]:
        """Generate STAC metadata from attributes"""
        stac = {
            "eopf:type": self.semantic,
            "platform": f"sentinel-{self.mission[-1]}{self.platform.lower()}",
        }
        return stac


@dataclass(kw_only=True)
class ProductFileNameGenerator(SentinelFileNameGenerator):
    """
    Sentinel Product File Name Generator
    """

    start: datetime
    duration: timedelta
    orbit_number: int
    consolidation: str

    suffix: str = ""
    fmt: L_DataFileNamePattern = "product/eopf"

    @staticmethod
    def new(
        mission: str,
        platform: str,
        semantic: str,
        start: T_DateTime,
        duration: T_TimeDelta,
        orbit_number: int | None = None,
        consolidation: str | None = None,
        suffix: str = "",
        **kwargs: Any,
    ) -> "ProductFileNameGenerator":
        """
        >>> prod_name_gen = ProductFileNameGenerator.new("s3", "a", "OLCEFR", "20241231T000000", 120, 311, "T")
        >>> prod_name_gen.to_string(hash="123")
        'S03OLCEFR_20241231T000000_0120_A311_T123.zarr'

        Parameters
        ----------
        mission
            is the owner mission (e.g. "S1", "S2", ... "S0" for any mission. two-digit is also allowed: "S03")
        platform
            is the satellite id. For example, "A", "B". Use "_" if not specified
        semantic
            is a code related to the data theme. SSSCCC <sensor><code> for example OLCEFR
        start
            is the observation start time (str like 20170810T150000 or datetime.datetime)
        duration
            is the duration of observation in seconds
        orbit_number, optional
            by default None
        consolidation, optional
            by default None
        suffix, optional
            user suffix, by default ""

        Returns
        -------
            _description_
        """
        if orbit_number is None:
            orbit_number = -1
        if consolidation is None:
            consolidation = "?"
        return ProductFileNameGenerator(
            mission=mission,
            platform=platform,
            semantic=semantic,
            start=fix_datetime(start),
            duration=fix_timedelta(duration),
            orbit_number=orbit_number,
            consolidation=consolidation,
            suffix=suffix,
        )

    @staticmethod
    def from_string(filename: str, **kwargs: Any) -> "ProductFileNameGenerator":
        """
        Generate a FileNameGenerator from filename string.
        If filename is a legacy filename, you must specify `semantic` to specify the new format semantic.

        For example:

        >>> legacy_name = "S3A_OL_0_EFR____20221101T162118_20221101T162318_20221101T180111_0119_091_311______PS1_O_NR_002.SEN3" # noqa: E501
        >>> filegen = ProductFileNameGenerator.from_string(legacy_name, semantic="OLCEFR")
        >>> filegen.semantic
        'OLCEFR'
        """
        data = _extract_data_from_product_filename(filename, **kwargs)
        return ProductFileNameGenerator(**data)

    def is_valid(self) -> bool:
        """
        return True if all required data are set, else retrun False
        """
        valid: bool = True
        valid = valid and self.platform.lower() in ascii_letters
        valid = valid and self.duration.total_seconds() >= 0
        valid = valid and self.orbit_number >= 0
        valid = valid and self.consolidation != "?"
        return valid

    def to_string(
        self,
        extension: str = ".zarr",
        hash: int = 0,
        creation_date: T_DateTime | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate a filename

        Parameters
        ----------
        extension, optional
            filename extension, by default ".zarr"
        hash, optional
            quasi-unique hexadecimal number (0..9,A..F),
            like a CRC checksum (to avoid overwriting files in case of reprocessing action)
        creation_date, optional
            creation_date: by default, use current time

        Returns
        -------
            valid sentinel file name

        """
        # S03OLCEFR_20230506T015316_0180_B117_T931.zarr
        return "_".join(
            [
                f"{self.mission}{self.semantic}",
                f"{self.start.strftime(DATE_FORMAT)}",
                f"{self.duration.seconds:04}",
                f"{self.platform}{self.orbit_number:03}",
                f"{self.consolidation}{hash:03}{self.suffix}{extension}",
            ],
        )

    def stac(self) -> dict[str, Any]:
        """Generate STAC metadata from attributes"""
        stac = super().stac()
        if self.consolidation == "T":
            timeline = "NRT"
        elif self.consolidation == "_":
            timeline = "STC"
        elif self.consolidation == "S":
            timeline = "NTC"
        else:
            timeline = None
        stac["start_datetime"] = self.start.strftime(DATE_FORMAT)
        stac["end_datetime"] = (self.start + self.duration).strftime(DATE_FORMAT)
        stac["sat:relative_orbit"] = str(self.orbit_number)
        if timeline:
            stac["eopf:timeline"] = timeline
        return stac


@dataclass(kw_only=True)
class AdfFileNameGenerator(SentinelFileNameGenerator):
    """
    Sentinel Product File Name Generator:
    """

    start: datetime
    stop: datetime
    suffix: str = ""
    fmt: L_DataFileNamePattern = "adf/eopf"

    @staticmethod
    def new(
        mission: str,
        platform: str,
        semantic: str,
        start: T_DateTime,
        stop: T_DateTime = "20991231T235959",
        suffix: str = "",
        **kwargs: Any,
    ) -> "AdfFileNameGenerator":
        """
        >>> adf_name = AdfFileNameGenerator.new("s3", "a", "OLINS", datetime(2024, 12, 31, 0, 1, 2))
        >>> adf_name.to_string(creation_date="20240327T115758")
        'S03A_ADF_OLINS_20241231T000102_20991231T235959_20240327T115758.zarr'

        Parameters
        ----------
        mission
            is the owner mission (e.g. "S1", "S2", ... "S0" for any mission. two-digit is also allowed: "S03")
        platform
            is the satellite id. For example, "A", "B". Use "_" if not specified
        semantic
            is a code related to the data theme. SSCCC <sensor><code> for example OLINS
        start
            is the validity start time (str like 20170810T150000 or datetime.datetime)
        stop, optional
            is the validity stop time (str like 20170810T150000 or datetime.datetime), by default "20991231T235959"
        suffix, optional
            user suffix, by default ""

        Returns
        -------
            _description_
        """
        return AdfFileNameGenerator(
            mission=mission,
            platform=platform,
            semantic=semantic,
            start=fix_datetime(start),
            stop=fix_datetime(stop),
            suffix=suffix,
        )

    @staticmethod
    def from_string(filename: str, **kwargs: Any) -> "AdfFileNameGenerator":
        """
        Generate a FileNameGenerator from filename string.
        If filename is a legacy filename, you must specify `semantic` to specify the new format semantic.
        """
        data = _extract_data_from_adf_filename(filename, **kwargs)
        return AdfFileNameGenerator(**data)

    def is_valid(self) -> bool:
        """
        return True if all required data are set, else retrun False
        """
        duration = fix_datetime(self.stop) - fix_datetime(self.start)
        valid: bool = True
        valid = valid and self.platform.lower() in ascii_letters
        valid = valid and duration.total_seconds() >= 0
        return valid

    def to_string(
        self,
        extension: str = ".zarr",
        hash: int = 0,
        creation_date: T_DateTime | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate a filename

        Parameters
        ----------
        extension, optional
            filename extension, by default ".zarr"
        hash, optional
            quasi-unique hexadecimal number (0..9,A..F),
            like a CRC checksum (to avoid overwriting files in case of reprocessing action)
        creation_date, optional
            creation_date: by default, use current time

        Returns
        -------
            valid sentinel file name

        """
        # S03A_ADF_OLEOP_20160216T000000_20991231T235959_20231030T154253.zarr
        if creation_date is None:
            creation = datetime.now()
        else:
            creation = fix_datetime(creation_date)
        return "_".join(
            [
                f"{self.mission}{self.platform}",
                "ADF",
                f"{self.semantic}",
                f"{self.start.strftime(DATE_FORMAT)}",
                f"{self.stop.strftime(DATE_FORMAT)}",
                f"{creation.strftime(DATE_FORMAT)}{self.suffix}{extension}",
            ],
        )


def filename_generator(filename: str, **kwargs: Any) -> FileNameGenerator:
    fmt = detect_filename_pattern(filename)
    if fmt.startswith("product"):
        return ProductFileNameGenerator.from_string(filename)
    elif fmt.startswith("adf"):
        return AdfFileNameGenerator.from_string(filename)
    else:
        raise NotImplementedError
