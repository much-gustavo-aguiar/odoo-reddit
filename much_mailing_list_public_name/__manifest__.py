# Copyright much. Consulting (https://muchconsulting.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
{
    'name': 'Mailing List Public Name',
    'version': '19.0.1.0.0',
    'summary': 'Show a marketing-friendly name to recipients instead of the internal one',
    'description': """
Mailing List Public Name
========================

Features
--------
* Adds a *Public Name* to every mailing list, shown to recipients on the
  subscription and unsubscribe pages instead of the internal list name.
* When the public name is left empty, the internal name is shown, so existing
  lists keep working unchanged.

Technical notes
---------------
* Adds ``public_name`` (stored) and the computed ``public_name_display``
  (``public_name`` with a fallback to ``name``) on ``mailing.list``.
* Overrides the portal unsubscribe templates and the two controller methods
  that build recipient-facing list-name strings, so the internal name never
  leaks anywhere on the public pages.

Compatibility
-------------
* Odoo 19.0 Community (extends ``mass_mailing``).
""",
    'author': 'much. Consulting',
    'website': 'https://muchconsulting.com',
    'license': 'LGPL-3',
    'category': 'Marketing/Email Marketing',
    'depends': ['mass_mailing'],
    'data': [
        'views/mailing_list_views.xml',
        'views/mailing_subscription_templates.xml',
    ],
    'installable': True,
    'application': False,
}
