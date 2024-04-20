import  re
from datetime import date
from odoo import models,fields,api
from odoo.exceptions import ValidationError

class hmsPatientHistoryLog(models.Model):
    _name="hms.patient.history.log"
    description = fields.Text()
    patient_id = fields.Many2one(comodel_name="hms.patient")


class hmsPatient(models.Model):
    _name='hms.patient'
    _rec_name = 'First_name'
    First_name = fields.Char(required=True)
    Last_name = fields.Char(required=True)
    Birth_date = fields.Date()
    History = fields.Html()
    CR_Ratio = fields.Float(required=True)
    Blood_type = fields.Selection([
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
    ])
    pcr = fields.Boolean()
    image = fields.Binary(attachment=True)
    Address = fields.Text()


    state = fields.Selection([
        ('Undetermined','Undetermined'),
        ('Good','Good'),
        ('Fair','Fair'),
        ('Serious','Serious')])

    dept_id = fields.Many2one(comodel_name="hms.department")
    dept_capacity = fields.Integer(related="dept_id.Capacity")
    doctors_ids = fields.Many2many(comodel_name="hms.doctor")
    history_log_ids = fields.One2many(comodel_name='hms.patient.history.log',inverse_name='patient_id')
    email = fields.Char(string='Email')

    Age = fields.Integer(compute='_compute_age', store=True)
    # customer_id = fields.Many2one(comodel_name='res.partner')

    @api.constrains('email')
    def Check_Unique_Email(self):
        for record in self:
            existing_record=self.search([('email','=',record.email),('id','!=',record.id)])
            if len(existing_record)>0:
                raise ValidationError('Patient Email %s already exist you must enter unique email'%record.email)
    @api.constrains('email')
    def _Validate_email(self):
        for record in self:
            if record.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError ('Patient Email invalid %s'%record.email)
    # @api.onchange('state')
    # def state_log(self):
    #     vals = {
    #         'description': 'state change to %s' % self.state,
    #         'patient_id': self.id
    #     }
    #     self.env['hms.patient.history.log'].create(vals)
    #
    @api.depends('Birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.Birth_date:
                today = date.today()
                rec.Age = today.year - rec.Birth_date.year - (
                        (today.month, today.day) < (rec.Birth_date.month, rec.Birth_date.day))
            else:
                rec.Age = 4
    def change_state(self):
        x=1
        if self.state=='Undetermined':
            self.state='Good'
            x=0
        elif self.state=='Good':
            self.state='Fair'
            x=0
        elif self.state=='Fair':
            self.state='Serious'
            x=0
        if x==0:
            vals = {
                'description': 'state change to %s' % self.state,
                'patient_id': self.id
            }
            self.env['hms.patient.history.log'].create(vals)

    @api.onchange('Age')
    def _onchange_pcr(self):
        if self.Age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'SELECTED PCR Sucess.'
                }
            }
        else:
            self.pcr = False
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'Pcr not selected.'
                }
            }
    @api.onchange('History')
    def create_history_log(self):
        vals = {
            'description':'History change to %s'%self.History,
            'patient_id':self.id
        }
        self.env['hms.patient.history.log'].create(vals)

