import logging
from concurrent.futures import ThreadPoolExecutor

import exchange
import grpc
import pytest

channel_options = [
    ("grpc.keepalive_time_ms", 8000),
    ("grpc.keepalive_timeout_ms", 50000),
    ("grpc.http2.max_pings_without_data", 5),
    ("grpc.keepalive_permit_without_calls", 1),
]


class TestExchange:
    channel = grpc.insecure_channel(
        target="localhost:8081",
        options=channel_options,
        # compression=grpc.Compression.Gzip,
    )
    ex = exchange.Exchange(channel=channel)

    def test_get_ticker(self):
        reply = self.ex.get_ticker(platform="okx.spot", instrument="btc_usdt")
        print(f"recv from server, result={reply.result}")
        print(f"recv from server, result={reply.result.info}")

    def test_get_kline(self):
        reply = self.ex.get_kline(
            platform="okx.spot", instrument="btc_usdt", resolution="1m"
        )
        print(f"recv from server, result={reply.result}")

    def test_get_orderbook(self):
        reply = self.ex.get_orderbook(platform="okx.spot", instrument="btc_usdt")
        print(f"recv from server, asks={reply.result.asks}, bid={reply.result.bids}")

    def test_get_position(self):
        reply = self.ex.get_position(platform="okx.spot")
        print(f"recv from server, result={reply.result}")
        print(f"recv from server, result={reply.result.info}")

    def test_get_order(self):
        reply = self.ex.get_order(platform="okx.spot", instrument="btc_usdt")
        print(f"recv from server, result={reply.result}")
        print(f"recv from server, result={reply.result.info}")

    def test_get_orders(self):
        reply = self.ex.get_orders(platform="okx.spot")
        print(f"recv from server, result={reply.result}")
        print(f"recv from server, result={reply.result.info}")

    def test_buy(self):
        reply = self.ex.buy(
            platform="okx.spot",
            instrument="btc_usdt",
            price="10000",
            amount="0.01",
            args={
                "instId": "BTC-USDT",
                "tdMode": "cash",
                "clOrdId": "b15",
                "side": "buy",
                "ordType": "limit",
                "px": "2.15",
                "sz": "2",
            },
        )
        print(f"recv from server, result={reply.result.info}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    t = TestExchange()
    t.test_get_kline()
    # t.test_buy()
