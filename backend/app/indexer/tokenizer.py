import re

STOP_WORDS = {
    "the",
    "is",
    "a",
    "an",
    "of",
    "to",
    "in",
    "for",
    "on",
    "and",
    "or",
    "with"
}

def tokenize(text):
    text = text.lower()
    
    words = re.findall(r"[a-z0-9]+",text)
    
    return [word for word in words if word not in STOP_WORDS]