import enum
import os

_ENV_PARAM_PREFIX = 'DP_PING_MON'


class EnvParam(enum.Enum):
    """
    The only allowed environment variables are those from this class.

    Environment variable is constructed as following:
        param prefix + '_' + env param name

    E.g. for 'VERSION_MAJOR' the real environment name is 'GSPG_VERSION_MAJOR'
    """
    VERSION_MAJOR = (0, 'VERSION_MAJOR')
    VERSION_MINOR = (1, 'VERSION_MINOR')
    VERSION_PATCH = (2, 'VERSION_PATCH')
    VERSION_BUILD_NUMBER = (3, 'VERSION_BUILD_NUMBER')

    IS_DEBUG = (4, 'IS_DEBUG')

    def __str__(self):
        return self.value[1]

    def as_str(self) -> str:
        return f'{_ENV_PARAM_PREFIX}_{str(self)}'


def _get_env_param_name(env_param: EnvParam) -> str:
    return env_param.as_str()


def _get_env_param_str(param: EnvParam, default: str = '') -> str:
    param_name = param.as_str()

    if param_name not in os.environ or isinstance(os.environ[param_name], str):
        return default

    return os.environ[param_name]


def _get_env_param_bool(param: EnvParam, default: bool = False) -> bool:
    val_str = _get_env_param_str(param, '')
    if val_str == '':
        return default

    return val_str.lower() in ['true', 'yes', 'on', '1']


def _get_env_param_int(param: EnvParam, default: int = 0) -> int:
    val_str = _get_env_param_str(param, '')
    if val_str == '':
        return default

    try:
        val_int = int(val_str)
    except ValueError:
        return default

    return val_int


class AppVersion(object):
    _instance = None

    _major = 0
    _minor = 0
    _patch = 0
    _build_number = 0

    def __init__(self):
        self._major = _get_env_param_int(EnvParam.VERSION_MAJOR, self._major)
        self._minor = _get_env_param_int(EnvParam.VERSION_MINOR, self._minor)
        self._patch = _get_env_param_int(EnvParam.VERSION_PATCH, self._patch)
        self._build_number = _get_env_param_int(EnvParam.VERSION_BUILD_NUMBER, self._build_number)

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            raise RuntimeError(f'{cls.__name__} assumed to be a singleton')

        return cls._instance

    def __str__(self) -> str:
        return self.as_str()

    def as_str(self, number_count=2) -> str:
        if number_count == 1:
            return f'v{self._major}'
        elif number_count == 2:
            pass  # default
        elif number_count == 3:
            return f'v{self._major}.{self._minor}.{self._patch}'
        elif number_count == 4:
            return f'v{self._major}.{self._minor}.{self._patch}, build {self._build_number}'

        return f'v{self._major}.{self._minor}'


class Defaults(object):
    _instance = None

    _use_cache = True
    _out_image_path = '.'
    _out_image_base_name = 'github_lang_stats-%Y_%m_%d-%H_%M_%S.png'
    _min_percent = 1.0

    _image_width = 1280
    _image_height = 720

    def __init__(self):
        pass

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            raise RuntimeError(f'{cls.__name__} assumed to be a singleton')

        return cls._instance

    @property
    def use_cache(self) -> bool:
        return self._use_cache

    @property
    def out_image_path(self) -> str:
        return self._out_image_path

    @property
    def out_image_base_name(self) -> str:
        return self._out_image_base_name

    @property
    def min_percent(self) -> float:
        return self._min_percent

    @property
    def image_width(self) -> int:
        return self._image_width

    @property
    def image_height(self) -> int:
        return self._image_height


class Config(object):
    _instance = None

    _app_version = AppVersion()
    _defaults = Defaults()

    _is_debug = True

    _organization_name = "DiPaolo"
    _organization_domain = 'dipaolo.dev'
    _application_name = 'DP Ping Monitor'
    _application_name_lowercase = 'dp_ping_monitor'

    def __init__(self):
        self._is_debug = _get_env_param_bool(EnvParam.IS_DEBUG, self._is_debug)

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            raise RuntimeError(f'{cls.__name__} assumed to be a singleton')

        return cls._instance

    @property
    def app_version(self) -> AppVersion:
        return self._app_version

    @property
    def defaults(self) -> Defaults:
        return self._defaults

    @property
    def is_debug(self) -> bool:
        return self._is_debug

    @property
    def max_repos_to_process(self) -> int:
        return 5 if self._is_debug else 2 ** 32  # applied in DEBUG only

    @property
    def organization_name(self) -> str:
        return self._organization_name

    @property
    def organization_domain(self) -> str:
        return self._organization_domain

    @property
    def application_name(self) -> str:
        return self._application_name

    @property
    def application_name_lowercase(self) -> str:
        return self._application_name_lowercase


config = Config()
