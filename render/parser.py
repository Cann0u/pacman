import json

class ParsingError(Exception):
    ...

class Parser:
    def __init__(self, file):
        try:
            with open(file) as f:
                self.info = json.load(f)
        except Exception as e:
            raise ParsingError(f"Error while loding configuration file:\n{e}")
