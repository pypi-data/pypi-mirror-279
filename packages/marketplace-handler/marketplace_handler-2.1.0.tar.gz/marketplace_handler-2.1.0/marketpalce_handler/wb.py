import json
from time import sleep
from datetime import datetime
from typing import List

from requests import HTTPError

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from .exceptions import InitialisationException, InvalidStatusException
from .logger import logger
from .config import settings
from .mapping import Mapping
from .marketplace import Marketplace
from .schemas import WbAccount, WbItem
from .utils import get_chunks, is_too_small_price
from .validators import (
    validate_ids_and_values,
    validate_id_and_value,
    validate_statuses,
    validate_date_string,
)


class Wildberries(Marketplace):
    def __init__(
        self,
        account_data: WbAccount,
        mapping_url,
        mapping_token,
        max_price_requests: int = 5,
        session: requests.Session = requests.Session(),
    ):
        self._logger = logger
        self._session = session
        self._mapping_service = Mapping(mapping_url, mapping_token)
        self._max_price_requests = max_price_requests
        retries = Retry(
            total=3,
            backoff_factor=0.5,
        )
        self._session.mount("https://", HTTPAdapter(max_retries=retries))

        self.warehouse_id = account_data.warehouse_id
        self._session.headers.update(
            {
                "Authorization": f"{account_data.common_token}",
            }
        )

        if not hasattr(self, "warehouse_id"):
            self._logger.error("Warehouse id is not found")
            raise InitialisationException("Warehouse id is not found")

        self._logger.debug("Wildberries is initialized")

    def get_stock(self, ms_id: str):
        try:
            assert isinstance(ms_id, str)
            ms_items = self._mapping_service.get_mapped_data([ms_id], [0])[0]
            stocks = self._session.post(
                f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                json={
                    "skus": [ms_items.barcodes],
                },
                timeout=5,
            )
            stocks.raise_for_status()
            return stocks.json()
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {ms_id} stock is not refreshed. Error: {e}"
            )
            raise e

    def get_stocks(
        self, date: str = datetime.now().strftime("%Y-%m-%d")
    ):
        """
        Get stocks updated for a specific date or datetime.
        To obtain the full stocks' quantity, the earliest possible value should be specified.

        Args:
            date (str, optional): The date or datetime string in "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS" format.
                Defaults to the current date in "YYYY-MM-DD" format.

        Raises:
            ValueError: If the input string is not in either date or datetime format.
            HTTPError: If the method is called more than once in a minute.
        """
        try:
            validate_date_string(date)
            url = f"{settings.wb_statistic_url}api/v1/supplier/stocks?dateFrom={date}"

            stocks_response = self._session.get(url)
            stocks_response.raise_for_status()
            stocks_data = {}
            if stocks_response.json():
                for stock in stocks_response.json():
                    stocks_data[str(stock["nmId"])] = {
                        "barcode": stock["barcode"],
                        "quantity": stock["quantityFull"],
                    }
            return self._mapping_service.get_mapped_data_by_nm_ids(stocks_data)
        except HTTPError as e:
            self._logger.error(f"Wildberries: too many responses. Error: {e}")
            raise e
        except Exception as e:
            self._logger.error(f"Wildberries: error while getting stocks. Error: {e}")
            raise e

    @validate_id_and_value
    def refresh_stock(self, ms_id: str, value: int):
        try:
            ms_items = self._mapping_service.get_mapped_data([ms_id], [value])[0]
            refresh_stock_resp = self._session.put(
                f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                json={
                    "stocks": [
                        {
                            "sku": ms_items.barcodes,
                            "amount": value,
                        },
                    ]
                },
                timeout=5,
            )
            refresh_stock_resp.raise_for_status()
            self._logger.info(f"Wildberries: {ms_id} stock is refreshed")
            return True
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {ms_id} stock is not refreshed. Error: {e}"
            )
            raise e

    @validate_ids_and_values
    def refresh_stocks(self, ms_ids: List[str], values: List[int]):
        try:
            json_data = []
            if len(ms_ids) > settings.WB_ITEMS_REFRESH_LIMIT:
                chunks_ids, chunks_values = get_chunks(ms_ids, values)
                for chunk_ids, chunk_values in zip(chunks_ids, chunks_values):
                    self.refresh_stocks(chunk_ids, chunk_values)

            for item in self._mapping_service.get_mapped_data(ms_ids, values):
                json_data.append(
                    {
                        "sku": item.barcodes,
                        "amount": item.value,
                    }
                )
            refresh_stocks_resp = self._session.put(
                f"{settings.wb_api_url}api/v3/stocks/{self.warehouse_id}",
                json={
                    "stocks": json_data,
                },
                timeout=5,
            )
            refresh_stocks_resp.raise_for_status()
            return True
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {ms_ids} stock is not refreshed. Error: {e}"
            )
            raise e

    def get_prices_from_market(self) -> dict:
        products = dict()
        default_offset = 0

        while True:
            response = self._session.get(
                f"{settings.wb_price_url}api/v2/list/goods/filter",
                timeout=50,
                params={
                    "limit": settings.WB_ITEMS_REFRESH_LIMIT,
                    "offset": default_offset,
                },
            )
            try:
                response.raise_for_status()
            except HTTPError as e:
                self._logger.error(f"Wildberries: prices are not refreshed. Error: {e}")
                raise e

            list_goods = response.json().get('data').get('listGoods')

            if not list_goods:
                break

            products.update(
                {
                    str(product["nmID"]): (product["sizes"][0]["price"], product["discount"])
                    for product in list_goods
                }
            )
            default_offset += + settings.WB_ITEMS_REFRESH_LIMIT

        return products

    @validate_id_and_value
    def refresh_price(self, product_data: WbItem):
        try:

            if is_too_small_price(price_from_ms=product_data.price, price_from_market=product_data.market_price):
                self._logger.warning(f"Price decreased by 30% or more for ms_id: {product_data.ms_id}.")
                return {
                    product_data.ms_id: {
                        "price_from_ms": product_data.price,
                        "price_from_market": product_data.market_price
                    }
                }

            self._update_prices([product_data])
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {product_data.ms_id} price is not refreshed. Error: {e}"
            )
            raise e

    def refresh_prices(self, products_data: List[WbItem]):

        suspicious_products = {}

        valid_products = []
        for product in products_data:
            if is_too_small_price(price_from_ms=product.price, price_from_market=product.market_price):
                suspicious_products[product.ms_id] = {
                    "price_from_ms": product.price,
                    "price_from_market": product.market_price,
                    "code": product.code
                }
                continue
            elif product.market_discount != settings.WB_DISCOUNT:
                product.market_discount = settings.WB_DISCOUNT

            valid_products.append(product)

        for i in range(0, len(valid_products), settings.WB_ITEMS_REFRESH_LIMIT):

            self._update_prices(valid_products[i: i + settings.WB_ITEMS_REFRESH_LIMIT])

        return suspicious_products

    def _update_prices(self, items: List[WbItem]):
        for i in range(0, len(items), settings.WB_ITEMS_REFRESH_LIMIT):
            prepare_data = {
                int(item.nm_id): {
                    "price": int(item.price),
                    "discount": int(item.market_discount)}
                for item in items[i: i + settings.WB_ITEMS_REFRESH_LIMIT]
                }

            price_update_resp = self._session.post(
                f"{settings.wb_price_url}api/v2/upload/task",
                json={"data": [
                    {"nmID": key, "price": value.get("price"), "discount": value.get("discount")}
                    for key, value in prepare_data.items()
                ]},
                timeout=50,
            )
            sleep(2)
            try:
                price_update_resp.raise_for_status()
            except HTTPError as e:
                if e.response.status_code == 400:
                    text = json.loads(e.response.text)
                    if text.get('errorText') == "No goods for process":
                        self._logger.warning(
                            f"Wildberries: The price and discount that we are"
                            f" trying to put coincides with the current one on the market"
                        )
                else:
                    self._logger.error(f"Wildberries: prices are not refreshed. Error: {e}")
                    raise e

            self._logger.info(
                f"response: {price_update_resp.status_code} {price_update_resp.json()}"
            )

    def refresh_status(self, wb_order_id: int, status_name: str, supply_id: str = None):
        assert isinstance(wb_order_id, int)
        assert isinstance(status_name, str)
        try:
            match status_name:
                case "confirm":
                    supply_id = supply_id or self._session.post(
                        f"{settings.wb_api_url}api/v3/supplies",
                        json={"name": f"supply_order{wb_order_id}"},
                        timeout=5,
                    ).json().get("id")
                    add_order_to_supply_resp = requests.patch(
                        f"{settings.wb_api_url}api/v3/supplies/{supply_id}/orders/{wb_order_id}",
                    )
                    add_order_to_supply_resp.raise_for_status()
                case "cancel":
                    cancel_order_resp = requests.patch(
                        f"{settings.wb_api_url}api/v3/orders/{wb_order_id}/cancel"
                    )
                    cancel_order_resp.raise_for_status()
                case _:
                    raise InvalidStatusException(
                        f"{status_name} is not valid status name"
                    )
            return True
        except HTTPError as e:
            self._logger.error(
                f"Wildberries: {wb_order_id} status is not refreshed. Error: {e}"
            )
            raise e

    @validate_statuses
    def refresh_statuses(self, wb_order_ids: List[int], statuses: List[str]):
        try:
            new_supply = self._session.post(
                f"{settings.wb_api_url}api/v3/supplies",
                json={"name": "supply_orders"},
                timeout=5,
            ).json()

            for wb_order_id, status in zip(wb_order_ids, statuses):
                self.refresh_status(
                    wb_order_id=wb_order_id,
                    status_name=status,
                    supply_id=new_supply.get("id"),
                )
            return True
        except HTTPError as e:
            self._logger.error(f"Wildberries: can't create new supply. Error: {e}")
            raise e
