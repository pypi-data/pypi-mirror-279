# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FsConsolidationWsDetail(models.Model):
    _name = "fs_consolidation_ws.detail"
    _description = "Financial Statement Consolidation - Detail"

    ws_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="fs_consolidation_ws",
        required=True,
        ondelete="cascade",
    )
    tb_detail_ids = fields.One2many(
        string="Trial Balance Detail",
        comodel_name="subsidiary_trial_balance.detail",
        inverse_name="ws_detail_id",
    )
    elimination_entry_detail_ids = fields.One2many(
        string="Elimination Entry Detail",
        comodel_name="elimination_entry.detail",
        inverse_name="ws_detail_id",
    )
    currency_id = fields.Many2one(
        related="ws_id.company_currency_id",
        store=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account_type",
        required=True,
        ondelete="restrict",
    )
    parent_balance = fields.Monetary(
        string="Parent Balance",
        required=True,
        default=0.0,
    )
    child_balance = fields.Monetary(
        string="Subsidiary Balance",
        compute="_compute_child_balance",
        store=True,
    )
    balance = fields.Monetary(
        string="Balance",
        compute="_compute_balance",
        store=True,
    )
    elimination_debit = fields.Monetary(
        string="Elimination Dr.",
        compute="_compute_elimination",
        store=True,
    )
    elimination_credit = fields.Monetary(
        string="Elimination Cr.",
        compute="_compute_elimination",
        store=True,
    )
    consolidated = fields.Monetary(
        string="Consolidated",
        compute="_compute_consolidated",
        store=True,
    )

    @api.depends(
        "tb_detail_ids",
        "tb_detail_ids.ending_balance",
    )
    def _compute_child_balance(self):
        for record in self:
            result = 0.0
            for detail in record.tb_detail_ids:
                result += detail.ending_balance
            record.child_balance = result

    @api.depends(
        "parent_balance",
        "child_balance",
    )
    def _compute_balance(self):
        for record in self:
            result = record.parent_balance + record.child_balance
            record.balance = result

    @api.depends(
        "elimination_entry_detail_ids",
        "elimination_entry_detail_ids.debit",
        "elimination_entry_detail_ids.credit",
    )
    def _compute_elimination(self):
        for record in self:
            debit = credit = 0.0
            for detail in record.elimination_entry_detail_ids:
                debit += detail.debit
                credit += detail.credit
            record.elimination_debit = debit
            record.elimination_credit = credit

    @api.depends(
        "balance",
        "elimination_debit",
        "elimination_credit",
    )
    def _compute_consolidated(self):
        for record in self:
            result = (
                record.balance + record.elimination_debit - record.elimination_credit
            )
            record.consolidated = result
