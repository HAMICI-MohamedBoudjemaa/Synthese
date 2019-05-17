import logging


from colorlog import ColoredFormatter

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
# formatter = logging.Formatter('[%(asctime)s :: %(levelname)s ]:: %(message)s')
LOGFORMAT = "%(log_color)s[%(reset)s " \
            "%(log_color)s%(asctime)-8s%(reset)s " \
            "%(log_color)s::%(reset)s " \
            "%(log_color)s%(levelname)-8s%(reset)s " \
            "%(log_color)s]%(reset)s " \
            "%(log_color)s::%(reset)s" \
            " %(log_color)s%(message)s%(reset)s"
formatter = ColoredFormatter(LOGFORMAT)
# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def log_message(message, type):

    if type == 'info':
        logger.info(message)
    elif type == 'error':
        logger.error(message)
    elif type == 'warn':
        logger.warning(message)
    elif type == 'debug':
        logger.debug(message)


if __name__ == '__main__':
    """gp = 'lire'
    log_message('Curious users might want to know this '+gp,'info')
    log_message('Something is wrong and any user should be informed','warn')
    log_message('Serious stuff, this is red for a reason','error')
    log_message('A quirky message only developers care about','debug')"""
