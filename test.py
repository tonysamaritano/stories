import stories.schemas as st

character: st.Character = st.Character(
    name="Claudine",
    motivation="wants to be the greatest samurai in the world",
    appearance="small female orange and white tabby cat",
    backstory="a fighter always looking for a challenge",
    development="learns to be become a disciplined samurai",
    gender=st.Gender.female,
    personality=[
        st.Personality.Ambitious, st.Personality.Cunning, st.Personality.Fierce
    ],
    role=[st.Role.Protagonist])

if st.Gender.female == character.gender:
    pronoun = ("she", "her")
elif st.Gender.male == character.gender:
    pronoun = ("he", "his")
else:
    pronoun = ("they", "their")

plot = st.ThreeActPlot(
    setup=f"{character.name}'s motivation is {pronoun[0]} {character.motivation}.",
    confrontation=f"{character.name} overcomes a great challenge.",
    resolution=f"{character.name}'s challege helps he character develop into {character.development}."
)

setting = st.Setting(
    location="a small village in the mountains of Japan",
    time="the 18th century")

scene = st.Scene(
    characters=[character],
    conflict=[st.Conflict.AgentVsSelf],
    setting=setting,
    emotion=[st.Emotion.happy, st.Emotion.serious],
    structure=plot)

print(scene.json(indent=4))

print(f"""Write a story where {character.name} is the {character.role[0].value.lower()} and {pronoun[0]} is \
a part of a three act plot. The setup is: {plot.setup} The confrontation is: {plot.confrontation} and the resolution \
is {plot.resolution}. {character.name} is in {setting.location} in {setting.time}. \
{character.name} is {character.appearance} and {pronoun[1]} personality is: \
{', '.join([p.value.lower() for p in character.personality])}. {character.name}'s backstory \
is: {character.backstory}. {character.name}'s character development is: {character.development}.""")