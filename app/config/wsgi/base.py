import os

__all__ = (
    'ENV_PATH',
)

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))

ENV_PATH = os.path.join(ROOT_DIR, '.env')
