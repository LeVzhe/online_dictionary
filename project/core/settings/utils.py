# flake8: noqa: N802, N803

import logging
import logging.config
import logging.handlers
import os
from datetime import datetime


class DailyDirectoryRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, filename, maxBytes=0, backupCount=0, encoding=None, delay=False):
        # Создаем путь к папке с текущей датой
        self._date = datetime.now().strftime("%d-%m-%Y")
        self._logs_dir = os.path.join("logs", self._date)

        # Создаем папку если ее нет
        os.makedirs(self._logs_dir, exist_ok=True)

        # Полный путь к файлу лога
        full_path = os.path.join(self._logs_dir, filename)

        super().__init__(
            full_path,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
        )

    def shouldRollover(self, record):
        # Проверяем, изменилась ли дата
        current_date = datetime.now().strftime("%d-%m-%Y")
        if current_date != self._date:
            return 1

        # Иначе проверяем по размеру файла
        return super().shouldRollover(record)

    def doRollover(self):
        # Закрываем текущий файл
        self.close()

        # Обновляем дату
        self._date = datetime.now().strftime("%d-%m-%Y")
        self._logs_dir = os.path.join("logs", self._date)
        os.makedirs(self._logs_dir, exist_ok=True)

        # Создаем новый файл
        self.baseFilename = os.path.join(self._logs_dir, os.path.basename(self.baseFilename))

        # Открываем новый файл
        if not self.delay:
            self.stream = self._open()
