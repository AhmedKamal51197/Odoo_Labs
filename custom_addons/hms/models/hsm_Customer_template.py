from odoo import models,fields,api
from odoo.exceptions import ValidationError

class hmsCustomerTemplate(models.Model):
    _inherit = 'res.partner'



    related_patient_id = fields.Many2one(comodel_name='hms.patient',string='Related Patient')

    vat = fields.Char(required=True)
    @api.constrains('related_patient_id')
    def check_only_one_patient(self):
        for record in self:
            existing_record = self.search([('related_patient_id.id','=',record.id),('id','!=',record.id)])
            if len (existing_record )>0 :
                raise ValidationError('it must be one patient related to only one customer')

 