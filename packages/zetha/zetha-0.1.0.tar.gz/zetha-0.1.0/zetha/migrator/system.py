# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring
from ..base import Base

class System(Base):
    "Classe abstrata de migrador"
    __abstract__ = True
    SYSTEM = 'migrator'
