from environs import Env


def load_env():
    env = Env()
    env.read_env()

    return env


def load_open_ai_key():
    env = load_env()
    open_ai_key = env('OPEN_AI_KEY', None)

    if open_ai_key is None:
        raise ValueError('OPEN_AI_KEY is not set in the environment')

    return open_ai_key
