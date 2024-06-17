# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FsConsolidationWsType(models.Model):
    _name = "fs_consolidation_ws_type"
    _inherit = [
        "mixin.master_data",
        "mixin.res_partner_m2o_configurator",
    ]
    _description = "Financial Statement Consolidation Worksheet Type"
    _res_partner_m2o_configurator_insert_form_element_ok = True
    _res_partner_m2o_configurator_form_xpath = "//page[@name='partner']"

    partner_ids = fields.Many2many(
        relation="rel_fs_consolidation_ws_type_2_partner",
    )
