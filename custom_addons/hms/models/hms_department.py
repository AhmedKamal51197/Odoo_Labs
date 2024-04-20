from odoo import  models,fields
class hmsDoctor(models.Model):
    _name = "hms.department"
    _rec_name = "Name"

    Name = fields.Char(required=True)
    Capacity = fields.Integer()
    Is_opened = fields.Boolean()

    patient_ids = fields.One2many(comodel_name="hms.patient",inverse_name="dept_id")