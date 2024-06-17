import spacy
import json   
from fuzzywuzzy import fuzz

"""
:authors: Dmitry Batrov
:license: Apache License, Version 2.0
:copyright: (c) 2024, Dmitry Batrov
"""

def process_text(text, filter_orgs=[]):
    """
    Process the given text and extract entities using the 'ru_cv_parse_model' spaCy model.
    If filter_orgs is provided, check if any of the extracted organizations match any of the filter_orgs.
    If a match is found, return a string indicating the matching organizations.
    Otherwise, format and return the extracted entities in a specific format.
    
    :param text: A string representing the text to be processed.
    :type text: str
    :param filter_orgs: A list of organizations to be filtered out, defaults to an empty list.
    :type filter_orgs: list, optional
    :return: A string representing the processed text with extracted entities.
    :rtype: str
    :raises Exception: If there is an error processing the text.
    """
    try:
        nlp = spacy.load("ru_cv_parse_model")

        doc = nlp(text)
 
        entities = {
            "fio": [],
            "org": [],
            "title": [],
            "work_date": [],
            "work_exp": [],
            "age": [],
            "gender": [],
            "education": []
        }

        for entity in doc.ents:
            entities[entity.label_].append(entity.text)
 
        matches = __find_matches(entities["org"], filter_orgs)
        if matches:
            text = f"Связь с нежелательными организациями: {matches}"
        else:
            text = __format_text(entities)
    except Exception as e:
        raise Exception(f"Ошибка обработки текста: {e}")

    return text

def save_json_ents(text, output_file, filter_orgs=[]):
    """
    Save the entities extracted from the given text to a JSON file.

    Parameters:
        text (str): The text from which entities will be extracted.
        output_file (str): The path to the output JSON file.
        filter_orgs (list, optional): A list of organizations to be filtered out. Defaults to an empty list.

    Raises:
        Exception: If there is an error processing the text or saving to JSON.

    Returns:
        None
    """
    try:
        nlp = spacy.load("ru_cv_parse_model")

        doc = nlp(text)

        entities = []
        
        for entity in doc.ents:
            entity_dict, signal = __create_entity_dict(entity, filter_orgs)
            if signal:
                entities = []
                entities.append(entity_dict)
                break
            else:
                entities.append(entity_dict)

        data = {'ents': entities}
    except Exception as e:
        raise Exception(f"Ошибка обработки текста: {e}")

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
    except Exception as e:
        raise Exception(f"Ошибка cохранения в JSON: {e}")

def __create_entity_dict(entity, filter_orgs):
    matches = __find_match(entity.text, filter_orgs)
    if matches:
        content = f"Связь с нежелательными организациями: {matches}"
        return {'content': content}, True
    else:
        content = entity.text
        label = entity.label_
        return {'content': content, 'label': label}, False


def __find_match(text, filter_orgs):
    matches = [org for org in filter_orgs if fuzz.ratio(text, org) > 90]
    return matches


def __find_matches(orgs, filter_orgs):
    matches = []
    for filter_org in filter_orgs:
        ratios = [fuzz.ratio(filter_org, org) for org in orgs]
        max_ratio = max(ratios)
        if max_ratio > 90:
            matches.append(filter_org)
    return matches


def __format_text(entities):
    return "".join([
        f"ФИО: {', '.join(entities['fio'])}\n",
        f"Пол: {', '.join(entities['gender'])}\n",
        f"Возраст: {', '.join(entities['age'])}\n",
        f"Опыт работы: {', '.join(entities['work_exp'])}\n",
        f"nКомпании: {', '.join(entities['org'])}\n",
        f"Должности: {', '.join(entities['title'])}\n",
        f"Периоды работы: {', '.join(entities['work_date'])}\n",
        f"Образование: {', '.join(entities['education'])}\n"
    ])

