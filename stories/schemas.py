from enum import Enum
from typing import List, Union, Optional

from pydantic import BaseModel


class Emotion(Enum):
    happy = "happy"
    sad = "sad"
    angry = "angry"
    scared = "scared"
    love = "love"
    jealous = "jealous"
    serious = "serious"


class Gender(Enum):
    male = "male"
    female = "female"
    nonbinary = "nonbinary"


class Conflict(Enum):
    internal = "internal"
    external = "external"
    AgentVsSelf = "AgentVsSelf"
    AgentVsAgent = "AgentVsAgent"
    AgentVsSociety = "AgentVsSociety"
    AgentVsNature = "AgentVsNature"


class Personality(Enum):
    Ambitious = "Ambitious"
    Arrogant = "Arrogant"
    Brave = "Brave"
    Calculating = "Calculating"
    Charming = "Charming"
    Cowardly = "Cowardly"
    Cunning = "Cunning"
    Devious = "Devious"
    Determined = "Determined"
    Energetic = "Energetic"
    Envious = "Envious"
    Fearless = "Fearless"
    Fierce = "Fierce"
    Generous = "Generous"
    Greedy = "Greedy"
    Handsome = "Handsome"
    Humble = "Humble"
    Impatient = "Impatient"
    Jealous = "Jealous"
    Kind = "Kind"
    Lazy = "Lazy"
    Loyal = "Loyal"
    Mischievous = "Mischievous"
    Nervous = "Nervous"
    Outgoing = "Outgoing"
    Patient = "Patient"
    Persistent = "Persistent"
    Resourceful = "Resourceful"
    Selfish = "Selfish"
    Sly = "Sly"
    Strong = "Strong"
    Thoughtful = "Thoughtful"
    Trustworthy = "Trustworthy"
    Vain = "Vain"
    Witty = "Witty"


class Role(Enum):
    Protagonist = "Protagonist"
    Antagonist = "Antagonist"
    Supporting = "Supporting"
    Narrator = "Narrator"


class PlotStructure(Enum):
    ThreeAct = "ThreeAct"
    FiveAct = "FiveAct"
    SevenAct = "SevenAct"
    HeroJourney = "HeroJourney"


class Character(BaseModel):
    name: str
    motivation: str
    appearance: str
    personality: List[Personality]
    role: List[Role]
    backstory: str
    development: str
    gender: Gender


class Action(BaseModel):
    action: str
    character: Character
    emotion: List[Emotion]


class ThreeActPlot(BaseModel):
    setup: str
    confrontation: str
    resolution: str


class FiveActPlot(ThreeActPlot):
    incitingIncident: str
    development: str


class SevenActPlot(FiveActPlot):
    turn: str
    aftermath: str


class HeroJourneyPlot(BaseModel):
    call: str
    refusal: str
    mentor: str
    threshold: str
    test: str
    cave: str
    ordeal: str
    reward: str
    roadBack: str
    returnHome: str


class Dialogue(BaseModel):
    characters: List[Character]  # id of character
    subtext: List[Emotion]
    purpose: str
    content: List[str]
    dialogue: List[str]


class Setting(BaseModel):
    location: str
    time: str
    details: Optional[List[str]]


class Scene(BaseModel):
    characters: List[Character]
    conflict: Optional[List[Conflict]]
    action: Optional[List[Action]]
    emotion: List[Emotion]
    scenes: list = []  # this is a list of scenes
    structure: Union[ThreeActPlot, FiveActPlot, SevenActPlot, HeroJourneyPlot]
    dialogue: Optional[List[Dialogue]]  # allows for multiple dialogues in a scene
    setting: Setting  # I don't think this would need to be a list
