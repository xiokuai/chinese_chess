import gettext

_ = gettext.gettext


def get_system_lang():
    import locale
    import os

    if hasattr(locale, "LC_MESSAGES"):
        lang = locale.getlocale(locale.LC_MESSAGES)[0]
        if lang:
            return lang

    lang = locale.getlocale()[0]
    if lang:
        return lang

    lang = os.environ.get("LANG", "en_US").split(".")[0]
    return lang


def init_l10n():
    try:
        lang = get_system_lang()
        trans = gettext.translation("chinese_chess", "locale", languages=[lang])
        trans.install()
        _ = trans.gettext
    except FileNotFoundError:
        print("Could not find translation files, using default language.")
