from typing import Dict
from .connector import Connector

def provide_data(
    public_url: str,
    asset_id: str,
    provider_connector: Connector,
    consumer_connector: Connector
) -> None:
    """
    High-level entrypoint: creates the asset, usage policy, access policy, and contract.
    """
    provider_connector.create_asset(asset_id, public_url)
    provider_connector.create_usage_policy(asset_id)
    provider_connector.create_access_policy(asset_id, consumer_connector)
    provider_connector.create_contract(asset_id)


def get_asset_access(
    asset_id: str,
    provider_connector: Connector,
    consumer_connector: Connector
) -> Dict:
    """
    High-level entrypoint: queries catalogue, negotiates EDR, requests EDR, and reads access details.
    """
    offer_id = consumer_connector.read_policy_id_from_catalog(provider_connector, asset_id)
    consumer_connector.negotiate_edr(offer_id, asset_id, provider_connector)
    transfer_id = consumer_connector.request_edr(asset_id)
    access = consumer_connector.read_edr_details(transfer_id)

    return access