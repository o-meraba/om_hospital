# -*- coding: utf-8 -*-
from odoo import fields, models


class ResGroups(models.Model):
    _inherit = 'res.groups'

    def get_application_groups(self,domain):
        group_id = self.env.ref('project.group_project_task_dependencies').id
        wave_group_id = self.env.ref('stock.group_stock_picking_wave').id
        performa_sale_id = self.env.ref('sale.group_proforma_sales').id
        return super(ResGroups, self).get_application_groups(domain + [('id', 'not in', (group_id, wave_group_id, performa_sale_id))])