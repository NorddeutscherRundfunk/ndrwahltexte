########################
#
# Dieses Script enthält ein generalisierten Textgenerator,
# der unabhängig von dem Rest des Repos sind
# und auch in andere Repos kopiert werden können
# -> l.sander.fm@ndr.de 
# 
#########################
import random
import re
from typing import Dict, List, Tuple
from simpleeval import simple_eval

#functions that are safe to be used in the conditions of templates
SAFE_FUNCTIONS = {
        "len": len,
        "min": min,
        "max": max,
        "sum": sum,
        "round": round,
        "abs": abs,
        "sorted": sorted,
        "int": int,
        "float": float
    }

class TemplateEngine:
    """
    TemplateEngine is a rule-based system for generating natural language text 
    using a combination of template dictionaries, variable data, and optional corrections.

    Templates can be filtered by topic or specific keys and include conditional logic 
    that determines whether they should be included based on the current variables.

    Attributes:
        templates (dict): Dictionary of sentence templates keyed by name.
        variables (dict): Dictionary of dynamic values to be substituted into templates.
        corrections (dict): Optional dictionary of text correction patterns (regex-based).
        article (dict): Generated text stored by section name.
    """
    
    
    def __init__(self, templates: dict, variables: dict, corrections: dict = None):
        """
        Initializes the TemplateEngine.

        Args:
            templates (dict): A dictionary of templates where each value includes:
                - 'text' (str or list of str): The sentence template(s).
                - 'topic' (str, optional): A category used for filtering.
                - 'conditions' (list of str, optional): Boolean expressions using `variables`.
            variables (dict): A dictionary of values used to format the templates.
            corrections (dict, optional): A dictionary of regex-based text corrections.
        """
        self.templates = templates                  # Sentence templates
        self.variables = variables                  # Variables to fill in
        self.corrections = corrections or {}        # Grammar/style corrections
        self.article = {}                           # Full generated article

    def check_conditions(self, conditions: List[str]) -> bool:
        """
        Evaluates all given condition strings using current variables.

        Args:
            conditions (List[str]): A list of boolean expressions as strings.

        Returns:
            bool: True if all conditions are met or if the list is empty.
            This means that sentences that are to always be used can be templated
            without a condition
        """
        if not conditions:
            return True
        try:
            return all(simple_eval(cond, names=self.variables, functions=SAFE_FUNCTIONS) for cond in conditions)
        except Exception:
            return False

    def select_templates(self, filter_topic=None) -> List[Tuple[str, dict]]:
        """
        Selects templates either by a topic string or a list of template keys.

        Args:
            filter_topic (str or list of str): 
                - If str: selects templates whose 'topic' matches the string.
                - If list: selects templates whose keys are in the list.

        Returns:
            List[Tuple[str, dict]]: A list of (template_key, template_dict) tuples.
        """
        selected = []

        # Case 1: A list of template keys (names)
        if isinstance(filter_topic, list):
            for key in filter_topic:
                template = self.templates.get(key)
                if template and self.check_conditions(template.get("conditions", [])):
                    selected.append((key, template))

        # Case 2: A single topic string
        else:
            for key, template in self.templates.items():
                if filter_topic and template.get("topic") != filter_topic:
                    continue
                if self.check_conditions(template.get("conditions", [])):
                    selected.append((key, template))

        return selected

    def generate_text(self, selected_templates: List[Tuple[str, dict]] = None) -> List[Tuple[str, str]]:
        """
        Generates a list of (template_key, sentence) tuples with variables filled in.

        Args:
            selected_templates (List[Tuple[str, dict]], optional): Pre-filtered templates. 
                If None, all valid templates are selected.

        Returns:
            List[Tuple[str, str]]: Generated sentences keyed by their template name.
        """
        if selected_templates is None:
            selected_templates = self.select_templates()
        sentences = []
        for key, template in selected_templates:
            text_options = template["text"]
            if isinstance(text_options, list):
                template_text = random.choice(text_options)
            else:
                template_text = text_options
            sentence = template_text.format(**self.variables)
            sentences.append((key, sentence))
        return sentences

    def text_corrections(self, sentences: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """
        Applies regex-based corrections to generated sentences.

        Args:
            sentences (List[Tuple[str, str]]): Sentences to correct.

        Returns:
            List[Tuple[str, str]]: Corrected sentences.
        """
        corrected_sentences = []
        for key, sentence in sentences:
            for pattern, corr in self.corrections.items():
                applies_to = corr.get("applies_to", None)
                if applies_to and key not in applies_to:
                    continue
                sentence = re.sub(pattern, corr["replacement"], sentence)
            corrected_sentences.append((key, sentence))
        return corrected_sentences

    def build_text(self, selected_templates: List[Tuple[str, dict]] = None) -> List[str]:
        """
        Generates a final joined text from the selected templates.

        Args:
            selected_templates (List[Tuple[str, dict]], optional): Templates to use.
            To use multiple topics the lists from select_templates can be added:
            selected_templates = self.select_templates(filter_topic='a'+self.select_templates(filter_topic='b')

        Returns:
            str: Full text as a single string, with corrections applied.
        """
        generated = self.generate_text(selected_templates)
        corrected = self.text_corrections(generated)
        return " ".join([sentence for _, sentence in corrected])

    def build_article(self, sections_dict: Dict[str, List[Tuple[str, dict]]]) -> Dict[str, List[str]]:
        """
        Builds a structured article composed of multiple sections.

        Args:
            sections_dict (Dict[str, List[Tuple[str, dict]]]): 
                Mapping of section names to lists of selected templates.

        Returns:
            Dict[str, str]: Mapping of section names to their final generated texts.
        """
        article = {}
        for section, selected_templates in sections_dict.items():
            text = self.build_text(selected_templates)
            article[section] = text
        self.article = article
        return article