import itertools
from concurrent.futures import Future, ThreadPoolExecutor

import grpc
import platform_pb2 as pb
import platform_pb2_grpc as grpcpb
from google.protobuf import any_pb2 as anypb

"""
grpc.keepalive_time_ms: The period (in milliseconds) after which a keepalive ping is
    sent on the transport.
grpc.keepalive_timeout_ms: The amount of time (in milliseconds) the sender of the keepalive
    ping waits for an acknowledgement. If it does not receive an acknowledgment within this
    time, it will close the connection.
grpc.keepalive_permit_without_calls: If set to 1 (0 : false; 1 : true), allows keepalive
    pings to be sent even if there are no calls in flight.
grpc.http2.max_pings_without_data: How many pings can the client send before needing to
    send a data/header frame.
For more details, check: https://github.com/grpc/grpc/blob/master/doc/keepalive.md
"""
channel_options = [
    ("grpc.keepalive_time_ms", 8000),
    ("grpc.keepalive_timeout_ms", 5000),
    ("grpc.http2.max_pings_without_data", 5),
    ("grpc.keepalive_permit_without_calls", 1),
]


resolution_ms_map = {
    "1s": 1000,
    "1m": 60 * 1000,
    "3m": 3 * 60 * 1000,
    "5m": 5 * 60 * 1000,
    "15m": 15 * 60 * 1000,
    "30m": 30 * 60 * 1000,
    "1h": 60 * 60 * 1000,
    "2h": 2 * 60 * 60 * 1000,
    "4h": 4 * 60 * 60 * 1000,
    "6h": 6 * 60 * 60 * 1000,
    "8h": 8 * 60 * 60 * 1000,
    "12h": 12 * 60 * 60 * 1000,
    "1d": 24 * 60 * 60 * 1000,
    "3d": 3 * 24 * 60 * 60 * 1000,
    "1w": 7 * 24 * 60 * 60 * 1000,
    "1M": 30 * 24 * 60 * 60 * 1000,
}


class Exchange:
    def __init__(
        self,
        channel: grpc.Channel,
        executor: ThreadPoolExecutor = None,
    ):
        self._executor = executor if executor else ThreadPoolExecutor()
        self._channel = channel
        self._stream = grpcpb.StreamServiceStub(self._channel)
        self._client = grpcpb.ExchangeServiceStub(self._channel)
        self._counter = itertools.count(1)

    def __str__(self):
        return f"{self.name}"

    def submit(self, fn, *args, **kwargs) -> Future:
        """提交异步执行的任务

        Args:
            fn (function): 要执行的函数

        Returns:
            A Future representing the given call.
        """
        return self._executor.submit(fn, *args, **kwargs)

    def subscribe_request(self, method: str, params: dict) -> pb.SubscribeRequest:
        any = anypb.Any()
        any.Pack(params)
        return pb.SubscribeRequest(
            id=next(self._counter),
            method=method,
            params=any,
        )

    def subscribe(
        self,
        platforms: list[str],
        instruments: list[str],
        handler: callable,
        method: str = "ticker",
        params: dict = {},
    ):
        params = pb.GetTickersRequest(
            platforms=platforms,
            instruments=instruments,
        )
        request = self.subscribe_request(method, params)
        response_iterator = self._stream.Subscribe(request)
        # Receive responses
        for response in response_iterator:
            result: anypb.Any = response.result
            if result.Is(pb.GetTickersReply.DESCRIPTOR):
                reply = pb.GetTickersReply()
                result.Unpack(reply)
                handler(reply.result)

    def get_ticker(self, platform: str, instrument: str) -> pb.GetTickerReply:
        return self._client.GetTicker(
            pb.GetTickerRequest(
                platform=platform,
                instrument=instrument,
            )
        )

    def get_tickers(
        self, platforms: list[str], instruments: list[str]
    ) -> pb.GetTickersReply:
        return self._client.GetTickers(
            pb.GetTickersRequest(
                platforms=platforms,
                instruments=instruments,
            )
        )

    def get_kline(
        self,
        platform: str,
        instrument: str,
        resolution: str,
        start_timestamp: int = None,
        end_timestamp: int = None,
    ) -> list[pb.Kline]:
        return self._client.GetKline(
            pb.GetKlineRequest(
                platform=platform,
                instrument=instrument,
                resolution=resolution,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
            )
        )

    def get_orderbook(
        self, platform: str, instrument: str, size: int = 10
    ) -> pb.GetOrderBookReply:
        return self._client.GetOrderBook(
            pb.GetOrderBookRequest(
                platform=platform,
                instrument=instrument,
                depth=size,
            )
        )

    ##### trade #####

    def buy(
        self, platform: str, instrument: str, price: str, amount: str, **kwargs
    ) -> pb.BuyReply:
        return self._client.Buy(
            pb.BuyRequest(
                platform=platform,
                instrument=instrument,
                price=price,
                amount=amount,
                params=kwargs,
            )
        )

    def sell(
        self, platform: str, instrument: str, price: str, amount: str, **kwargs
    ) -> pb.SellReply:
        return self._client.Sell(
            pb.SellRequest(
                platform=platform,
                instrument=instrument,
                price=price,
                amount=amount,
                params=kwargs,
            )
        )

    def close_buy(
        self, platform: str, instrument: str, price: str, amount: str, **kwargs
    ) -> pb.CloseBuyReply:
        return self._client.CloseBuy(
            pb.CloseBuyRequest(
                platform=platform,
                instrument=instrument,
                price=price,
                amount=amount,
                params=kwargs,
            )
        )

    def close_sell(
        self, platform: str, instrument: str, price: str, amount: str, **kwargs
    ) -> pb.CloseSellReply:
        return self._client.CloseSell(
            pb.CloseSellRequest(
                platform=platform,
                instrument=instrument,
                price=price,
                amount=amount,
                params=kwargs,
            )
        )

    def get_order(
        self,
        platform: str,
        instrument: str,
        order_id: str,
        client_order_id: str,
        **kwargs,
    ) -> pb.Order:
        return self._client.GetOrder(
            pb.GetOrderRequest(
                platform=platform,
                instrument=instrument,
                order_id=order_id,
                client_order_id=client_order_id,
                params=kwargs,
            )
        )

    def get_orders(self, platform: str, instrument: str, **kwargs) -> pb.GetOrdersReply:
        return self._client.GetOrders(
            pb.GetOrdersRequest(
                platform=platform,
                instrument=instrument,
                params=kwargs,
            )
        )

    def get_position(self, platform: str, **kwargs) -> pb.GetPositionReply:

        return self._client.GetPosition(
            pb.GetPositionRequest(
                platform=platform,
                params=kwargs,
            )
        )

    def set_leverage(
        self, platform: str, instrument: str, leverage: int, **kwargs
    ) -> pb.SetLeverageReply:
        """设置杠杆

        Args:
            platform (str): 平台
            instrument (str): 标的
            leverage (int): 杠杆倍数

        Returns:
            pb.SetLeverageReply: 设置杠杆返回,包含设置杠杆的信息
        """
        return self._client.SetLeverage(
            pb.SetLeverageRequest(
                platform=platform,
                instrument=instrument,
                leverage=leverage,
                params=kwargs,
            )
        )
