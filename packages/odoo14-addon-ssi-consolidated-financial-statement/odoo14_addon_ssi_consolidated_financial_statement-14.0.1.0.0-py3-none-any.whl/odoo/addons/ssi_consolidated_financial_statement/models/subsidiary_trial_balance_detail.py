# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SubsidiaryTrialBalanceDetail(models.Model):
    _name = "subsidiary_trial_balance.detail"
    _description = "Subsidiary Trial Balance - Detail"

    tb_id = fields.Many2one(
        string="# Subsidiary Trial Balance",
        comodel_name="subsidiary_trial_balance",
        required=True,
        ondelete="cascade",
    )
    ws_id = fields.Many2one(
        string="# Consolidated Financial Statement Worksheet",
        related="tb_id.ws_id",
        store=True,
    )
    ws_detail_id = fields.Many2one(
        string="Consolidated Financial Statement Worksheet Detail",
        comodel_name="fs_consolidation_ws.detail",
        compute="_compute_ws_detail_id",
        store=True,
    )
    adjustment_detail_ids = fields.One2many(
        string="Adjustment Detail",
        comodel_name="subsidiary_tb_adjustment_entry.detail",
        inverse_name="tb_detail_id",
    )
    partner_id = fields.Many2one(
        related="tb_id.partner_id",
        store=True,
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
    beginning_balance = fields.Monetary(
        string="Beginning Balance",
        required=True,
        default=0.0,
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
    adjustment_debit = fields.Monetary(
        string="Adjustment Debit",
        compute="_compute_adjustment",
        store=True,
    )
    adjustment_credit = fields.Monetary(
        string="Adjustment Credit",
        compute="_compute_adjustment",
        store=True,
    )
    ending_balance = fields.Monetary(
        string="Ending Balance",
        compute="_compute_ending_balance",
        store=True,
    )

    @api.depends(
        "ws_id",
        "account_id",
    )
    def _compute_ws_detail_id(self):
        Detail = self.env["fs_consolidation_ws.detail"]
        for record in self:
            if record.ws_id and record.account_id:
                criteria = [
                    ("ws_id", "=", record.ws_id.id),
                    ("account_id", "=", record.account_id.id),
                ]
                details = Detail.search(criteria)
                if len(details) > 0:
                    result = details[0]
            record.ws_detail_id = result

    @api.depends(
        "adjustment_detail_ids",
        "adjustment_detail_ids.debit",
        "adjustment_detail_ids.credit",
    )
    def _compute_adjustment(self):
        for record in self:
            debit = credit = 0.0
            for detail in record.adjustment_detail_ids:
                debit += detail.debit
                credit += detail.credit
            record.adjustment_debit = debit
            record.adjustment_credit = credit

    @api.depends(
        "beginning_balance",
        "debit",
        "credit",
        "adjustment_debit",
        "adjustment_credit",
    )
    def _compute_ending_balance(self):
        for record in self:
            result = (
                record.beginning_balance
                + record.debit
                - record.credit
                + record.adjustment_debit
                - record.adjustment_credit
            )
            record.ending_balance = result
