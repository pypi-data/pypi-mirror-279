"""初始化"""

from pathlib import Path
import polars as pl
from vxsched.core import ON_INIT_EVENT
from vxsched import vxsched, VXEvent
from vxutils import VXContext


@vxsched.register(ON_INIT_EVENT)
def init(context: VXContext, mod: str) -> None:
    """初始化"""
    context.calendar = pl.read_csv(
        Path.home() / ".data" / "calendar.csv", dtypes={"date": pl.Date}
    )
    
