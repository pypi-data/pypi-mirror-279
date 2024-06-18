from typing import TypedDict

class NFTCollection(TypedDict):
    contractAddress: str
    chainId: str
    imageUrl: str
    nftType: str
    collectionName: str
    collectionSymbol: str
    projectName: str
    projectDescription: str
    projectProfileImageUrl: str
    totalSupply: int
    onSaleCount: int
    rentedCount: int
