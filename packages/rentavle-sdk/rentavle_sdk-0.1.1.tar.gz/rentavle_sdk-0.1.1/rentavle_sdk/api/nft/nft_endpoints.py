class NFTEndpoints:
    def get_rentavle_contract_detail(self, contract_address):
        url = f"/v1/nfts/contracts/{contract_address}/rentavle/detail"
        return self.get(url)

    def get_all_registered_nft_collections(self, size=10, cursor=""):
        url = "/v1/nfts/contracts/rentavle"
        params = {"size": size, "cursor": cursor}
        return self.get(url, params=params)

    def get_list_of_nfts_owned_by(self, owner_address, size=10, cursor=""):
        url = f"/v1/nfts/tokens/owners/{owner_address}"
        params = {"size": size, "cursor": cursor}
        return self.get(url, params=params)

    def get_list_of_nfts_by_contract_owned_by(self, contract_address, owner_address, size=10, cursor=""):
        url = f"/v1/nfts/tokens/contracts/{contract_address}/owners/{owner_address}"
        params = {"size": size, "cursor": cursor}
        return self.get(url, params=params)

    def get_list_of_contracts_owned_by(self, owner_address, size=10, cursor=""):
        url = f"/v1/nfts/contracts/owners/{owner_address}"
        params = {"size": size, "cursor": cursor}
        return self.get(url, params=params)

    def get_list_of_nfts_by_contract(self, contract_address, size=10, cursor=""):
        url = f"/v1/nfts/tokens/contracts/{contract_address}"
        params = {"size": size, "cursor": cursor}
        return self.get(url, params=params)

    def get_list_of_nfts_borrowed_by(self, borrower_address, size=10, cursor=""):
        url = f"/v1/nfts/tokens/borrowers/{borrower_address}"
        params = {"size": size, "cursor": cursor}
        return self.get(url, params=params)

    def get_list_of_nfts_lent_by(self, lender_address, size=10, cursor=""):
        url = f"/v1/nfts/tokens/lenders/{lender_address}"
        params = {"size": size, "cursor": cursor}
        return self.get(url, params=params)
