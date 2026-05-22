from __future__ import annotations

import random
import re
from datetime import date, timedelta
from enum import Enum
from typing import List, Optional, Tuple, Union


class Decision(Enum):
    ALLOW = "allow"
    DENY = "deny"


class GameRules:
    def __init__(
        self,
        min_age: int = 16,
        group_pattern: str = r"^[А-Я]{2}-\d{6}$",
        valid_group_prefixes: Tuple[str, ...] = ("ИС", "ПИ", "БИ", "ЭК", "МТ"),
        reward_for_correct_decision: int = 10,
        fine_for_mistake: int = 5,
        prison_balance_limit: int = -50,
        current_date: Optional[date] = None,
    ):
        self.min_age = min_age
        self.group_pattern = group_pattern
        self.valid_group_prefixes = valid_group_prefixes
        self.reward_for_correct_decision = reward_for_correct_decision
        self.fine_for_mistake = fine_for_mistake
        self.prison_balance_limit = prison_balance_limit
        self.current_date = current_date or date.today()

    def instruction_lines(self) -> List[str]:
        prefixes = ", ".join(self.valid_group_prefixes)
        return [
            "Пропускать только людей с пропуском.",
            "Срок действия пропуска не должен быть истекшим.",
            f"Возраст посетителя должен быть от {self.min_age} лет.",
            f"Группа должна иметь формат АА-000000 и начинаться с: {prefixes}.",
            "Данные в пропуске должны совпадать с данными посетителя.",
        ]


class Economy:
    def __init__(self, money: int = 0, reward: int = 10, fine_amount: int = 5):
        self.money = money
        self.reward = reward
        self.fine_amount = fine_amount

    def add_money(self, amount: Optional[int] = None) -> int:
        value = self.reward if amount is None else amount
        self.money += value
        return value

    def fine(self, amount: Optional[int] = None) -> int:
        value = self.fine_amount if amount is None else amount
        self.money -= value
        return -value

    def apply_result(self, is_correct: bool) -> int:
        if is_correct:
            return self.add_money()
        return self.fine()


class Document:
    def __init__(
        self,
        name: str = "",
        age: int = 0,
        group: str = "",
        valid_until: Optional[date] = None,
    ):
        self.name = name
        self.age = age
        self.group = group
        self.valid_until = valid_until

    def is_expired(self, current_date: date) -> bool:
        if self.valid_until is None:
            return True
        return self.valid_until < current_date

    def display_valid_until(self) -> str:
        if self.valid_until is None:
            return "нет данных"
        return self.valid_until.strftime("%d.%m.%Y")


class Person:
    def __init__(
        self,
        name: str = "",
        age: int = 0,
        group: str = "",
        document: Optional[Document] = None,
        is_important: bool = False,
    ):
        self.name = name
        self.age = age
        self.group = group
        self.document = document
        self.is_important = is_important

    def display_data(self) -> List[str]:
        return [
            f"Имя: {self.name}",
            f"Возраст: {self.age}",
            f"Группа: {self.group}",
        ]

    def document_data(self) -> List[str]:
        if self.document is None:
            return ["Пропуска нет"]

        return [
            f"Имя: {self.document.name}",
            f"Возраст: {self.document.age}",
            f"Группа: {self.document.group}",
            f"Действителен до: {self.document.display_valid_until()}",
        ]


class CheckResult:
    def __init__(self, allow: bool, errors: Tuple[str, ...]):
        self.allow = allow
        self.errors = errors


class RoundResult:
    def __init__(
        self,
        player_decision: Decision,
        correct_decision: Decision,
        is_correct: bool,
        errors: Tuple[str, ...],
        money_delta: int,
        balance: int,
        game_over: bool,
        game_over_reason: str = "",
    ):
        self.player_decision = player_decision
        self.correct_decision = correct_decision
        self.is_correct = is_correct
        self.errors = errors
        self.money_delta = money_delta
        self.balance = balance
        self.game_over = game_over
        self.game_over_reason = game_over_reason


class PersonGenerator:
    def __init__(self, rules: Optional[GameRules] = None, seed: Optional[int] = None):
        self.rules = rules or GameRules()
        self.random = random.Random(seed)
        self.names = [
            "Артур",
            "Саша",
            "Данил",
            "Алина",
            "Мария",
            "Илья",
            "Кирилл",
            "Вика",
            "Егор",
        ]
        self.invalid_reasons = [
            "no_document",
            "expired_document",
            "too_young",
            "bad_group_format",
            "bad_group_prefix",
            "wrong_name",
            "wrong_age",
            "wrong_group",
        ]

    def generate(self) -> Person:
        person = self._generate_valid_person()

        should_be_invalid = self.random.random() < 0.45
        if should_be_invalid:
            self._apply_random_error(person)

        return person

    def _generate_valid_person(self) -> Person:
        name = self.random.choice(self.names)
        age = self.random.randint(self.rules.min_age, 30)
        group = self._generate_valid_group()
        valid_until = self.rules.current_date + timedelta(days=self.random.randint(1, 120))

        return Person(
            name=name,
            age=age,
            group=group,
            document=Document(
                name=name,
                age=age,
                group=group,
                valid_until=valid_until,
            ),
        )

    def _apply_random_error(self, person: Person) -> None:
        reason = self.random.choice(self.invalid_reasons)

        if reason == "no_document":
            person.document = None
            return

        document = person.document
        if document is None:
            return

        if reason == "expired_document":
            document.valid_until = self.rules.current_date - timedelta(days=self.random.randint(1, 60))
        elif reason == "too_young":
            person.age = self.random.randint(10, self.rules.min_age - 1)
            document.age = person.age
        elif reason == "bad_group_format":
            document.group = self.random.choice(["123456", "АА123456", "A1-000001", "ГРУППА"])
        elif reason == "bad_group_prefix":
            document.group = f"ЮР-{self.random.randint(100000, 999999)}"
        elif reason == "wrong_name":
            possible_names = [name for name in self.names if name != person.name]
            document.name = self.random.choice(possible_names)
        elif reason == "wrong_age":
            document.age = person.age + self.random.choice([-2, -1, 1, 2])
        elif reason == "wrong_group":
            document.group = self._generate_valid_group(exclude=person.group)

    def _generate_valid_group(self, exclude: Optional[str] = None) -> str:
        while True:
            prefix = self.random.choice(self.rules.valid_group_prefixes)
            group = f"{prefix}-{self.random.randint(100000, 999999)}"
            if group != exclude:
                return group


class Checker:
    def __init__(self, rules: Optional[GameRules] = None):
        self.rules = rules or GameRules()

    def check_exists(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            errors.append("Нет пропуска")

    def check_expired(self, person: Person, errors: List[str]) -> None:
        if person.document is not None and person.document.is_expired(self.rules.current_date):
            errors.append("Срок действия пропуска истёк")

    def check_age(self, person: Person, errors: List[str]) -> None:
        if person.age < self.rules.min_age:
            errors.append("Посетитель младше допустимого возраста")

    def check_name(self, person: Person, errors: List[str]) -> None:
        if person.document is not None and person.document.name != person.name:
            errors.append("Имя в пропуске не совпадает")

    def check_document_age(self, person: Person, errors: List[str]) -> None:
        if person.document is not None and person.document.age != person.age:
            errors.append("Возраст в пропуске не совпадает")

    def check_group(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        group = person.document.group

        if not re.match(self.rules.group_pattern, group):
            errors.append("Неверный формат группы")
            return

        prefix = group.split("-", 1)[0]
        if prefix not in self.rules.valid_group_prefixes:
            errors.append("Группа не относится к институту")

        if group != person.group:
            errors.append("Группа в пропуске не совпадает")

    def check_all(self, person: Person) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        self.check_exists(person, errors)
        if person.document is None:
            return False, errors

        self.check_expired(person, errors)
        self.check_age(person, errors)
        self.check_name(person, errors)
        self.check_document_age(person, errors)
        self.check_group(person, errors)

        return len(errors) == 0, errors

    def get_result(self, person: Person) -> CheckResult:
        allow, errors = self.check_all(person)
        return CheckResult(allow=allow, errors=tuple(errors))


class GameModel:
    def __init__(
        self,
        rules: Optional[GameRules] = None,
        generator: Optional[PersonGenerator] = None,
        checker: Optional[Checker] = None,
        economy: Optional[Economy] = None,
    ):
        self.rules = rules or GameRules()
        self.generator = generator or PersonGenerator(self.rules)
        self.checker = checker or Checker(self.rules)
        self.economy = economy or Economy(
            reward=self.rules.reward_for_correct_decision,
            fine_amount=self.rules.fine_for_mistake,
        )
        self.round_number = 0
        self.current_person: Optional[Person] = None
        self.last_result: Optional[RoundResult] = None
        self.game_over = False
        self.game_over_reason = ""

        self.next_round()

    def next_round(self) -> Optional[Person]:
        if self.game_over:
            return None

        self.round_number += 1
        self.current_person = self.generator.generate()
        return self.current_person

    def decide(self, decision: Union[Decision, str, bool]) -> RoundResult:
        if self.current_person is None:
            raise RuntimeError("Нельзя принять решение: нет текущего посетителя")
        if self.game_over:
            raise RuntimeError("Игра окончена")

        player_decision = self._normalize_decision(decision)
        check_result = self.checker.get_result(self.current_person)
        correct_decision = Decision.ALLOW if check_result.allow else Decision.DENY
        is_correct = player_decision == correct_decision
        money_delta = self.economy.apply_result(is_correct)

        if self.economy.money <= self.rules.prison_balance_limit:
            self.game_over = True
            self.game_over_reason = "Долги слишком большие: чел навсегда попадает в тюрьму к Марвину"

        result = RoundResult(
            player_decision=player_decision,
            correct_decision=correct_decision,
            is_correct=is_correct,
            errors=check_result.errors,
            money_delta=money_delta,
            balance=self.economy.money,
            game_over=self.game_over,
            game_over_reason=self.game_over_reason,
        )
        self.last_result = result

        if not self.game_over:
            self.next_round()

        return result

    def get_instruction(self) -> List[str]:
        return self.rules.instruction_lines()

    def to_save_data(self) -> dict:
        return {
            "money": self.economy.money,
            "round_number": self.round_number,
            "game_over": self.game_over,
            "game_over_reason": self.game_over_reason,
        }

    @staticmethod
    def _normalize_decision(decision: Union[Decision, str, bool]) -> Decision:
        if isinstance(decision, Decision):
            return decision
        if isinstance(decision, bool):
            return Decision.ALLOW if decision else Decision.DENY

        value = decision.strip().lower()
        allow_values = {"allow", "accept", "pass", "пропустить", "допустить"}
        deny_values = {"deny", "reject", "kick", "вышвырнуть", "отказать", "не пропустить"}

        if value in allow_values:
            return Decision.ALLOW
        if value in deny_values:
            return Decision.DENY

        raise ValueError(f"Неизвестное решение игрока: {decision}")
