import dataclasses
import typing

from unico_device_setuper.lib import auth, cnsl, env, unitech


@dataclasses.dataclass
class Args:
    unitech_client_strategy: auth.ClientStrategy
    unitech_env: env.UnitechEnv


Handler: typing.TypeAlias = typing.Callable[['Setup'], typing.Awaitable[None]]


@dataclasses.dataclass
class Setup:
    args: Args
    _unitech_client: unitech.Client

    @staticmethod
    async def execute(args: Args, handler: Handler):
        cnsl.print_gray(f'Environement: {args.unitech_env.value}')
        async with unitech.Client(base_url=str(args.unitech_env.api_base_url)) as unitech_client:
            await handler(Setup(args=args, _unitech_client=unitech_client))

    async def get_unitech_client(self):
        headers = self._unitech_client.get_async_httpx_client().headers
        auth_header_name = 'Authorization'
        if headers.get(auth_header_name) is None:
            auth_token = await auth.get_unitech_auth_token(
                self.args.unitech_env, client_strategy=self.args.unitech_client_strategy
            )
            if auth_token is None:
                return None
            headers[auth_header_name] = f'Bearer {auth_token}'
        return self._unitech_client
