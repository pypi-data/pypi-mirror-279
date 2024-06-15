import requests
from ..utils.request import get
from .nft.nft_endpoints import add_nft_endpoints
from ..config import API_ENDPOINT, CHAIN_ID, DEBUG

class RentavleSDK:
    def __init__(self, api_endpoint=API_ENDPOINT, chain_id=CHAIN_ID, debug=DEBUG):
        self.api_endpoint = api_endpoint
        self.chain_id = chain_id
        self.debug = debug

        self.session = requests.Session()
        self.session.headers.update({"x-chain-id": self.chain_id})

        add_nft_endpoints(self)

    def get(self, url, params=None):
        full_url = f"{self.api_endpoint}{url}"
        return get(full_url, params=params)
