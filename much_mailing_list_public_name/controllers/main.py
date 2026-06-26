# Copyright much. Consulting (https://muchconsulting.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from werkzeug.exceptions import NotFound, Unauthorized

from odoo import _, http
from odoo.http import request

from odoo.addons.mass_mailing.controllers.main import MassMailController


class MassMailPublicNameController(MassMailController):
    """ Use the mailing list public name in the recipient-facing strings that
    core builds in Python (the template-rendered lists are handled in QWeb).
    These two methods mirror core ``mass_mailing`` and only swap ``name`` for
    ``public_name_display``. """

    @http.route('/mailing/<int:mailing_id>/confirm_unsubscribe', type='http', website=True, auth='public')
    def mailing_confirm_unsubscribe(self, mailing_id, document_id=None, email=None, hash_token=None):
        mailing = request.env['mailing.mailing'].sudo().browse(mailing_id)
        # check that mailing exists/has access
        email_found, hash_token_found = self._fetch_user_information(email, hash_token)
        try:
            self._check_mailing_email_token(
                mailing_id, document_id, email_found, hash_token_found,
                required_mailing_id=True
            )
        except NotFound as e:  # avoid leaking ID existence
            raise Unauthorized() from e

        unsubscribed_lists = ''
        # Display public list name if list is public
        if mailing.mailing_model_real == 'mailing.contact':
            unsubscribed_lists = ', '.join(
                mailing_list.public_name_display
                for mailing_list in mailing.contact_list_ids if mailing_list.is_public
            )

        return request.render('mass_mailing.page_mailing_confirm_unsubscribe', {
            'mailing_id': mailing_id,
            'document_id': document_id,
            'email': email,
            'hash_token': hash_token,
            'unsubscribed_lists': unsubscribed_lists,
        })

    def _mailing_unsubscribe_from_list(self, mailing, document_id, email, hash_token):
        # Unsubscribe directly + Let the user choose their subscriptions

        mailing.contact_list_ids._update_subscription_from_email(email, opt_out=True)
        # compute name of unsubscribed list: hide non public lists, use public name
        if all(not mlist.is_public for mlist in mailing.contact_list_ids):
            lists_unsubscribed_name = _('You are no longer part of our mailing list(s).')
        elif len(mailing.contact_list_ids) == 1:
            lists_unsubscribed_name = _('You are no longer part of the %(mailing_name)s mailing list.',
                                        mailing_name=mailing.contact_list_ids.public_name_display)
        else:
            lists_unsubscribed_name = _(
                'You are no longer part of the %(mailing_names)s mailing list.',
                mailing_names=', '.join(
                    mlist.public_name_display for mlist in mailing.contact_list_ids if mlist.is_public
                )
            )

        return request.render(
            'mass_mailing.page_mailing_unsubscribe',
            dict(
                self._prepare_mailing_subscription_values(
                    mailing, document_id, email, hash_token
                ),
                last_action='subscription_updated',
                unsubscribed_name=lists_unsubscribed_name,
            )
        )
