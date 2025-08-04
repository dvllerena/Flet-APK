"""
Paquete de pestañas para LVentas
"""

from .summary_tab import SummaryTab
from .monthly_tab import MonthlyTab
from .accumulated_tab import AccumulatedTab
from .charts_tab import ChartsTab
from .base_tab import BaseTab
from .utils import *
from .config import *

__all__ = [
    'SummaryTab',
    'MonthlyTab', 
    'AccumulatedTab',
    'ChartsTab',
    'BaseTab'
]

__version__ = '1.0.0'
