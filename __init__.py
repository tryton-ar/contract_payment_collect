# This file is part of the contract_payment_collect module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import contract


def register():
    Pool.register(
        contract.Contract,
        contract.ContractConsumption,
        module='contract_payment_collect', type_='model')
