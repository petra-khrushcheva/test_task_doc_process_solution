import logging

from config import LogConfig


def configure_logging(log_config: LogConfig):

    logger = logging.getLogger()
    logger.setLevel(log_config.level)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(module)-20s] [LINE:%(lineno)-3d] #%(levelname)-7s %(message)s"  # noqa
    )

    # Обработчик для вывода в консоль
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
