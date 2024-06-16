import spacy
import dateparser

class YearExtractor:
    def __init__(self):
        # Load the spaCy model once during initialization
        self.nlp = spacy.load("en_core_web_lg")

    def extract_and_convert(self, text):
        # Process the text using the spaCy model
        doc = self.nlp(text)
        
        # Extract date entities
        date_entities = [ent for ent in doc.ents if ent.label_ == "DATE"]
        print("Extracted date entities:", date_entities)

        # Assume only one date entity is present and process it
        if date_entities:
            ent = date_entities[0]  # Assume there is only one, process this one
            print("Processing entity:", ent.text)
            # Use dateparser to parse the date entity
            date = dateparser.parse(ent.text, settings={'PREFER_DATES_FROM': 'past'})
            print("Parsed date:", date)
            if date:
                return date.year  # Return the year as an integer

        return None  # Return None if no date entities or no parseable date

