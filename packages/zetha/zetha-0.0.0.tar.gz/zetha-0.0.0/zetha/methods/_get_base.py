# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring
from typing import TYPE_CHECKING, Type
from importlib import import_module

if TYPE_CHECKING:
    from ..base import Base

def basemodel() -> Type['Base']:
    """Retorna modelo base"""
    base = import_module('zetha.base')
    base_model: Type['Base'] = getattr(base, 'Base')
    return base_model
