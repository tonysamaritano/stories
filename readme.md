# Pet Legendary Backend

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

env vars:

```
SUPERUSER_EMAIL
STRIPE_API_KEY
GOOGLE_CLIENT_ID
JWT_SECRET_KEY
JWT_ALGORITHM
DATABASE_URL
```

## Goal

The general goal of this backend is to provide an API for a generic artwork request and delivery marketplace. An example of this is the [Pet Legendary](https://www.petlegendary.com) website.

This needs to be generic enough to cover a story as simple as what I'm creating today all the way to a multi-season, complex storyline like Breaking Bad. Why? This technology can be used in the future to generate on-demand, customized content.

## Features

- User authentication
- User profile
- Artist Profiles (e.g. Anime Artist, Portrait Artist, etc.)
- Subjects (e.g. Pet, Person, Idea etc.)
  - Description
  - Adjectives
  - Images
- Scene
  - Plot Description
  - Subjects
    - Tags for each subject
- Story
  - Plot Description
  - Scenes

- Plot Point
  - Title
  - Genre
  - Description
  - Charactors[]
    - Actor
    - Description
  - Location
  - S

- Scene
  - Link to Plot Point
  - Setting
  - Action
  - Characters


## Example:

- [ ] how do you create parallel scenes?

```json
{
    "id": 1, // root node
    "plot_point":
        {
            "id": 0,
            "description": "A cat becomes a samurai.",
        },
    "title": "A cat becomes a samurai.",
    "characters": [
        {
            "id": 1,
            "name": "Kitty",
            "description": "A scrappy stray cat."
        },
        {
            "id": 2,
            "name": "Samurai",
            "description": "A kind old samurai."
        }
    ],
    "plots": [
        {
            "id": 2, // branch
            "plot_point":
            {
                "id": 1,
                "description": "The cat, who is a stray living on the streets, is taken in by a kind old samurai who sees potential in the feline's natural agility and quick reflexes.",
            },
            "title": "Scene 1",
            "characters": [
                {
                    "id": 1,
                    "name": "Kitty",
                    "description": "A scrappy stray cat."
                },
                {
                    "id": 2,
                    "name": "Samurai",
                    "description": "A kind old samurai."
                },
                {
                    "id": 3,
                    "name": "Wise old man",
                    "description": "A kind old samurai."
                }
            ],
            "plots": [
                {
                    "id": 9, // leaf node
                    "title": "Scene 1a",
                    "characters": [], // adopt
                    "plots": [], // leaf of the node
                    "description": "Kitty huddled under the awning of a small shop, trying to stay dry in the pouring rain. She had been living on the streets for as long as she could remember, scavenging for scraps and dodging the dangers of city life.",
                },
                {
                    "id": 10,
                    "title": "Scene 1b",
                    "characters": [],
                    "plots": [],
                    "description": "As the rain continued to fall, a kind old samurai approached, his face creased with concern as he saw the bedraggled cat huddled on the street. He reached out and gently stroked Kitty's head, and she looked up at him with wide, trusting eyes.",
                },
                {
                    "id": 11,
                    "title": "Scene 1c",
                    "characters": [],
                    "plots": [],
                    "description": "The old samurai, seeing the potential in Kitty's natural agility and quick reflexes, decided to take her in and train her in the way of the samurai. He brought her back to his home and began teaching her sword fighting techniques and the code of honor that guided the samurai's actions.",
                },
                {
                    "id": 12,
                    "title": "Scene 1d",
                    "characters": [],
                    "plots": [],
                    "description": "Kitty, grateful for the kindness and shelter of her new master, devoted herself to her training, determined to prove herself worthy of the samurai's trust. And so, under the guidance of the old samurai, Kitty began her journey towards becoming a true samurai warrior.",
                },
            ],
        },
    ],
}

```


## Breakdown of a Scene:

A scene in a storyline typically consists of the following components:

- **Characters:** The people or other beings who are present in the scene and participate in the action.
- **Setting:** The location where the scene takes place and any relevant details about the environment.
- **Dialogue:** The conversation or other exchanges of words between the characters in the scene.
- **Action:** The physical actions and events that take place in the scene.
- **Plot:** The events and actions in the scene that contribute to the overall storyline.
- **Emotion:** The feelings and emotions of the characters in the scene, as well as any sensory details that help convey a sense of mood or atmosphere.
- **Conflict:** The problem or obstacle that the characters in the scene are trying to overcome or resolve.

> Not every scene will necessarily include all of these components, and the relative emphasis on each component will vary depending on the needs of the story.

### Characters

Characters are the people or other beings that populate a story and participate in the action. Characters are an essential element of a story, as they are the ones who experience the events of the plot and drive the action forward.

There are several elements to consider when creating characters:

- Personality: The characteristics and traits that define a character's personality, such as their values, beliefs, habits, and quirks.
- Appearance: The physical characteristics of a character, including their age, gender, ethnicity, and other details that help to define their appearance.
- Motivation: The driving force behind a character's actions and decisions. What do they want, and why?
- Goals: The things that a character is striving to achieve or accomplish.
- Conflict: The problems or obstacles that a character must overcome in order to achieve their goals.
- Development: The changes or growth that a character experiences over the course of the story.

It's important to create well-rounded and believable characters in a story, as they are the ones who will engage the reader or viewer and help to convey the themes and message of the story.

#### Features of a Character

- Name: A character's name is an important element of their identity and can reveal information about their background, culture, and personality. A character's name should be appropriate for the time and place in which the story takes place and should be memorable and distinctive.
- Motivation: Motivation refers to the driving force behind a character's actions and decisions. It's important to consider a character's motivation when creating them, as it helps to define their goals and desires and reveals important information about their personality and values. A character's motivation can change over the course of the story as they experience new events or challenges.
- Appearance: The physical characteristics of a character, including their age, gender, ethnicity, and other details that help to define their appearance.
- Personality: The characteristics and traits that define a character's personality, such as their values, beliefs, habits, and quirks.
- Relationship to other characters: The way in which a character relates to other characters in the story, including family, friends, enemies, and allies.
- Role in the story: The purpose or function that a character serves in the story, such as a protagonist, antagonist, supporting character, or narrator.
- Backstory: The events and experiences that have shaped a character's past and influenced their present circumstances.
- Development: The changes or growth that a character experiences over the course of the story.

### Setting

In the context of a story, the setting refers to the location and time period in which the story takes place. The setting can have a significant impact on the characters, plot, and themes of story, and it can help to establish the mood and atmosphere.

The setting includes both the physical location where the story takes place, as well as any relevant details about the environment. For example, the setting of a story might be a small town in the countryside, a bustling city, or a distant planet. It could also include details about the time period, such as the era in which the story takes place, or the season or weather.

The setting can influence the characters' actions, thoughts, and behaviors, and it can also reveal important information about the culture, society, or values of the time and place in which the story takes place.

It's important to consider the setting when writing a story, as it can help to immerse the reader or viewer in the world of the story and provide a sense of realism and authenticity.

### Dialogue

Dialogue refers to the conversation or exchanges of words between characters in a story. Dialogue serves several purposes in a story: it can reveal information about the characters and the plot, it can convey the characters' emotions and personalities, and it can help to move the story forward.

There are several elements to consider when writing dialogue:

- Content: The words and ideas that are being expressed by the characters.
- Delivery: The way in which the words are spoken, including the tone of voice, inflection, and pace.
- Subtext: The underlying meaning or emotions that are conveyed through the dialogue, even if they are not explicitly stated.
- Purpose: The reason why the characters are speaking and what they hope to achieve through their conversation.

It's important to keep in mind that dialogue should sound natural and believable, and it should be appropriate for the characters and the context in which it is spoken. It's also important to consider how the dialogue will advance the story or reveal important information about the characters.

### Action

In the context of a scene in a storyline, an action refers to any physical activity or event that takes place. This could include things like a character moving around, using objects, or interacting with other characters or the environment.

For example, an action might be a character opening a door, picking up a book, or driving a car. Actions can also include nonverbal behaviors, such as facial expressions or gestures.

The purpose of an action in a scene is to convey information to the reader or viewer and to advance the plot or character development. An action can reveal a character's personality, intentions, or motivations, and it can also create tension or conflict, move the story forward, or reveal important plot points.

### Plot

In the context of a story, the plot is the series of events and actions that make up the story. The plot includes the main events of the story as well as any subplots or supporting events that help to advance the story or develop the characters.

The plot of a story typically has a beginning, middle, and end, and it includes a series of conflicts or problems that the characters must overcome in order to achieve their goals. The plot also includes rising and falling action, which refers to the build-up and resolution of tension or conflict.

There are several elements that are typically included in the plot of a story:

- Exposition: This is the part of the story that introduces the characters, setting, and background information.
- Rising action: This is the part of the story where the conflict or problem is introduced and the characters start working to overcome it.
- Climax: This is the point of greatest tension or conflict in the story, where the outcome of the story is uncertain.
- Falling action: This is the part of the story where the conflict or problem is resolved and the characters achieve their goals or come to a resolution.
- Resolution: This is the part of the story where the story's events are brought to a close and the characters' fates are revealed.

The plot is an essential element of a story because it provides the structure and direction for the story and keeps the reader or viewer engaged. It helps to convey the characters' motivations and desires and reveals important information about the story's themes and message.

#### Act Structures

Some popular plot structures

- The three-act structure
- The hero's journey
- The five-act structure
- The seven-act structure

**The three-act structure:** This is a common plot structure that is often used in plays, movies, and novels. It consists of three parts: the setup, the confrontation, and the resolution. The setup introduces the characters, setting, and background information. The confrontation is the main action of the story, where the conflict or problem is introduced and the characters work to overcome it. The resolution is the part of the story where the conflict is resolved and the characters' fates are revealed.

**The hero's journey:** This is a plot structure that was popularized by Joseph Campbell and is often used in epic stories or myths. It consists of a series of steps that a hero must go through in order to complete a journey and achieve a goal. The steps of the hero's journey include the call to adventure, the refusal of the call, the meeting with the mentor, the crossing of the threshold, the tests and challenges, the innermost cave, the supreme ordeal, the reward, the road back, and the return home.

**The five-act structure:** This is a plot structure that was popularized by Aristotle and is often used in plays and movies. It consists of five parts: the exposition, the rising action, the climax, the falling action, and the resolution. The exposition introduces the characters, setting, and background information. The rising action is the part of the story where the conflict or problem is introduced and the characters start working to overcome it. The climax is the point of greatest tension or conflict in the story, where the outcome of the story is uncertain. The falling action is the part of the story where the conflict or problem is resolved and the characters achieve their goals or come to a resolution. The resolution is the part of the story where the story's events are brought to a close and the characters' fates are revealed.

**The seven-act structure:** This is a plot structure that is often used in movies and consists of seven parts: the setup, the inciting incident, the development, the turn, the confrontation, the resolution, and the aftermath. The setup introduces the characters, setting, and background information. The inciting incident is the event that sets the plot in motion. The development is the part of the story where the conflict or problem is introduced and the characters start working to overcome it. The turn is the point in the story where something changes or takes an unexpected turn. The confrontation is the point of greatest tension or conflict in the story, where the outcome of the story is uncertain. The resolution is the part of the story where the conflict or problem is resolved and the characters achieve their goals or come to a resolution. The aftermath is the part of the story where the characters reflect on the events of the story and the consequences of their actions.

### Emotion

Emotion refers to the feelings and emotional states that characters experience in a story. Emotion is an important element of storytelling because it helps to convey the inner experience of characters and helps the reader or viewer to connect with them on a deeper level.

Emotion can be conveyed through a character's words, actions, and behaviors, as well as through sensory details that help to create a sense of mood or atmosphere. For example, a character who is feeling sad might speak in a low, monotone voice, avoid eye contact, and hunch their shoulders, while a character who is feeling happy might speak more animatedly, make eye contact, and stand up straight.

There are many different emotions that characters can experience in a story, including happiness, sadness, anger, fear, love, and jealousy, among others. The specific emotions that a character experiences will depend on the events and actions that take place in the story, as well as the character's personality and background.

In addition to conveying the inner experience of characters, emotion can also be used to create tension, advance the plot, or reveal important information about a character's motivations and desires

### Conflict

Conflict refers to a problem or obstacle that a character or group of characters must overcome in order to achieve a goal or move the story forward. Conflict is a fundamental element of storytelling, as it provides the tension and drama that keeps the reader or viewer engaged.

There are several types of conflict that can occur in a story:

- Internal conflict: This refers to a conflict that takes place within a character's mind or emotions. An internal conflict might be a character struggling with a difficult decision or grappling with conflicting desires or values.
- External conflict: This refers to a conflict that takes place between a character and an external force, such as another character, a natural disaster, or societal expectations. An external conflict might be a character trying to achieve a goal that is opposed by another character or group.
- Man vs. self: This type of conflict occurs when a character is in conflict with themselves, struggling with their own thoughts, feelings, or desires.
- Man vs. man: This type of conflict occurs when two or more characters are in direct opposition to each other.
- Man vs. society: This type of conflict occurs when a character is in conflict with the rules, norms, or expectations of the society in which they live.
- Man vs. nature: This type of conflict occurs when a character is in conflict with the natural world, such as trying to survive in a harsh environment or dealing with a natural disaster.

Conflict is an essential element of storytelling because it creates tension and drives the plot forward. It can also reveal important information about a character's motivations, desires, and personality.

```python

class Emotion(Enum):
    happy = "happy"
    sad = "sad"
    angry = "angry"
    scared = "scared"
    love = "love"
    jealous = "jealous"

class Conflict(Enum):
    internal = "internal"
    external = "external"
    AgentVsSelf = "AgentVsSelf"
    AgentVsAgent = "AgentVsAgent"
    AgentVsSociety = "AgentVsSociety"
    AgentVsNature = "AgentVsNature"

class Action:
    action: str
    character: int # id of character
    emotion: List[Emotion]

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

class Character:
    name: str
    motivation: str
    appearance: str
    personality: List[Personality]
    relationship: List[Character]
    role: List[Role]
    backstory: str
    development: str

class PlotStructure(Enum):
    ThreeAct = "ThreeAct"
    FiveAct = "FiveAct"
    SevenAct = "SevenAct"
    HeroJourney = "HeroJourney"

class Plot:
    structure: PlotStructure
    plot: str # this should be a json object

class ThreeActPlot:
    setup: str
    confrontation: str
    resolution: str

class FiveActPlot(ThreeActPlot):
    incitingIncident: str
    development: str

class SevenActPlot(FiveActPlot):
    turn: str
    aftermath: str

class HeroJourneyPlot:
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

class Dialogue:
    characters: List[Character] # id of character
    subtext: List[Emotion]
    purpose: str
    content: List[str]
    dialogue: List[str]

class Setting:
    location: str
    time: str
    details: List[str]

class Plot:
    characters: List[Character]
    conflict: List[Conflict]
    action: List[Action]
    emotion: List[Emotion]
    plot: List[Plot]
    structure: Union[ThreeActPlot, FiveActPlot, SevenActPlot, HeroJourneyPlot] # can expand this to include other plot structures
    dialogue: List[Dialogue] # allows for multiple dialogues in a scene
    setting: Setting # I don't think this would need to be a list
```