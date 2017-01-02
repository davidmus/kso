from django import template
from django.template.defaultfilters import stringfilter
from django.utils.datastructures import SortedDict
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
@stringfilter
def obfuscate_mailto(value):
    mailto_re = re.compile('href="mailto:(?P<left>[^@]*)@(?P<right>[^"]*)"')
    replacement = 'class="email" onclick="var symbol=String.fromCharCode(0x40);this.href=&apos;mai&apos;+&apos;lto:&apos;+&apos;\g<left>&apos;+symbol+&apos;\g<right>&apos;;" href="#"'
    return mark_safe(mailto_re.sub(replacement, value))

@register.filter
@stringfilter
def remove_dots_from_ampm(value):
    value = re.sub(r'([aApP]\.?[mM](\.|,))',
        do_remove_dots_from_ampm,
        value)
    value = re.sub(r'^0', r'', value)
    return value

def do_remove_dots_from_ampm(match):
    return re.sub('\.', '', match.group(1).lower())

@register.filter
def order_by(value, field):
    return value.order_by(field)
