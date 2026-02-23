import logging
from binance.exceptions import BinanceAPIException
from pydantic import ValidationError
from .validators import OrderInput
from .validators import OrderType


# -------------------------
# Order Execution Function
# -------------------------

def place_order(order_data: dict, client) -> dict:
    """Place an order using an existing `client` instance.

    The CLI should create the `BinanceFuturesClient` and pass
    `client_wrapper.get_client()` here to avoid multiple client instances.
    """
    logger = logging.getLogger(__name__)
    try:
        order = OrderInput(**order_data)


        if order.order_type == OrderType.MARKET:
            response = client.futures_create_order(
                symbol=order.symbol,
                side=order.side.value,
                type=order.order_type.value,
                quantity=order.quantity,
            )

        else:  # LIMIT
            response = client.futures_create_order(
                symbol=order.symbol,
                side=order.side.value,
                type=order.order_type.value,
                quantity=order.quantity,
                price=order.price,
                timeInForce="GTC",
            )


        return {
            "orderId": response.get("orderId"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty", "0"),
            "avgPrice": response.get("avgPrice", None),
            "raw": response,
        }

    except ValidationError as ve:
        logger.error("Validation Error: %s", ve)
        raise

    except BinanceAPIException as be:
        logger.exception("Binance API Error: %s", getattr(be, 'message', str(be)))
        raise

    except Exception as e:
        logger.exception("Unexpected Error: %s", str(e))
        raise