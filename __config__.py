from pathlib import Path

# Setup paths variables
PROJECT_PATH = Path(__file__).parent.resolve()
SOURCE_PATH = Path(f'{PROJECT_PATH}\\source').resolve()
RAW = Path(f'{SOURCE_PATH}\\raw').resolve()
PROCESSED = Path(f'{SOURCE_PATH}\\processed').resolve()
