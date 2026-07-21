# database/connection.py
import sqlite3
import threading
from config import Config

class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._connection = sqlite3.connect(
                    Config.DATABASE_PATH,
                    check_same_thread=False,
                    isolation_level=None  # دستی transactionها را مدیریت می‌کنیم
                )
                cls._instance._connection.execute("PRAGMA journal_mode=WAL;")
                cls._instance._connection.execute("PRAGMA foreign_keys=ON;")
        return cls._instance

    @property
    def connection(self):
        return self._connection

    def execute(self, query, params=()):
        """اجرای یک کوئری با مدیریت قفل نویسی"""
        with self._lock:
            cursor = self._connection.execute(query, params)
            return cursor

    def executemany(self, query, seq):
        with self._lock:
            self._connection.executemany(query, seq)

    def commit(self):
        with self._lock:
            self._connection.commit()

    def close(self):
        with self._lock:
            self._connection.close()
