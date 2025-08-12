import gettext

_ = gettext.gettext

from configure import config, statistic


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
        if(statistic == 0):
            lang = get_system_lang()
        else:
            lang = config["language"]
        trans = gettext.translation("chinese_chess", "l10n", languages=[lang])
        trans.install()
        global _
        _ = trans.gettext
    except FileNotFoundError:
        print(f"Could not find translation files for language '{lang}', using default language.")


init_l10n()
