from odoo import models,fields
class hmsDepartment(models.Model):
    _name="hms.doctor"
    _rec_name ="First_Name"

    First_Name = fields.Char(required=True)
    Last_Name = fields.Char(required=True)
    image = fields.Binary(attachment=True)

