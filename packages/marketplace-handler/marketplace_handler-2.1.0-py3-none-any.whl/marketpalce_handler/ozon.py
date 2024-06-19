from typing import List

import requests
from requests import Session, HTTPError
from requests.adapters import HTTPAdapter, Retry

from .schemas import OzonItem, OzonAccount
from .exceptions import InitialisationException
from .mapping import Mapping
from .marketplace import Marketplace
from .logger import logger
from .config import settings
from .utils import get_chunks, is_too_small_price
from .validators import validate_id_and_value, validate_ids_and_values


class Ozon(Marketplace):
    def __init__(
        self,
        account_data: OzonAccount,
        mapping_url: str,
        mapping_token: str,
        session: Session = requests.Session(),
    ):
        self._name = account_data.name
        self.warehouse_id = account_data.warehouse_id
        self._mapping_service = Mapping(mapping_url, mapping_token)
        self._logger = logger
        self._session = session
        self._ozon_item_schema = OzonItem
        retries = Retry(
            total=3,
            backoff_factor=0.5,
        )
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

        self._session.headers.update(
            {
                "Client-Id": account_data.client_id,
                "Api-Key": account_data.api_key,
            }
        )

        if not hasattr(self, "warehouse_id"):
            self._logger.error(f"Warehouse ID not found for account name: {self._name}")
            raise InitialisationException(f"Warehouse ID not found for account name: {self._name}")

        self._logger.info("Ozon marketplace is initialised")

    def get_prices_from_market(self) -> dict:
        products_from_market = {}
        last_id = ''

        while True:

            resp = self._session.post(
                f"{settings.ozon_api_url}v4/product/info/prices",
                json={
                    "filter": {"visibility": "ALL"},
                    "limit": "1000",
                    "last_id": last_id
                },
            ).json()

            if resp.get('code'):
                break

            products_from_market.update(
                {
                    item['offer_id']: float(item['price']['price']) for item in resp['result']['items']
                }
            )

            last_id = resp.get('result').get('last_id')

            if not last_id:
                break

        return products_from_market

    def refresh_prices(self, products_data: List[OzonItem]):
        suspicious_products = {}
        valid_products = []

        for product in products_data:
            if is_too_small_price(price_from_ms=product.ozon_after_discount,
                                  price_from_market=product.market_price
                                  ):
                suspicious_products[product.ms_id] = {
                    "price_from_ms": product.ozon_after_discount,
                    "price_from_market": product.market_price,
                    "code": product.code
                }
            else:
                valid_products.append(product)

        for i in range(0, len(valid_products), settings.OZONE_PRICE_LIMIT):

            response = self._session.post(
                f"{settings.ozon_api_url}v1/product/import/prices",
                json={"prices": [
                    {"offer_id": item.code, "price": str(item.ozon_after_discount), "min_price": str(item.ozon_after_discount)}
                    for item in valid_products[i: i + settings.OZONE_PRICE_LIMIT]
                ]}
            )
            try:
                response.raise_for_status()
                self._logger.info("Many updates stocks for ozon is completed.")
            except HTTPError as exc:
                self._logger.error(f"Get Error while updating price in ozon. {exc}")
                raise exc

        return suspicious_products

    @validate_id_and_value
    def refresh_price(self, ms_id: str, value: int):
        mapped_data = self._mapping_service.get_product_data([ms_id], self._ozon_item_schema)
        offer_id = mapped_data[0].offer_id
        resp = self._session.post(
            f"{settings.ozon_api_url}v1/product/import/prices",
            json={"prices": [{"offer_id": offer_id, "price": str(value)}]},
        )
        return resp.json()

    @validate_id_and_value
    def refresh_stock(self, ms_id: str, value: int):
        mapped_data = self._mapping_service.get_product_data([ms_id], self._ozon_item_schema)
        offer_id = mapped_data[0].offer_id
        resp = self._session.post(
            f"{settings.ozon_api_url}v1/product/import/stocks",
            json={"stocks": [{"offer_id": offer_id, "stock": value}]},
        )
        return resp.json()

    @validate_id_and_value
    def refresh_stock_by_warehouse(self, ms_id: str, value: int):
        mapped_data = self._mapping_service.get_product_data([ms_id], self._ozon_item_schema)
        offer_id = mapped_data[0].offer_id
        resp = self._session.post(
            f"{settings.ozon_api_url}v2/products/stocks",
            json={
                "stocks": [
                    {"offer_id": offer_id, "stock": value, "warehouse_id": self.warehouse_id}
                ]
            },
        )
        return resp.json()

    @validate_ids_and_values
    def refresh_stocks(self, ms_ids: List[str], values: List[int]):
        response = []
        mapped_data = self._mapping_service.get_product_data(ms_ids, self._ozon_item_schema)
        ids_map = {item.ms_id: item.offer_id for item in mapped_data}
        if len(ms_ids) > settings.OZON_STOCK_LIMIT:
            chunks_ids, chunks_values = get_chunks(
                ms_ids, values, settings.OZON_STOCK_LIMIT
            )
            for chunk_ids, chunk_values in zip(chunks_ids, chunks_values):
                response.extend(self.refresh_stocks(chunk_ids, chunk_values))

        stocks = []
        for ms_id, value in zip(ms_ids, values):
            stocks.append({"offer_id": ids_map[ms_id], "stock": value})
        stocks_data = self._session.post(
            f"{settings.ozon_api_url}v1/product/import/stocks", json={"stocks": stocks}
        ).json()
        response.append(stocks_data)
        return response

    @validate_ids_and_values
    def refresh_stocks_by_warehouse(self, ms_ids: List[str], values: List[int]):
        mapped_data = self._mapping_service.get_product_data(ms_ids, self._ozon_item_schema)
        ids_map = {item.ms_id: item.offer_id for item in mapped_data}
        stocks = []
        for ms_id, value, warehouse in zip(ms_ids, values):
            stocks.append(
                {"offer_id": ids_map[ms_id], "stock": value, "warehouse_id": self.warehouse_id}
            )
        return self._session.post(
            f"{settings.ozon_api_url}v2/products/stocks", json={"stocks": stocks}
        ).json()

    def refresh_status(self, wb_order_id, status):
        raise NotImplementedError

    def refresh_statuses(self, wb_order_ids, statuses):
        raise NotImplementedError
