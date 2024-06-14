import enum
import typing

from unico_device_setuper.lib import datadir, rl


class UnitechEnv(enum.Enum):
    LOCAL = 'local'
    DEV = 'dev'
    PRE_PROD = 'pre-prod'
    PROD = 'prod'

    @property
    def api_base_url(self):
        if self == UnitechEnv.LOCAL:
            return rl.Url('http://localhost:3000')
        return rl.Url(f'https://api.{self.value}.unicofrance.com')

    @property
    def device_setuper_base_url(self):
        if self == UnitechEnv.LOCAL:
            return rl.Url('http://localhost:12000')
        return rl.Url('https://device-setuper.prod.unicofrance.com')

    @property
    def static_base_url(self) -> rl.Url:
        if self == UnitechEnv.LOCAL:
            return UnitechEnv.DEV.static_base_url
        return rl.Url(f'https://static.{self.value}.unicofrance.com')

    @classmethod
    def get_default(cls):
        if datadir.is_release_version():
            return cls.PROD
        return cls.LOCAL


class SygicEnv(enum.Enum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'

    @property
    def api_base_url(self):
        return rl.Url('https://api.bls.sygic.com/api/v1')

    @classmethod
    def get_default(cls):
        if datadir.is_release_version():
            return cls.PRIMARY
        return cls.SECONDARY


Env: typing.TypeAlias = SygicEnv | UnitechEnv
