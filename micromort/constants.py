import os

ROOT = os.path.dirname(os.path.dirname(__file__))

PATHS = {
    'LOGS_DIR': os.path.join(ROOT, 'micromort', 'logs'),
    'OUTPUTS_DIR': os.path.join(ROOT, 'micromort', 'outputs'),
    'DATA_DIR': os.path.join(ROOT, 'micromort', 'data')

}

# The number of characters below which the article is not considered for labeling
ARTICLE_LENGTH_PREP = 1000
