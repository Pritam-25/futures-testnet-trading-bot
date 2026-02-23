from enum import Enum
from pydantic import BaseModel, Field,  model_validator
from typing import Optional

from .validators import OrderSide, OrderType


class OrderSide(str, Enum):
	BUY = "BUY"
	SELL = "SELL"


class OrderType(str, Enum):
	MARKET = "MARKET"
	LIMIT = "LIMIT"


def validate_min_notional(notional: float, min_notional: float = 100.0) -> bool:
	"""Return True if notional meets the exchange minimum (default 100 USDT)."""
	try:
		return float(notional) >= float(min_notional)
	except Exception:
		return False

# -------------------------
# Pydantic Order Schema
# -------------------------

class OrderInput(BaseModel):
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float = Field(gt=0)
    price: Optional[float] = None

    @model_validator(mode="after")
    def validate_price_for_limit(self):
        if self.order_type == OrderType.LIMIT and self.price is None:
            raise ValueError("Price is required for LIMIT orders")
        return self