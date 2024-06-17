# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SubsidiaryTbAdjustmentEntry(models.Model):
    _name = "subsidiary_tb_adjustment_entry.detail"
    _description = "Subsidiary TB Adjustment Entry - Detail"

    entry_id = fields.Many2one(
        string="# Subsidiary TB Adjustment Entry",
        comodel_name="subsidiary_tb_adjustment_entry",
        required=True,
        ondelete="cascade",
    )
    tb_id = fields.Many2one(
        string="# Subsidiary Trial Balance",
        related="entry_id.tb_id",
        store=True,
    )
    tb_detail_id = fields.Many2one(
        string="Subsidiary Trial Balance Detail",
        comodel_name="subsidiary_trial_balance.detail",
        compute="_compute_tb_detail_id",
        store=True,
    )
    currency_id = fields.Many2one(
        related="entry_id.company_currency_id",
        store=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account_type",
        required=True,
        ondelete="restrict",
    )
    name = fields.Char(
        string="Label",
        required=True,
    )
    ref = fields.Char(
        string="Ref",
        required=True,
    )
    debit = fields.Monetary(
        string="Debit",
        required=True,
        default=0.0,
    )
    credit = fields.Monetary(
        string="Credit",
        required=True,
        default=0.0,
    )

    @api.depends(
        "tb_id",
        "account_id",
        "entry_id.state",
    )
    def _compute_tb_detail_id(self):
        Detail = self.env["subsidiary_trial_balance.detail"]
        for record in self:
            result = False
            if record.tb_id and record.account_id and record.entry_id.state in ["done"]:
                criteria = [
                    ("tb_id", "=", record.tb_id.id),
                    ("account_id", "=", record.account_id.id),
                ]
                details = Detail.search(criteria)
                if len(details) > 0:
                    result = details[0]
            record.tb_detail_id = result
