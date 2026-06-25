import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { formPhoneField, PhoneField } from "@web/views/fields/phone/phone_field";

export class PhoneCountryFlagField extends PhoneField {
    static template = "contacts_phone_country_flag.PhoneCountryFlagField";

    get countryFlag() {
        return this.props.record.data[`${this.props.name}_country_flag`] || "";
    }
}

export const phoneCountryFlagField = {
    ...formPhoneField,
    component: PhoneCountryFlagField,
    displayName: _t("Phone with country flag"),
    // Auto-load the matching computed flag field (e.g. phone -> phone_country_flag)
    // so the widget can read it without declaring it in the view.
    fieldDependencies: ({ name }) => [{ name: `${name}_country_flag`, type: "char" }],
};

registry.category("fields").add("phone_country_flag", phoneCountryFlagField);
