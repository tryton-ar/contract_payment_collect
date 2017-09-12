# This file is part of the contract_payment_collect module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['Contract', 'ContractConsumption']


class Contract:
    __metaclass__ = PoolMeta
    __name__ = 'contract'
    paymode = fields.Many2One(
        'payment.paymode',
        'Paymode', domain=[('party', '=', Eval('party'))],
        required=False)

    def __get_paymode(self):
        '''
        Return paymode.
        '''
        if self.party:
            if self.party.customer_paymode:
                self.paymode = self.party.customer_paymode

    @fields.depends('party', 'paymode')
    def on_change_party(self):
        self.paymode = None
        self.__get_paymode()


class ContractConsumption:
    __metaclass__ = PoolMeta
    __name__ = 'contract.consumption'

    @classmethod
    def _group_invoice_key(cls, line):
        grouping = super(ContractConsumption, cls)._group_invoice_key(line)

        consumption_id, _ = line
        consumption = cls(consumption_id)
        grouping.append(
            ('payment_collect', consumption.contract_line.contract.paymode))
        return grouping

    @classmethod
    def _invoice(cls, consumptions):
        Invoice = Pool().get('account.invoice')

        invoices = super(ContractConsumption, cls)._invoice(consumptions)

        to_write = []
        for invoice in invoices:
            contract = None
            for line in invoice.lines:
                if line.origin and line.origin.__name__ == 'contract.consumption':
                    contract = line.origin.contract_line.contract
                    break
            if contract and contract.paymode:
                to_write.extend(([invoice], {'paymode': contract.paymode}))

        if to_write:
            Invoice.write(*to_write)

        return invoices
