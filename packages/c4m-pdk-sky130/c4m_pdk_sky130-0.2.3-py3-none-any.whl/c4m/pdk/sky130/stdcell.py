# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import Optional, Any, cast

from pdkmaster.technology import primitive as _prm
from pdkmaster.design import library as _lbry

from c4m.flexcell import factory as _fab

from .pdkmaster import tech, cktfab, layoutfab

__all__ = ["StdCellFactory", "stdcellcanvas", "stdcelllib"]

prims = tech.primitives


class StdCellFactory(_fab.StdCellFactory):
    def __init__(self, *,
        lib: _lbry.RoutingGaugeLibrary,
        name_prefix: str = "", name_suffix: str = "",
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            name_prefix=name_prefix, name_suffix=name_suffix,
            canvas=stdcellcanvas,
        )


stdcellcanvas = _fab.StdCellCanvas(
    tech=tech, **_fab.StdCellCanvas.compute_dimensions_lambda(lambda_=0.05),
    nmos=cast(_prm.MOSFET, prims.nfet_01v8), pmos=cast(_prm.MOSFET, prims.pfet_01v8),
    nimplant=cast(_prm.Implant, prims.nsdm), pimplant=cast(_prm.Implant, prims.psdm),
)


_stdcelllib: Optional[_lbry.RoutingGaugeLibrary] = None
stdcelllib: _lbry.RoutingGaugeLibrary
def __getattr__(name: str) -> Any:
    if name == "stdcelllib":
        global _stdcelllib
        if _stdcelllib is None:
            _stdcelllib = _lbry.RoutingGaugeLibrary(
                name="StdCellLib", tech=tech, routinggauge=stdcellcanvas.routinggauge,
            )
            StdCellFactory(lib=_stdcelllib).add_default()
        return _stdcelllib
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
