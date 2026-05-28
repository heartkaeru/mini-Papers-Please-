import unittest
from datetime import date

import config
from model import Checker, Decision, Document, Economy, GameModel, GameRules, Person, PersonGenerator


def make_valid_person() -> Person:
    birth_date = date(2007, 1, 1)
    document = Document(
        full_name="Иванов Иван Иванович",
        group="ИС-123456",
        birth_date=birth_date,
        education_form="очная",
        education_level="бакалавриат",
        institute="ИнЭУ",
        issue_date=date(2024, 9, 1),
    )

    return Person(
        full_name="Иванов Иван Иванович",
        group="ИС-123456",
        birth_date=birth_date,
        document=document,
    )


class FixedGenerator:
    def __init__(self, person: Person):
        self.person = person

    def generate(self) -> Person:
        return self.person


class CheckerTest(unittest.TestCase):
    def setUp(self):
        self.checker = Checker(GameRules())

    def test_valid_student_card_is_allowed(self):
        person = make_valid_person()

        result = self.checker.get_result(person)

        self.assertTrue(result.allow)
        self.assertEqual(result.errors, ())

    def test_person_without_student_card_is_denied(self):
        person = make_valid_person()
        person.document = None

        result = self.checker.get_result(person)

        self.assertFalse(result.allow)
        self.assertIn(config.ERROR_NO_DOCUMENT, result.errors)

    def test_bad_birth_year_is_denied(self):
        person = make_valid_person()
        person.document.birth_date = date(2008, 1, 1)

        result = self.checker.get_result(person)

        self.assertFalse(result.allow)
        self.assertIn(config.ERROR_BAD_BIRTH_DATE, result.errors)

    def test_bad_issue_date_is_denied(self):
        person = make_valid_person()
        person.document.issue_date = date(2026, 9, 1)

        result = self.checker.get_result(person)

        self.assertFalse(result.allow)
        self.assertIn(config.ERROR_BAD_ISSUE_DATE, result.errors)

    def test_bad_group_format_is_denied(self):
        person = make_valid_person()
        person.document.group = "ИС123456"

        result = self.checker.get_result(person)

        self.assertFalse(result.allow)
        self.assertIn(config.ERROR_BAD_GROUP_FORMAT, result.errors)

    def test_bad_group_prefix_is_denied(self):
        person = make_valid_person()
        person.document.group = "ЮР-123456"

        result = self.checker.get_result(person)

        self.assertFalse(result.allow)
        self.assertIn(config.ERROR_BAD_GROUP_PREFIX, result.errors)

    def test_bad_education_form_is_denied(self):
        person = make_valid_person()
        person.document.education_form = "Домашняя"

        result = self.checker.get_result(person)

        self.assertFalse(result.allow)
        self.assertIn(config.ERROR_BAD_EDUCATION_FORM, result.errors)

    def test_bad_education_level_is_denied(self):
        person = make_valid_person()
        person.document.education_level = "Супервысшее"

        result = self.checker.get_result(person)

        self.assertFalse(result.allow)
        self.assertIn(config.ERROR_BAD_EDUCATION_LEVEL, result.errors)

    def test_bad_institute_is_denied(self):
        person = make_valid_person()
        person.document.institute = "Факультет без расписания"

        result = self.checker.get_result(person)

        self.assertFalse(result.allow)
        self.assertIn(config.ERROR_BAD_INSTITUTE, result.errors)


class PersonGeneratorTest(unittest.TestCase):
    def test_generated_valid_person_has_correct_student_card(self):
        rules = GameRules()
        generator = PersonGenerator(rules, seed=1)

        person = generator._generate_valid_person()
        result = Checker(rules).get_result(person)

        self.assertTrue(result.allow)
        self.assertIsNotNone(person.document)
        self.assertEqual(len(person.full_name.split()), 3)

        issue_age = person.document.issue_date.year - person.document.birth_date.year
        self.assertIn(issue_age, config.VALID_ISSUE_AGES)


class EconomyTest(unittest.TestCase):
    def test_correct_result_adds_money(self):
        economy = Economy(money=0, reward=10, fine_amount=5)

        money_delta = economy.apply_result(True)

        self.assertEqual(money_delta, 10)
        self.assertEqual(economy.money, 10)

    def test_mistake_takes_money(self):
        economy = Economy(money=0, reward=10, fine_amount=5)

        money_delta = economy.apply_result(False)

        self.assertEqual(money_delta, -5)
        self.assertEqual(economy.money, -5)


class GameModelTest(unittest.TestCase):
    def test_allowing_valid_person_is_correct(self):
        person = make_valid_person()
        game = GameModel(generator=FixedGenerator(person))

        result = game.decide(Decision.ALLOW)

        self.assertTrue(result.is_correct)
        self.assertEqual(result.money_delta, config.DEFAULT_REWARD)
        self.assertEqual(result.balance, config.DEFAULT_REWARD)

    def test_denying_person_without_card_is_correct(self):
        person = make_valid_person()
        person.document = None
        game = GameModel(generator=FixedGenerator(person))

        result = game.decide(Decision.DENY)

        self.assertTrue(result.is_correct)
        self.assertEqual(result.money_delta, config.DEFAULT_REWARD)

    def test_wrong_decision_can_end_game(self):
        person = make_valid_person()
        rules = GameRules(
            fine_for_mistake=5,
            dismissal_balance_limit=-5,
        )
        economy = Economy(money=0, reward=10, fine_amount=5)
        game = GameModel(
            rules=rules,
            generator=FixedGenerator(person),
            economy=economy,
        )

        result = game.decide(Decision.DENY)

        self.assertFalse(result.is_correct)
        self.assertTrue(result.game_over)
        self.assertEqual(result.balance, -5)


if __name__ == "__main__":
    unittest.main()
