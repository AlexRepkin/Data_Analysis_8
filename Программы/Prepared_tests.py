#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from pathlib import Path
import Individual as operations
import unittest


'''Модернизация индивидуального задания из работы №7.
Тестирование операций по работе с базой данных.

Напоминание о задании из работы №7: данные о людях хранятся в файле, создаваемом SQLite3 – people.db.
По умолчанию, файл создаётся в домашнем каталоге пользователя.
В данном файле имеется две таблицы – people и surnames'''


class TestDatabaseOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''Вызывается один раз для всего класса, в начале.'''
        print("~~~~~~~~~~~~~~")

    @classmethod
    def tearDownClass(cls):
        '''Вызывается один раз для всего класса, в конце.'''
        print("~~~~~~~~~~~~~~")
        print("Tests finished!")

    def setUp(self):
        '''Метод setUp вызывается перед каждым тестом для подготовки окружения.
        В данном случае он указывает имя для базы данных.'''
        self.store_tests = Path("test_database.db")
        print("~Test name:")

    def tearDown(self):
        '''Метод tearDown вызывается после каждого теста для очистки окружения.
        В данном случае он избавляется от временной базы данных после проведения тестов.'''
        if self.store_tests.exists():
            conn = sqlite3.connect(self.store_tests)
            conn.close()
            self.store_tests.unlink()
            print(" Succesfull!\n")

    def test_create_db(self):
        '''Тестирование создания базы данных.'''
        # Создание базы данных.
        print("Creating DB.")
        operations.create_db(self.store_tests)
        self.assertTrue(self.store_tests.exists())

        conn = sqlite3.connect(self.store_tests)
        cursor = conn.cursor()
        # Проверка, создалась ли база данных и нужные 2 таблицы одновременно!
        # Сначала получаем список всех таблиц в базе данных.
        # Потом сверяемся, есть ли surnames и people среди них.
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()  # Просто получение ответа.
        self.assertIn(('surnames',), tables)
        self.assertIn(('people',), tables)
        # Отключение от базы данных.
        conn.close()

    def test_new_human(self):
        '''Попытка добавления нового человека.'''
        print("New Human.")
        operations.create_db(self.store_tests)
        operations.new_human(self.store_tests, "Suzuki",
                             "Satoru", "40000000004", "2015-07-07")

        conn = sqlite3.connect(self.store_tests)
        cursor = conn.cursor()
        # Запрос. Сначала получение всех 4-ёх параметров (Кроме id человека), после чего относительно surname_id
        # из таблицы surnames, вставляются (Правильнее сказать соединяются) фамилии в таблицу people.
        cursor.execute(
            """
            SELECT people.name, surnames.surname, people.telephone, people.birthday
            FROM people
            INNER JOIN surnames ON surnames.surname_id = people.surname_id
            """
        )
        human = cursor.fetchone()
        # Проверка на не пустоту, после чего поэлементная проверка содержимого на правильность.
        self.assertIsNotNone(human)
        self.assertEqual(human[0], "Suzuki")
        self.assertEqual(human[1], "Satoru")
        self.assertEqual(human[2], "40000000004")
        self.assertEqual(human[3], "2015-07-07")
        conn.close()

    def test_select_all(self):
        '''Попытка получения вообще всех записей о людях.'''
        print("Selecting all people.")
        operations.create_db(self.store_tests)
        # Сразу 3 записи.
        operations.new_human(self.store_tests, "Suzuki",
                             "Satoru", "40000000004", "2015-07-07")
        operations.new_human(self.store_tests, "Alebrije",
                             "Wisdom", "99999999999", "2007-07-01")
        operations.new_human(self.store_tests, "Angus",
                             "Bambi", "30403040304", "2011-06-14")
        people = operations.select_all(self.store_tests)
        # Проверка, 3 ли записи получено, после чего все 3 проверяются на правильность.
        self.assertEqual(len(people), 3)
        self.assertEqual(len(people), 3)
        self.assertEqual(people[0]["name"], "Suzuki")
        self.assertEqual(people[0]["surname"], "Satoru")
        self.assertEqual(people[0]["telephone"], "40000000004")
        self.assertEqual(people[0]["birthday"], "2015-07-07")
        self.assertEqual(people[1]["name"], "Alebrije")
        self.assertEqual(people[1]["surname"], "Wisdom")
        self.assertEqual(people[1]["telephone"], "99999999999")
        self.assertEqual(people[1]["birthday"], "2007-07-01")
        self.assertEqual(people[2]["name"], "Angus")
        self.assertEqual(people[2]["surname"], "Bambi")
        self.assertEqual(people[2]["telephone"], "30403040304")
        self.assertEqual(people[2]["birthday"], "2011-06-14")

    def test_select_by_month(self):
        '''Попытка выбрать людей относительно их месяца рождения.'''
        print("Selecting people according to month.")
        operations.create_db(self.store_tests)
        operations.new_human(self.store_tests, "Suzuki",
                             "Satoru", "40000000004", "2015-07-07")
        operations.new_human(self.store_tests, "Alebrije",
                             "Wisdom", "99999999999", "2007-07-01")
        operations.new_human(self.store_tests, "Angus",
                             "Bambi", "30403040304", "2011-06-14")
        # Получение 7 месяца.
        both = operations.select_by_month(self.store_tests, 7)
        # Получение 6 месяца.
        only_one = operations.select_by_month(self.store_tests, 6)
        self.assertEqual(len(both), 2)
        self.assertEqual(both[0]["name"], "Suzuki")
        self.assertEqual(both[1]["name"], "Alebrije")
        self.assertEqual(len(only_one), 1)
        self.assertEqual(only_one[0]["name"], "Angus")


if __name__ == '__main__':
    unittest.main()
