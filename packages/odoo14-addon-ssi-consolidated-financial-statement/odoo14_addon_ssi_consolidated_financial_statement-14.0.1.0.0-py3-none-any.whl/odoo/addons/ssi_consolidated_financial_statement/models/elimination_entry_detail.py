# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EliminationEntryDetail(models.Model):
    _name = "elimination_entry.detail"
    _description = "Elimination Entry - Detail"

    entry_id = fields.Many2one(
        string="# Elimination Entry",
        comodel_name="elimination_entry",
        required=True,
        ondelete="cascade",
    )
    ws_id = fields.Many2one(
        string="# Consolidated Financial Statement Worksheet",
        related="entry_id.ws_id",
        store=True,
    )
    ws_detail_id = fields.Many2one(
        string="Consolidated Financial Statement Worksheet Detail",
        comodel_name="fs_consolidation_ws.detail",
        compute="_compute_ws_detail_id",
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
        "ws_id",
        "account_id",
        "ws_id.state",
    )
    def _compute_ws_detail_id(self):
        Detail = self.env["fs_consolidation_ws.detail"]
        for record in self:
            result = False
            if (
                record.ws_id
                and record.account_id
                and record.ws_id.state in ["open", "done"]
            ):
                criteria = [
                    ("ws_id", "=", record.ws_id.id),
                    ("account_id", "=", record.account_id.id),
                ]
                details = Detail.search(criteria)
                if len(details) > 0:
                    result = details[0]
            record.ws_detail_id = result
