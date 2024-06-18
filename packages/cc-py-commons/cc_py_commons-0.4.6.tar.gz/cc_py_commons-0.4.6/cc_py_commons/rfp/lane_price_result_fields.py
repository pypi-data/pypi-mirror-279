from cc_py_commons.rfp.price_lane_file_input_fields import PriceLaneFileFieldConstants


class LaneResultFieldConstants:

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
    MODEL_NAME = "model_name"
    RSQUARED = "rsquared"
    ROWS_USED = "rows_used"
    LANE_PRICE_SEARCH_ID = "lane_price_search_id"
    PREDICTION = 'prediction'
    LOWER_BOUND = 'lower_bound'
    UPPER_BOUND = 'upper_bound'
    FUEL_COST_DATE = 'fuel_price_date'
    FUEL_PRICE_GALLON = 'fuel_price_per_gallon'
    FUEL_COST = 'fuel_cost'
    TRIP_MILES = 'trip_miles'
    SEARCH_RADIUS = "search_radius"
    CONFIDENCE_SCORE = 'confidence_score'
    KITCHEN_SINK_WEIGHT = 'kitchen_sink_weight'

class ResultFieldConstants:

    ALL_IN_COST = "allInCost"
    ALL_IN_COST_LOW = "allInCostLow"
    ALL_IN_COST_HIGH = "allInCostHigh"
    LINE_HAUL_COST = "lineHaulCost"
    LINE_HAUL_COST_LOW = "lineHaulCostLow"
    LINE_HAUL_COST_HIGH = "lineHaulCostHigh"
    FUEL_PRICE_DATE = "fuelPriceDate"
    FUEL_COST = "fuelCost"
    FUEL_COST_PER_MILE = "fuelCostPerMile"
    LANE_MILES = "laneMiles"
    LANE_PRICE_SEARCH_ID = "lanePriceSearchId"
    LOADS_USED = "loadsUsed"
    SEARCH_RADIUS = "searchRadius"
    FUEL_COST_BY_MILES = "fuelCostByMiles"
    FLAT_RATE = "flatRate"
    CONFIDENCE_SCORE = 'confidenceScore'

class PriceLaneFileResultFields(PriceLaneFileFieldConstants):

    TRAILER_TYPE = 'trailer_type'
    ALL_IN = "all_in"
    ALL_IN_HIGH = "all_in_high"
    ALL_IN_LOW = "all_in_low"
    PER_MILE = "per_mile"
    DISTANCE = "distance"
    LOADS_USED = "loads_used"
    SEARCH_RADIUS = "search_radius"
