import json

from groq import Groq, GroqError
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Optional

from env import GROQ_API_KEY

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

groq = Groq(api_key=GROQ_API_KEY)


class ResponseModel(BaseModel):
    title: str
    story: str
    word_count: int


def call_groq_api(
    character_type="Human",
    character_name="Alex",
    character_age="Child",
    character_personality="Brave",
    sidekick="a loyal dog",
    story_genre="Adventure",
    story_tone="Lighthearted",
    story_theme="Friendship",
    story_setting="Enchanted Forest",
    story_cultural_context="Fairy tales",
    story_goal_or_conflict="Finding a hidden treasure",
    story_challenges="Riddles and puzzles",
    story_powers="Super strength",
    story_learning_focus="Kindness",
    story_emotional_focus="Overcoming fears",
    story_ending_type="Happy",
    story_resolution_type="Adventure ends successfully",
    language_complexity="Medium",
    antagonist_type="Mischievous goblin",
    antagonist_name="Grizzle",
    user_personalization_animals="Dog",
    user_personalization_activities="Exploring",
    user_personalization_colors="Blue",
    length="200-500",
):
    try:
        context_for_llm = f"""
        The purpose of this story generation is to create a personalized and engaging children's story tailored to the preferences of a young reader. The story should be imaginative, age-appropriate, and capture the child's attention through relatable characters, a simple but engaging plot, and a meaningful moral or lesson. The tone can vary from lighthearted to mildly suspenseful based on the specified genre and theme, but the story should remain suitable for young readers.

        Key elements to incorporate include:

        1. **Relatable Characters**: The main character should embody positive traits that resonate with young readers, such as bravery, kindness, or curiosity. Supporting characters like sidekicks or friends enhance the story by adding companionship and support.
        Adventure and Challenges: The story's plot should include a clear goal and some gentle challenges to create suspense and excitement while reinforcing the lesson or moral.
        2. **Cultural Influence**: When requested, incorporate subtle cultural or folkloric elements to broaden the child's world and foster curiosity about diverse backgrounds.
        3. **Personalization**: Pay attention to the child's favorite animals, colors, and activities to ensure the story feels personalized, relatable, and fun.
        The final story should feel both entertaining and educational, sparking curiosity, empathy, and joy in the young reader while nurturing their love for storytelling.
        4. **Word Count**: The specified word count range ensures the story is engaging and detailed enough to captivate the reader without being too lengthy or complex for the intended age group.

        The **JSON** schema for this task is as follows, adhere to the structure when generating the story:
        f{json.dumps(ResponseModel.model_json_schema(), indent=2)}
        """

        prompt_for_llm = f"""
        Write a children's story based on the following specifications with a title that captures the essence of the narrative:
        
        1.  **Main Character**: A {character_type} named {character_name}, who is a {character_age} with a {character_personality} personality.
        2.  **Supporting Character**: {sidekick} accompanies the main character.
        3.  **Genre and Tone**: This story is a {story_genre} with a {story_tone} tone, focusing on themes of {story_theme}.
        4.  **Setting**: The story takes place in {story_setting}, with cultural or folkloric influences from {story_cultural_context}.
        5.  **Goal/Conflict**: The main character's goal is {story_goal_or_conflict}, but they face challenges like {story_challenges} along the way.
        6.  **Antagonist**: They encounter a {antagonist_type} named {antagonist_name}, who tries to prevent them from achieving their goal.
        7.  **Special Powers/Abilities**: The main character has {story_powers} that help them on their journey.
        8.  **Learning/Moral Focus**: The story includes a moral about {story_learning_focus}, with an emphasis on {story_emotional_focus}.
        9.  **Story Complexity**: The narrative should be suitable for a {language_complexity} reading level.
        10. **Ending and Resolution**: Conclude with a {story_ending_type} ending where {story_resolution_type}.

        11. **Length**: The story should be approximately {length} words.

        For personalization:
        - The main character should resemble a child's interest in animals like {user_personalization_animals}, enjoy activities like {user_personalization_activities}, and prefer colors like {user_personalization_colors}.
        """

        chat = groq.chat.completions.create(
            messages=[
                {"role": "system", "content": context_for_llm},
                {"role": "user", "content": prompt_for_llm},
            ],
            model="llama3-8b-8192",
            temperature=0,
            stream=False,
            response_format={"type": "json_object"},
        )

        validated_output = ResponseModel.model_validate_json(
            chat.choices[0].message.content
        )
        print(validated_output.model_dump_json(indent=2))

        return validated_output
    except GroqError as e:
        print(e)
        return str(e)


@app.post("/story")
def generate_story(
    character_type: str = Form("Human"),
    character_name: str = Form("Alex"),
    character_age: str = Form("Child"),
    character_personality: str = Form("Brave"),
    sidekick: str = Form("a loyal dog"),
    story_genre: str = Form("Adventure"),
    story_tone: str = Form("Lighthearted"),
    story_theme: str = Form("Friendship"),
    story_setting: str = Form("Enchanted Forest"),
    story_cultural_context: str = Form("Fairy tales"),
    story_goal_or_conflict: str = Form("Finding a hidden treasure"),
    story_challenges: str = Form("Riddles and puzzles"),
    story_powers: str = Form("Super strength"),
    story_learning_focus: str = Form("Kindness"),
    story_emotional_focus: str = Form("Overcoming fears"),
    story_ending_type: str = Form("Happy"),
    story_resolution_type: str = Form("Adventure ends successfully"),
    language_complexity: str = Form("Medium"),
    antagonist_type: str = Form("Mischievous goblin"),
    antagonist_name: str = Form("Grizzle"),
    user_personalization_animals: str = Form("Dog"),
    user_personalization_activities: str = Form("Exploring"),
    user_personalization_colors: str = Form("Blue"),
    length: str = Form("200-500"),
):
    return call_groq_api(
        character_type=character_type,
        character_name=character_name,
        character_age=character_age,
        character_personality=character_personality,
        sidekick=sidekick,
        story_genre=story_genre,
        story_tone=story_tone,
        story_theme=story_theme,
        story_setting=story_setting,
        story_cultural_context=story_cultural_context,
        story_goal_or_conflict=story_goal_or_conflict,
        story_challenges=story_challenges,
        story_powers=story_powers,
        story_learning_focus=story_learning_focus,
        story_emotional_focus=story_emotional_focus,
        story_ending_type=story_ending_type,
        story_resolution_type=story_resolution_type,
        language_complexity=language_complexity,
        antagonist_type=antagonist_type,
        antagonist_name=antagonist_name,
        user_personalization_animals=user_personalization_animals,
        user_personalization_activities=user_personalization_activities,
        user_personalization_colors=user_personalization_colors,
        length=length,
    )
