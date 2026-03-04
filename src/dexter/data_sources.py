import os
from typing import Literal, Optional, Tuple
from enum import Enum

class DataSource(Enum):
    YAHOO_FINANCE = "yfinance"
    DATABURSATIL = "databursatil"
    FINANCIAL_DATASETS = "financialdatasets"

class DataSourceManager:
    """Manage primary and secondary data sources with automatic fallback."""
    
    def __init__(
        self,
        primary: DataSource = DataSource.YAHOO_FINANCE,
        secondary: Optional[DataSource] = None
    ):
        self.primary = primary
        self.secondary = secondary or DataSource.YAHOO_FINANCE
        self._validate_api_keys()
    
    def _validate_api_keys(self):
        """Check if required API keys are present."""
        if self.primary == DataSource.DATABURSATIL:
            if not os.getenv("DATABURSATIL_API_KEY"):
                raise ValueError("DATABURSATIL_API_KEY required but not found")
        
        if self.primary == DataSource.FINANCIAL_DATASETS:
            if not os.getenv("FINANCIAL_DATASETS_API_KEY"):
                raise ValueError("FINANCIAL_DATASETS_API_KEY required but not found")
    
    def get_provider_name(self, source: DataSource) -> str:
        """Get the provider name string for tools."""
        return source.value
    
    def get_primary_provider(self) -> str:
        return self.get_provider_name(self.primary)
    
    def get_secondary_provider(self) -> str:
        return self.get_provider_name(self.secondary)
    
    def switch_primary(self, new_primary: DataSource):
        """Switch primary data source."""
        old_primary = self.primary
        self.primary = new_primary
        self._validate_api_keys()
        return f"Primary source: {old_primary.value} → {new_primary.value}"
    
    def switch_secondary(self, new_secondary: DataSource):
        """Switch secondary data source."""
        old_secondary = self.secondary
        self.secondary = new_secondary
        return f"Secondary source: {old_secondary.value} → {new_secondary.value}"
    
    @classmethod
    def from_env(cls) -> "DataSourceManager":
        """Create manager from environment variables."""
        primary_str = os.getenv("PRIMARY_DATA_SOURCE", "yfinance")
        secondary_str = os.getenv("SECONDARY_DATA_SOURCE", "yfinance")
        
        primary = DataSource(primary_str)
        secondary = DataSource(secondary_str)
        
        return cls(primary=primary, secondary=secondary)
