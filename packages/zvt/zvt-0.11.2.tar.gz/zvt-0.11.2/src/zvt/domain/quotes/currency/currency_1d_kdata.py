# -*- coding: utf-8 -*-
# this file is generated by gen_kdata_schema function, dont't change it
from sqlalchemy.orm import declarative_base

from zvt.contract.register import register_schema
from zvt.domain.quotes import CurrencyKdataCommon

KdataBase = declarative_base()


class Currency1dKdata(KdataBase, CurrencyKdataCommon):
    __tablename__ = "currency_1d_kdata"


register_schema(providers=["em"], db_name="currency_1d_kdata", schema_base=KdataBase, entity_type="currency")

# the __all__ is generated
__all__ = ["Currency1dKdata"]
