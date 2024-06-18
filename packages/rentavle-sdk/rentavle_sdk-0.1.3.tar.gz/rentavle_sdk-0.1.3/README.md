# Rentavle SDK\n\nThis SDK provides tools to interact with Rentavle services.


from rentavle_sdk import RentavleSDK

# Using default configuration
sdk = RentavleSDK()

# Providing custom configuration
custom_sdk = RentavleSDK(api_endpoint="https://custom-api.rentavle.com", chain_id="custom_chain_id", debug=True)
