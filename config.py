from pathlib import Path

PROJECT_PATH = Path(__file__).parent.resolve()
PROJECT_SOURCE_PATH = Path(f'{PROJECT_PATH}\\source').resolve()
PROJECT_SOURCE_RAW = Path(f'{PROJECT_SOURCE_PATH}\\raw').resolve()
PROJECT_SOURCE_PROCESSED = Path(f'{PROJECT_SOURCE_PATH}\\processed').resolve()
