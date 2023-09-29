from django.utils.translation import gettext_lazy as _


DOCUMENT_TYPE_LIST = (
    ('none', _('--none--')),
    ('DNI', _('DNI')),
    ('alien-certificate', _('alien_certificate')),
    ('passport', _('passport')),
    ('cedula', _('cedula')),
    ('ID', _('ID')),
    ('CPP', _('CPP')),
    ('CURP', _('CURP')),
)