# Copyright much. Consulting (https://muchconsulting.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
{
    'name': 'Contacts Phone Country Flag',
    'version': '19.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Show the country flag next to phone numbers on contacts',
    'author': 'much. Consulting',
    'website': 'https://muchconsulting.com',
    'license': 'LGPL-3',
    'description': """
Contacts Phone Country Flag
===========================

Display a country flag emoji right before the phone number on the contact
form, for example ``🇧🇪 +32 2 340 02 25``. This makes international address
books much easier to scan, the way Gmail and other tools already do.

Features
--------

* Detects the country from the phone number's international prefix using the
  ``phonenumbers`` library (through Odoo's ``phone_validation`` module).
* Falls back to the contact's country (``country_id``) when the number is
  stored in national format.
* Shows nothing when no country can be determined, keeping the form clean.

Technical notes
---------------

* The flag value is a computed, non-stored field: it adds no database column
  and is only evaluated for the records actually displayed.
* It is rendered as a Unicode regional-indicator emoji, so it needs no image
  assets and no extra database lookups.
* The phone widget is a thin extension of the standard Odoo phone field; the
  rest of its behaviour (click-to-call, edit mode) is untouched.

Compatibility
-------------

Works on both Odoo Community and Enterprise (Odoo 19.0).
""",
    'depends': [
        'contacts',
        'phone_validation',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'contacts_phone_country_flag/static/src/**/*',
        ],
        'web.assets_tests': [
            'contacts_phone_country_flag/static/tests/**/*',
        ],
    },
    'installable': True,
    'application': False,
}
