#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Unified Chip Design Platform - AMBA - AHB Multilayer.
"""

from logging import getLogger
from typing import ClassVar

import ucdp as u
from ucdp_glbl import AddrMaster, AddrMatrix, AddrRef, AddrSlave

from . import types as t

LOGGER = getLogger(__name__)


class Master(AddrMaster):
    """
    Master.
    """

    proto: t.AmbaProto
    """Protocol Version."""


class Slave(AddrSlave):
    """
    Slave.
    """

    proto: t.AmbaProto
    """Protocol Version."""


class UcdpAhbMlMod(u.ATailoredMod, AddrMatrix):
    """
    AHB Multilayer.

    Multilayer.
    """

    filelists: ClassVar[u.ModFileLists] = (
        u.ModFileList(
            name="hdl",
            gen="full",
            filepaths=("$PRJROOT/{mod.topmodname}/{mod.modname}.sv"),
            template_filepaths=("ucdp_ahb2apb.sv.mako", "sv.mako"),
        ),
    )
    proto: t.AmbaProto = t.AmbaProto()
    """Default Protocol."""
    is_sub: bool = False
    """Full Address Decoding By Default."""

    def _build(self):
        self.add_port(u.ClkRstAnType(), "main_i")

    def add_master(
        self,
        name: str,
        slavenames: u.Names | None = None,
        proto: t.AmbaProto | None = None,
        route: u.Routeable | None = None,
    ) -> Master:
        """
        Add master port named `name` connected to `route`.

        Args:
            name: Name or Pattern ('*' is supported)

        Keyword Args:
            slavenames: Names of slaves to be accessed by this master.
            proto: Protocol.
            route: port to connect this master to.
        """
        self.check_lock()
        proto = proto or self.proto
        master = Master(name=name, proto=proto)
        self._add_master(master, slavenames=slavenames)

        portname = f"ahb_mst_{name}_i"
        title = f"AHB Input {name!r}"
        self.add_port(t.AhbMstType(proto=proto), portname, title=title, comment=title)
        if route:
            self.con(portname, route)

        return master

    def add_slave(
        self,
        name: str,
        baseaddr=u.AUTO,
        size: u.Bytes | None = None,
        proto: t.AmbaProto | None = None,
        masternames: u.Names | None = None,
        route: u.Routeable | None = None,
        ref: u.BaseMod | str | None = None,
    ):
        """
        Add APB Slave.

        Args:
            name: Slave Name.

        Keyword Args:
            baseaddr: Base address, Next Free address by default. Do not add address space if `None`.
            size: Address Space.
            proto: AMBA Protocol Selection.
            masternames: Names of masters to be accessed by this slave.
            route: APB Slave Port to connect.
            ref: Logical Module connected.
        """
        self.check_lock()
        proto = proto or self.proto
        slave = Slave(name=name, addrdecoder=self, proto=proto, ref=ref)
        self._add_slave(slave, masternames=masternames, baseaddr=baseaddr, size=size)

        portname = f"ahb_slv_{name}_o"
        title = f"AHB Output {name!r}"
        self.add_port(t.AhbSlvType(proto=proto), portname, title=title, comment=title)
        if route:
            self.con(portname, route)

        return slave

    def _builddep(self):
        self._check_masters_slaves()

    @staticmethod
    def build_top(**kwargs):
        """Build example top module and return it."""
        return UcdpAhbMlExampleMod()

    def _resolve_ref(self, ref: AddrRef) -> AddrRef:
        return self.parent.parser(ref)

    def get_overview(self) -> str:
        """Matrix Overview."""
        return AddrMatrix.get_overview(self)


class UcdpAhbMlExampleMod(u.AMod):
    """
    Just an Example Multilayer.

    >>> print(UcdpAhbMlExampleMod().get_inst('u_ml').get_overview())
     Master > Slave    ram    periph    misc
    ----------------  -----  --------  ------
          ext           X
          dsp           X       X
    <BLANKLINE>
    <BLANKLINE>
    Size: 3.75 GB
    <BLANKLINE>
    | Addrspace | Type     | Base       | Size                    | Attributes |
    | --------- | ----     | ----       | ----                    | ---------- |
    | reserved0 | Reserved | 0x0        | 1006632960x32 (3.75 GB) |            |
    | ram       | Slave    | 0xF0000000 | 16384x32 (64 KB)        |            |
    | periph    | Slave    | 0xF0010000 | 16384x32 (64 KB)        |            |
    | misc      | Slave    | 0xF0020000 | 8192x32 (32 KB)         |            |
    | reserved1 | Reserved | 0xF0028000 | 67067904x32 (255.84 MB) |            |
    <BLANKLINE>
    """

    def _build(self):
        ml = UcdpAhbMlMod(self, "u_ml")
        ml.add_master("ext")
        ml.add_master("dsp")

        slv = ml.add_slave("ram", masternames=["ext", "dsp"])
        slv.add_addrrange(0xF0000000, size=2**16)

        slv = ml.add_slave("periph")
        slv.add_addrrange(0xF0010000, size="64kb")

        slv = ml.add_slave("misc")
        slv.add_addrrange(size="32k")

        # slv = ml.add_slave("ext", masternames=["ext", "dsp"])
        # slv.add_addrrange(0x0, size=2**32)
        # slv.add_exclude_addrrange(0xF0000000, size=2**18)

        ml.add_interconnects("dsp", "periph")
        ml.add_interconnects("external", "misc")
