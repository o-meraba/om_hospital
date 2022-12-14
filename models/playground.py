from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

class OdooPlayGround(models.Model):
    _name = "odoo.playground"
    _description = "Odoo PlayGround"

    DEFAULT_ENV_VARIABLES = """# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered; is a void recordset
#  - record: record on which the action is triggered; may be void
#  - records: recordset of all records on which the action is triggered in multi-mode; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - float_compare: Odoo function to compare floats based on specific precisions
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - UserError: Warning Exception to use with raise
#  - Command: x2Many commands namespace
# To return an action, assign: action = {...}"""
    model_id = fields.Many2one('ir.model', string='Model')
    code = fields.Text(string="Code")
    result = fields.Text(string='Result')


    def action_clear(self):
        self.code = ''
        self.result = ''
    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            if self.code:
                self.result = safe_eval(self.code.strip(), {'self': model}, mode="eval")
            else:
                self.result = "Enter some codes to evaluate"
        except Exception as e:
            self.result = str(e)