# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


"""class vc_mail_account_invoice(models.Model):
  _inherit='account.invoice'

  def _notify_get_groups(self, message, groups):
    grups = super(vc_mail_account_invoice, self)._notify_get_groups(message, groups)
    for group_name, group_method, group_data in grups:
      if group_name in ('customer', 'portal', 'portal_customer'):
          group_data['has_button_access'] = False
          continue
      group_data['has_button_access'] = True

    return grups
    """
