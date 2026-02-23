import typer
from typing import Optional
from bot.orders import place_order
from bot.validators import OrderInput
import logging
from bot.logging_config import setup_logging
from pydantic import ValidationError
from binance.exceptions import BinanceAPIException
from bot.client import BinanceFuturesClient
from bot.validators import OrderSide, OrderType, validate_min_notional


logger = setup_logging()

app = typer.Typer(help="Binance Futures Testnet Trading Bot", add_completion=False)


@app.command()
def trade(
    symbol: str = typer.Option(..., help="Trading pair symbol (e.g., BTCUSDT)"),
    side: OrderSide = typer.Option(..., help="Order side: BUY or SELL"),
    order_type: OrderType = typer.Option(..., "--type", help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Order quantity (must be > 0)"),
    price: Optional[float] = typer.Option(None, help="Price (required for LIMIT)"),
    confirm: bool = typer.Option(True, help="Ask confirmation before placing order"),
):
    """
    Place a Futures order on Binance Testnet.
    """

    # logging already configured at module import

    try:
        client_wrapper = BinanceFuturesClient(testnet=True)
        client = client_wrapper.get_client()

        # Fetch account balance
        account_info = client.futures_account()
        balance = float(account_info.get("availableBalance", 0))

        typer.secho(f"\n💰 Available Balance: {balance} USDT", fg=typer.colors.CYAN)

        # Fetch current price
        ticker = client.futures_symbol_ticker(symbol=symbol.upper())
        current_price = float(ticker.get("price", 0))

        typer.secho(f"📈 Current {symbol.upper()} Price: {current_price} USDT", fg=typer.colors.CYAN)

        # Determine effective price (Pydantic will validate LIMIT price)
        effective_price = price if price is not None else current_price
        notional = quantity * effective_price

        # Prepare order data and validate with Pydantic before confirmation
        order_data = {
            "symbol": symbol.upper(),
            "side": side.value,
            "order_type": order_type.value,
            "quantity": quantity,
            "price": price,
        }

        try:
            OrderInput(**order_data)
        except ValidationError as ve:
            typer.secho("\n❌ Validation Error:", fg=typer.colors.RED)
            for err in ve.errors():
                loc = ".".join([str(x) for x in err.get("loc", [])])
                msg = err.get("msg", str(err))
                typer.echo(f"• {loc}: {msg}")

            logger.error("Validation error while building order: %s", ve)
            raise typer.Exit()

        typer.secho(f"🧮 Order Notional Value: {notional:.2f} USDT", fg=typer.colors.YELLOW)

        if not validate_min_notional(notional):
            typer.secho(
                "⚠ Warning: Binance requires minimum notional of 100 USDT.",
                fg=typer.colors.RED,
            )

        # Confirmation prompt
        if confirm:
            proceed = typer.confirm("Do you want to place this order?")
            if not proceed:
                typer.secho("❌ Order cancelled by user.", fg=typer.colors.RED)
                raise typer.Exit()

        # Place order (pass single client instance)
        result = place_order(order_data, client)

        # Print summary
        typer.secho("\n========== ORDER SUMMARY ==========", bold=True)
        typer.echo(f"Symbol: {symbol.upper()}")
        typer.echo(f"Side: {side.value}")
        typer.echo(f"Type: {order_type.value}")
        typer.echo(f"Quantity: {quantity}")
        if price is not None:
            typer.echo(f"Price: {price}")

        typer.secho("\n========== ORDER RESPONSE ==========", bold=True)
        typer.echo(f"Order ID: {result.get('orderId')}")
        typer.echo(f"Status: {result.get('status')}")
        typer.echo(f"Executed Quantity: {result.get('executedQty')}")
        typer.echo(f"Average Price: {result.get('avgPrice')}")

        typer.secho("\n✅ Order placed successfully!", fg=typer.colors.GREEN)
        # Log successful order placement to file
        logger.info(
            "Order placed successfully: %s %s %s qty=%s price=%s | Order ID: %s",
            side.value,
            order_type.value,
            symbol.upper(),
            quantity,
            effective_price,
            result.get("orderId"),
        )

    except typer.Exit:
        # Clean exit (user cancelled or validation raised Exit)
        raise

    except BinanceAPIException as be:
        typer.secho("\n❌ Binance API Error:", fg=typer.colors.RED)
        typer.echo(getattr(be, "message", str(be)))
        logger.exception("Binance API error while placing order: %s", getattr(be, "message", str(be)))

    except Exception as e:
        typer.secho("\n❌ Unexpected Error:", fg=typer.colors.RED)
        typer.echo(str(e))
        logger.exception("Unexpected error in trade command: %s", str(e))


if __name__ == "__main__":
    app()