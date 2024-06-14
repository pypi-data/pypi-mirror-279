import dataclasses
import itertools
import typing

import slugify

from unico_device_setuper.cli import stp
from unico_device_setuper.cli.command import register_unitech
from unico_device_setuper.lib import aio, cnsl, env, sygic, unitech, util


@dataclasses.dataclass(frozen=True)
class Product:
    name: str
    is_dev: bool

    @property
    def label(self):
        return ('[DEV] ' if self.is_dev else '') + self.name

    @staticmethod
    def from_license(license: sygic.License):
        return Product(license.product_name, license.is_testing_license)


GroupedLicenses: typing.TypeAlias = typing.Mapping[Product, typing.Sequence[sygic.License]]


async def get_grouped_licenses(sygic_client: sygic.Client, unitech_env: env.UnitechEnv):
    return util.groupby(
        (
            license
            for license in await sygic_client.get_licenses()
            if license.license_status_type == 'free'
            or license.license_status_type == 'deactivated'
            and not (unitech_env == env.UnitechEnv.LOCAL and not license.is_testing_license)
        ),
        Product.from_license,
    )


async def get_activated_products_for_device(device_id: str, sygic_client: sygic.Client):
    return {
        Product(license.product_name, license.is_testing_license): license
        for license in await sygic_client.get_licenses()
        if license.identifier == device_id
    }


async def choose_product(grouped_licenses: GroupedLicenses, product_labels: list[str] | None):
    if product_labels is None:
        cnsl.print_blue('Choisir des types de licence:')
        return await cnsl.print_choose_multiple(
            sorted(grouped_licenses.keys(), key=lambda p: p.label),
            prompt='Types de licence: ',
            formater=lambda p: p.label
            + f' ({len(grouped_licenses[p])} licence{'s' if grouped_licenses[p] else ''})',
            choice_formater=lambda p: p.label,
        )

    product_label_map = {slugify.slugify(product.label): product for product in grouped_licenses}

    products: list[Product] = []
    for product_label in product_labels:
        if (product := product_label_map.get(slugify.slugify(product_label))) is None:
            cnsl.print_red(f'Aucun type de license nommé [hot_pink3]`{product_label}`[/hot_pink3]')
            return None
        products.append(product)

    return products


async def get_device_name(device_id: str, setup: stp.Setup):
    unitech_client = await setup.get_unitech_client()
    if unitech_client is None:
        return None
    return next(
        (
            d.name
            for d in await unitech.get_device_all_devices.request(unitech_client) or []
            if d.id_device == device_id
        ),
        None,
    )


async def register_licence(
    license: sygic.License, device_id: str, device_name: str, client: sygic.Client
):
    license = license.model_copy()
    license.license_status_type = 'active'
    license.identifier = device_id
    license.note = device_name
    license.license_identifier_type = 'device'
    await client.update_license(license)
    cnsl.print(f"Utilisation d'une license {Product.from_license(license).label}")


async def rename_licence(license: sygic.License, device_name: str, client: sygic.Client):
    license = license.model_copy()
    license.note = device_name
    await client.update_license(license)
    cnsl.print_gray(f'Renomage de la license {Product.from_license(license).label}')


@cnsl.command("Enregistrement de l'appareil sur Sygic", 'Appareil enregistré sur Sygic')
async def register_sygic(setup: stp.Setup):
    sygic_client = await setup.get_sygic_client()
    grouped_licenses = await get_grouped_licenses(sygic_client, setup.unitech_env)
    products = await choose_product(
        grouped_licenses, product_labels=setup.args.sygic_products_names
    )
    if products is None:
        return False

    products = set(products)

    device_id = await register_unitech.get_id_device(setup)
    if device_id is None:
        cnsl.print_red("Impossible de trouver l'id device")
        return False

    device_name = await get_device_name(device_id, setup)
    if device_name is None:
        cnsl.print_red("Impossible de trouver le nom de l'appereil")
        return False

    license_to_rename: list[sygic.License] = []

    for activated_product, license in (
        await get_activated_products_for_device(device_id, sygic_client)
    ).items():
        if activated_product in products:
            cnsl.print_gray(
                f'Une license {activated_product.label} est déja active pour cet appareil'
            )
            products.remove(activated_product)
            if license.note != device_name:
                license_to_rename.append(license)

    await aio.gather_unordered(
        itertools.chain(
            (
                register_licence(
                    license=grouped_licenses[product][0],
                    device_id=device_id,
                    device_name=device_name,
                    client=sygic_client,
                )
                for product in products
            ),
            (
                rename_licence(license=license, device_name=device_name, client=sygic_client)
                for license in license_to_rename
            ),
        )
    )

    return True
