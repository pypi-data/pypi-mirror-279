from typing import List, Dict, TypeVar, Type

from pydantic import BaseModel
from requests import Session

from marketpalce_handler.config import settings
from marketpalce_handler.logger import logger
from marketpalce_handler.schemas import MsItem, BarcodesName, WbItem, OzonItem
from marketpalce_handler.validators import validate_ids_and_values


NameItem = TypeVar('NameItem', bound=BaseModel)


class Mapping:

    def __init__(self, url: str, mapping_token: str):
        self._logger = logger
        self.session = Session()
        self.session.headers.update(
            {
                "Authorization": mapping_token,
            }
        )
        self.mapping_url = url + "/collector/v1/mapping"
        self.product_url = url + "/collector/v1/products/additional/cmd_list"

    @validate_ids_and_values
    def get_mapped_data(self, ms_ids: List[str], values: List[int], name_market_barcode: BarcodesName) -> List[MsItem]:
        if len(ms_ids) == 1:
            ms_items = self.session.get(
                f"{self.mapping_url}", params={"ms_id": ms_ids[0]}
            )
            ms_items = ms_items.json()[0]
            ms_items["barcodes"] = ms_items[name_market_barcode.value]
            return [MsItem(**ms_items, value=values[0])]

        mapped_data = []
        for i in range(0, len(ms_ids), settings.MAPPING_LIMIT):
            ms_ids_chunk = ms_ids[i: i + settings.MAPPING_LIMIT]
            values_chunk = values[i: i + settings.MAPPING_LIMIT]
            ms_items = self.session.get(
                f"{self.mapping_url}", params={"ms_id": ",".join(ms_ids_chunk)}
            )

            id_value_map = dict(zip(ms_ids_chunk, values_chunk))

            for item in ms_items.json():
                value = id_value_map.get(item["ms_id"])
                item["value"] = value
                item["barcode"] = item[name_market_barcode]
                mapped_data.append(MsItem(**item))

        return mapped_data

    def get_mapped_data_by_nm_ids(self, stocks_data: Dict) -> List[Dict]:
        mapped_data = []
        response = []
        nm_ids = list(stocks_data.keys())
        for i in range(0, len(nm_ids), settings.MAPPING_LIMIT):
            nm_ids_chunk = nm_ids[i: i + settings.MAPPING_LIMIT]
            mapped_data.extend(
                self.session.get(
                    f"{self.mapping_url}", params={"nm_id": ",".join(nm_ids_chunk)}
                ).json()
            )

        for elem in mapped_data:
            if stocks_data.get(elem.get("nm_id")):
                response.append(
                    {
                        "ms_id": elem.get("ms_id"),
                        "nm_id": elem.get("nm_id"),
                        "barcode": stocks_data.get(elem.get("nm_id")).get("barcode"),
                        "quantity": stocks_data.get(elem.get("nm_id")).get("quantity"),
                    }
                )
        return response

    def get_product_data(self, ms_ids: list[str], name_base_item: Type[NameItem]) -> List[NameItem]:

        mapped_data = self.session.post(self.product_url, json={"ms_id": ms_ids}).json()
        return [name_base_item(**item) for item in mapped_data]

    def mapped_data(self, ms_products: list, market_products: dict, name_base_item: Type[NameItem], name_barcodes) -> List[NameItem]:

        mapped_data = []

        for ms_product in ms_products:
            instance = name_base_item(**ms_product)

            if name_base_item == WbItem and not instance.nm_id:
                self._logger.error(f"Product {instance.ms_id} does not have nm_id")
                continue
            elif name_base_item == OzonItem and not instance.code:
                self._logger.error(f"Product {instance.ms_id} does not have ozon_sku")
                continue

            barcode = getattr(instance, name_barcodes)

            if name_base_item == WbItem:
                instance.market_price = market_products.get(barcode)[0] if market_products.get(barcode) else None
                instance.market_discount = market_products.get(barcode)[1] if market_products.get(barcode) else None
            else:
                instance.market_price = market_products.get(barcode)

            if not instance.market_price:
                self._logger.error(f"For {instance.ms_id} not price in market {name_base_item.__name__}")
                continue

            mapped_data.append(instance)

            if len(market_products) == len(mapped_data):
                break

        return mapped_data
