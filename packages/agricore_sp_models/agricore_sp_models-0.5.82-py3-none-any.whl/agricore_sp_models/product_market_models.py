from pydantic import BaseModel
from typing import Optional, List, Tuple
from enum import IntEnum

class ProductGroupDescription(BaseModel):
    # Name of the product group in the population
    productGroupName: str
    # List of the fadn codes included in this group and their representativeness (0..100) over the total group
    fadnProducts: List[Tuple[str, float]]
    # 0 if the product group is conventional, 1 if it is organic, 2 if it is undetermined
    organic: int
    
class ProductionDataEntry(BaseModel):
    # Name of the product group
    productGroupName: str
    # NUTS3 code for which this production data applies
    nuts3: str
    # Amount of produced units for this product
    production: float

class DataToPMM(BaseModel):
    productList: List[ProductGroupDescription]
    # Year for which the data is requested
    yearNumber: int
    # True if we desire to receive the estimation of this data only accounting with previous years data
    simulationRequested: bool
    # True if we desire to receive the actual historical value for this year, should it exists
    actualDataRequested: bool
    # List of the NUTS3 codes for which the data is requested
    nuts3List: List[str]
    # List of expected production for each product group / region, so the impact on the price can be calculated.
    expectedProduction: List[ProductionDataEntry]    

class IndividualPrice(BaseModel):
    # Name of the product group
    productGroupName: str
    # NUTS3 code for which this production data applies
    nuts3: str
    # Price [€/unit] for this product
    simulatedPrice: float
    # Price [€/unit] for this product in the historical data. 0 if not available
    actualPrice: float
    
class DataFromPMM(BaseModel):
    prices: List[IndividualPrice]
    # Year for which the data is related to
    yearNumber: int