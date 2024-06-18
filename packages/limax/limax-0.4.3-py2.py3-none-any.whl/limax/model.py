"""Models for LiMAx data."""

from typing import Any, Dict, List

import pandas as pd
from pydantic import BaseModel, Field


class LXMetaData(BaseModel):
    """LiMAx metadata.

    0 # mID 102
    1 # 'doc' (, )
    2 # Dr. Max Mustermann
    3 # 01.01.2010 08:30
    4 # utouARg
    5 # 160 cm
    6 # 70 kg
    7 # 43,295187
    8 # 44,395187
    9 # 630,0
    10 # Nahrungskarenz: über 3 Std., Raucher: Nein, Sauerstoff: Nein, Beatmung: Nein, Medikation: Ja
    """

    mid: str
    datetime: str = Field(repr=True)
    height: float = Field(description="Height in [cm]")
    weight: float = Field(description="Weight in [kg]")
    sex: str = Field(description="Sex in {M, F, NA}")
    smoking: bool = Field(description="Smoking status")
    oxygen: bool = Field(repr=True)
    ventilation: bool = Field(repr=True)
    medication: bool = Field(repr=True)
    food_abstinence: str = Field(repr=True)
    values: List[float] = Field(repr=True)
    comments: List[str] = Field(repr=False)


class LXData(BaseModel):
    """LiMAx data."""

    time: List[float]
    dob: List[float]
    error: List[str]

    def to_df(self) -> pd.DataFrame:
        """Get pandas DataFrame representation."""
        d: Dict[str, Any] = {
            "time": self.time,
            "dob": self.dob,
            "error": self.error,
        }
        df = pd.DataFrame(d)
        df = df[["time", "dob", "error"]]
        # make columns numeric
        # df = pd.to_numeric(df)
        # print(df.head())

        # sort by time (some strange artefacts in some files)
        df.sort_values(by=["time"], inplace=True)
        return df


class LX(BaseModel):
    """LiMAx DOB curve."""

    metadata: LXMetaData
    data: LXData = Field(repr=False)

    model_config: Dict = {"arbitrary_types_allowed": True}

    def to_df(self) -> pd.DataFrame:
        """Convert to DOB dataframe."""
        return self.data.to_df()
