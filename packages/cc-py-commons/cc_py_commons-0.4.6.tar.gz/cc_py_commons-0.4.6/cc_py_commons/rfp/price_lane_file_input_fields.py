class PriceLaneFileFieldConstants:
    PICKUP_DATE = "pickup_date"
    DELIVERY_DATE = "delivery_date"
    EQUIPMENT = "equipment"
    ORIGIN_CITY = "origin_city"
    ORIGIN_STATE = "origin_state"
    ORIGIN_POSTCODE = "origin_postcode"
    ORIGIN_LATITUDE = "origin_latitude"
    ORIGIN_LONGITUDE = "origin_longitude"
    DEST_CITY = "destination_city"
    DEST_STATE = "destination_state"
    DEST_POSTCODE = "destination_postcode"
    DEST_LATITUDE = "destination_latitude"
    DEST_LONGITUDE = "destination_longitude"
    ACCOUNT_ID = "account_id"
    CLIENT_ID = "client_id"
    LOG_SQL = 'log_sql'
    SAVE_SEARCH = 'save_search'
    WEIGHT = 'weight'
    MODE = 'mode'
    TRAILER_TYPE = 'trailer_type'

class PriceLaneFileInputFields:

    required_file_parser = [
        PriceLaneFileFieldConstants.PICKUP_DATE,
        PriceLaneFileFieldConstants.DELIVERY_DATE,
        PriceLaneFileFieldConstants.TRAILER_TYPE,
        PriceLaneFileFieldConstants.ORIGIN_CITY,
        PriceLaneFileFieldConstants.ORIGIN_STATE,
        PriceLaneFileFieldConstants.DEST_CITY,
        PriceLaneFileFieldConstants.DEST_STATE
    ]

    optional = [
        PriceLaneFileFieldConstants.ORIGIN_LATITUDE,
        PriceLaneFileFieldConstants.ORIGIN_LONGITUDE,
        PriceLaneFileFieldConstants.ORIGIN_POSTCODE,
        PriceLaneFileFieldConstants.DEST_LATITUDE,
        PriceLaneFileFieldConstants.DEST_LONGITUDE,
        PriceLaneFileFieldConstants.DEST_POSTCODE,
        PriceLaneFileFieldConstants.LOG_SQL,
        PriceLaneFileFieldConstants.SAVE_SEARCH,
        PriceLaneFileFieldConstants.WEIGHT,
        PriceLaneFileFieldConstants.MODE
    ]

price_lane_file_input_fields = PriceLaneFileInputFields
