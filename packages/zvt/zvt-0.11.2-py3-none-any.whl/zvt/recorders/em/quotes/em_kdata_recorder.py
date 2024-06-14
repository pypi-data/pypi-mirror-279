# -*- coding: utf-8 -*-

import requests

from zvt.api.kdata import get_kdata_schema
from zvt.contract import IntervalLevel, AdjustType
from zvt.contract.api import df_to_db
from zvt.contract.recorder import FixedCycleDataRecorder
from zvt.domain import (
    Stock,
    Index,
    Block,
    StockKdataCommon,
    IndexKdataCommon,
    StockhkKdataCommon,
    StockusKdataCommon,
    BlockKdataCommon,
    Indexus,
    IndexusKdataCommon,
    Future,
    FutureKdataCommon,
    Currency,
    CurrencyKdataCommon,
)
from zvt.domain.meta.stockhk_meta import Stockhk
from zvt.domain.meta.stockus_meta import Stockus
from zvt.recorders.em.em_api import get_kdata
from zvt.utils.pd_utils import pd_is_not_null


class BaseEMStockKdataRecorder(FixedCycleDataRecorder):
    default_size = 50000
    entity_provider: str = "em"

    provider = "em"

    def __init__(
        self,
        force_update=True,
        sleeping_time=10,
        exchanges=None,
        entity_id=None,
        entity_ids=None,
        code=None,
        codes=None,
        day_data=False,
        entity_filters=None,
        ignore_failed=True,
        real_time=False,
        fix_duplicate_way="ignore",
        start_timestamp=None,
        end_timestamp=None,
        level=IntervalLevel.LEVEL_1DAY,
        kdata_use_begin_time=False,
        one_day_trading_minutes=24 * 60,
        adjust_type=AdjustType.qfq,
        return_unfinished=False,
    ) -> None:
        level = IntervalLevel(level)
        self.adjust_type = AdjustType(adjust_type)
        self.entity_type = self.entity_schema.__name__.lower()

        self.data_schema = get_kdata_schema(entity_type=self.entity_type, level=level, adjust_type=self.adjust_type)

        super().__init__(
            force_update,
            sleeping_time,
            exchanges,
            entity_id,
            entity_ids,
            code,
            codes,
            day_data,
            entity_filters,
            ignore_failed,
            real_time,
            fix_duplicate_way,
            start_timestamp,
            end_timestamp,
            level,
            kdata_use_begin_time,
            one_day_trading_minutes,
            return_unfinished,
        )

    def record(self, entity, start, end, size, timestamps):
        if not self.http_session:
            self.http_session = requests.Session()

        df = get_kdata(
            session=self.http_session, entity_id=entity.id, limit=size, adjust_type=self.adjust_type, level=self.level
        )
        if pd_is_not_null(df):
            df_to_db(df=df, data_schema=self.data_schema, provider=self.provider, force_update=self.force_update)
        else:
            self.logger.info(f"no kdata for {entity.id}")

    def on_finish_entity(self, entity):
        # fill timestamp
        if not entity.timestamp or not entity.list_date:
            # get the first
            kdatas = self.data_schema.query_data(
                provider=self.provider,
                entity_id=entity.id,
                order=self.data_schema.timestamp.asc(),
                limit=1,
                return_type="domain",
            )
            if kdatas:
                timestamp = kdatas[0].timestamp

                self.logger.info(f"fill {entity.name} list_date as {timestamp}")

                if not entity.timestamp:
                    entity.timestamp = timestamp
                if not entity.list_date:
                    entity.list_date = timestamp
                self.entity_session.add(entity)
                self.entity_session.commit()


class EMStockKdataRecorder(BaseEMStockKdataRecorder):
    entity_schema = Stock
    data_schema = StockKdataCommon


class EMStockusKdataRecorder(BaseEMStockKdataRecorder):
    entity_provider = "em"
    entity_schema = Stockus
    data_schema = StockusKdataCommon


class EMStockhkKdataRecorder(BaseEMStockKdataRecorder):
    entity_provider = "em"
    entity_schema = Stockhk
    data_schema = StockhkKdataCommon


class EMIndexKdataRecorder(BaseEMStockKdataRecorder):
    entity_provider = "em"
    entity_schema = Index

    data_schema = IndexKdataCommon


class EMIndexusKdataRecorder(BaseEMStockKdataRecorder):
    entity_provider = "em"
    entity_schema = Indexus

    data_schema = IndexusKdataCommon


class EMBlockKdataRecorder(BaseEMStockKdataRecorder):
    entity_provider = "em"
    entity_schema = Block

    data_schema = BlockKdataCommon


class EMFutureKdataRecorder(BaseEMStockKdataRecorder):
    entity_provider = "em"
    entity_schema = Future

    data_schema = FutureKdataCommon


class EMCurrencyKdataRecorder(BaseEMStockKdataRecorder):
    entity_provider = "em"
    entity_schema = Currency

    data_schema = CurrencyKdataCommon


if __name__ == "__main__":
    df = Stock.query_data(filters=[Stock.exchange == "bj"], provider="em")
    entity_ids = df["entity_id"].tolist()
    recorder = EMStockKdataRecorder(
        level=IntervalLevel.LEVEL_1DAY, entity_ids=entity_ids, sleeping_time=0, adjust_type=AdjustType.hfq
    )
    recorder.run()
# the __all__ is generated
__all__ = [
    "BaseEMStockKdataRecorder",
    "EMStockKdataRecorder",
    "EMStockusKdataRecorder",
    "EMStockhkKdataRecorder",
    "EMIndexKdataRecorder",
    "EMIndexusKdataRecorder",
    "EMBlockKdataRecorder",
    "EMFutureKdataRecorder",
    "EMCurrencyKdataRecorder",
]
