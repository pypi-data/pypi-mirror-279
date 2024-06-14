import requests

from urllib3 import Retry
from typing import Optional, Dict, List
from requests import HTTPError
from requests.adapters import HTTPAdapter

from marketpalce_handler.config import settings
from marketpalce_handler.mapping import Mapping
from marketpalce_handler.logger import logger
from marketpalce_handler.utils import is_too_small_price
from marketpalce_handler.schemas import YandexItem, YandexAccount
from marketpalce_handler.marketplace import Marketplace
from marketpalce_handler.exceptions import InitialisationException
from marketpalce_handler.validators import validate_id_and_value, validate_ids_and_values


class Yandex(Marketplace):
    stock_limit = settings.YANDEX_STOCK_LIMIT

    def __init__(
            self,
            account_data: YandexAccount,
            mapping_url: str,
            mapping_token: str,
            session: requests.Session = requests.Session()
    ):
        self._name = account_data.name
        self._campaign_id = account_data.campaign_id
        self._business_id = account_data.business_id
        self._logger = logger

        self._mapping_service = Mapping(mapping_url, mapping_token)

        self._session = session
        retries = Retry(total=3, backoff_factor=0.5)
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

        self._session.headers.update(
            {
                "Authorization": f"Bearer {account_data.token}"
            }
        )

        if not hasattr(self, "_campaign_id") or not hasattr(self, "_business_id"):
            self._logger.error(f"Campaing or Business id not found for account name: {self._name}")
            raise InitialisationException(f"Campaing or Business id not found for account name: {self._name}")

        self._logger.info(f"Yandex account for {self._name} if initialized.")

    def get_stocks(self, page_token: Optional[str] = None):
        request_params = {
            "url": f"{settings.yandex_api_url}/businesses/{self._business_id}/offer-mappings",
            "params": {"page_token": page_token} if page_token else None
        }

        stocks = self._session.post(**request_params, timeout=5)

        try:
            stocks.raise_for_status()
        except HTTPError as e:
            self._logger.error(f"Cannot get stocks for account: {self._name}")
            raise e
        else:
            return stocks.json()

    def get_prices_from_market(self) -> Dict:
        products_from_market = {}
        page_token = None

        while True:
            products = self.get_stocks(page_token=page_token)
            paging = products.get("result").get("paging")

            page_token = paging.get("nextPageToken") if paging else None

            for product in products.get("result").get("offerMappings"):
                barcode = product.get("offer").get("barcodes")
                barcode = barcode[0] if isinstance(barcode, list) else barcode

                try:
                    products_from_market.update(
                        {
                            barcode: product.get("offer").get("basicPrice").get('value')
                        }
                    )
                except AttributeError:
                    self._logger.error(f"Product with barcode: {barcode} on Yandex Market doesn't have price!")

            if not page_token:
                return products_from_market

    @validate_id_and_value
    def refresh_stock(self, ms_id: str, value: int):

        ms_items = self._mapping_service.get_mapped_data([ms_id], [value])[0]

        refresh_stock_resp = self._session.post(
            url=f"{settings.yandex_api_url}/businesses/{self._business_id}/offer-mappings/update",
            json={
                "skus": [
                    {
                        "sku": ms_items.barcodes,
                        "items": [
                            {
                                "count": ms_items.value
                            }
                        ]
                    }
                ]
            },
            timeout=5
        )
        try:
            refresh_stock_resp.raise_for_status()
        except HTTPError as exc:
            self._logger.error(f"Yandex {ms_id} stock is not refreshed. Error: {exc}")
            raise exc
        else:
            self._logger.info(f"Yandex {ms_id} stock if refreshed")
            return True

    @validate_id_and_value
    def refresh_price(self, ms_id: str, price_from_market: int):
        product_data = self._mapping_service.get_product_data([ms_id], YandexItem)[0]
        offer_id = product_data.yandex_barcodes

        if is_too_small_price(price_from_ms=product_data.price, price_from_market=price_from_market):
            self._logger.warning(f"Price decreased by 50% or more for ms_id: {ms_id}.")
            return {
                product_data.ms_id: {
                    "price_from_ms": product_data.price,
                    "price_from_market": product_data.market_price
                }
            }

        response = self._session.post(
            url=f"{settings.yandex_api_url}/businesses/{self._business_id}/offer-prices/updates",
            json={
                "offers": [
                    {
                        "offerId": offer_id,
                        "price": {
                            "value": int(product_data.price),
                            "currencyId": "RUR",
                            "discountBase": int(product_data.discount_base)
                        }
                    }
                ]
            },
            timeout=5
        )
        return response.json()

    @validate_ids_and_values
    def refresh_stocks(self, ms_ids: list[int], values: list[int]):

        for pos in range(0, len(ms_ids), self.stock_limit):
            items = self._mapping_service.get_mapped_data(
                ms_ids=ms_ids[pos: pos + self.stock_limit],
                values=values[pos: pos + self.stock_limit]
            )

            refresh_stocks_resp = self._session.post(
                url=f"{settings.yandex_api_url}/businesses/{self._business_id}/offer-mappings/update",
                json={
                    "skus": [
                        {
                            "sku": item.barcodes,
                            "items": [{"count": item.value}]
                        } for item in items
                    ]
                },
                timeout=5
            )
            try:
                refresh_stocks_resp.raise_for_status()
                self._logger("Many updates stocks for yandex is completed.")
            except HTTPError as exc:
                self._logger.error(f"Cannot update many items. Error: {exc}")
                raise exc

        return True

    def refresh_prices(self, products_data: List[YandexItem]):

        suspicious_products = {}

        valid_products = []
        for product in products_data:
            if is_too_small_price(
                    price_from_ms=product.price,
                    price_from_market=product.market_price
            ):
                suspicious_products[product.ms_id] = {
                    "price_from_ms": product.price,
                    "price_from_market": product.market_price
                }
            else:
                valid_products.append(product)

        for i in range(0, len(valid_products), self.stock_limit):
            refresh_stocks_resp = self._session.post(
                url=f"{settings.yandex_api_url}/businesses/{self._business_id}/offer-prices/updates",
                json={
                    "offers": [
                        {
                            "offerId": item.offer_id,
                            "price": {
                                "value": int(item.price),
                                "currencyId": "RUR",
                                "discountBase": int(item.discount_base)
                            }
                        } for item in valid_products[i: i + self.stock_limit]
                    ]
                },
                timeout=5
            )
            try:
                refresh_stocks_resp.raise_for_status()
                self._logger("Many updates stocks for yandex is completed.")
            except HTTPError as exc:
                self._logger.error(f"Cannot update many items. Error: {exc}")
                raise exc

        return suspicious_products

    def refresh_status(self, ms_id, value):
        raise NotImplementedError

    def refresh_statuses(self, ids: list[int], values: list[str]):
        raise NotImplementedError
