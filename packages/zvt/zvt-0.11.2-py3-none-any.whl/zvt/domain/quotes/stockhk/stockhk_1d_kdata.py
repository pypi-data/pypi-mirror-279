# -*- coding: utf-8 -*-
# this file is generated by gen_kdata_schema function, dont't change it
from sqlalchemy.orm import declarative_base

from zvt.contract.register import register_schema
from zvt.domain.quotes import StockhkKdataCommon

KdataBase = declarative_base()


class Stockhk1dKdata(KdataBase, StockhkKdataCommon):
    __tablename__ = "stockhk_1d_kdata"


register_schema(providers=["em"], db_name="stockhk_1d_kdata", schema_base=KdataBase, entity_type="stockhk")

# the __all__ is generated
__all__ = ["Stockhk1dKdata"]
