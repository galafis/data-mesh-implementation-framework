"""
Data Mesh Implementation Framework
Author: Gabriel Demetrios Lafis
Year: 2025

Este pacote fornece implementações de Data Products seguindo os princípios do Data Mesh.
"""

from .domain_data_product import (
    DomainDataProduct,
    DataProductMetadata,
    DataSchema,
    DataProductSLA,
    DataProductStatus,
    DataQualityLevel
)
from .sales_data_product import SalesDataProduct
from .customer_data_product import CustomerDataProduct
from .api_integration import WorldBankAPIIntegration, ExternalDataEnricher

__version__ = "1.0.0"
__author__ = "Gabriel Demetrios Lafis"

__all__ = [
    "DomainDataProduct",
    "DataProductMetadata",
    "DataSchema",
    "DataProductSLA",
    "DataProductStatus",
    "DataQualityLevel",
    "SalesDataProduct",
    "CustomerDataProduct",
    "WorldBankAPIIntegration",
    "ExternalDataEnricher"
]
