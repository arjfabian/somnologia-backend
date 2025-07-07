# somnologia_app/plugins/interpreters/base.py

from abc import ABC, abstractmethod

class DreamInterpreter(ABC):
    """
    Abstract Base Class (ABC) defining the interface for all dream interpreters.
    Any concrete dream interpreter must inherit from this class and implement
    all abstract methods.
    """

    @abstractmethod
    def analyze_dream_description(self, dream_description: str) -> dict:
        """
        Analyzes a dream description and returns structured interpretation data.

        Args:
            dream_description (str): The text description of the dream.

        Returns:
            dict: A dictionary containing:
                - 'interpretation': (str) The AI-generated textual interpretation.
                - 'suggested_person_ids': (list[int]) List of IDs of existing Persons found in the description.
                - 'suggested_new_person_names': (list[str]) List of names of potential new Persons found.
                - 'suggested_tag_ids': (list[int]) List of IDs of suggested Tags.
        """
        pass

    @abstractmethod
    def generate_dream_image(self, dream_description: str, interpretation: str = None) -> str | None:
        """
        Generates an image based on the dream description and/or its interpretation.

        Args:
            dream_description (str): The original text description of the dream.
            interpretation (str, optional): The textual interpretation of the dream.
                                            Useful if the image generation AI uses interpretation insights.
                                            Defaults to None.

        Returns:
            str | None: A URL to the generated image, or None if no image could be generated.
        """
        pass