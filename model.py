import random
import re
from datetime import date, timedelta
from enum import Enum
from typing import List, Optional, Tuple, Union

import config


class Decision(Enum):
    ALLOW = config.DECISION_ALLOW
    DENY = config.DECISION_DENY


class GameRules:
    def __init__(
        self,
        min_age: int = config.DEFAULT_MIN_AGE,
        group_pattern: str = config.GROUP_PATTERN,
        valid_group_prefixes: Tuple[str, ...] = config.VALID_GROUP_PREFIXES,
        reward_for_correct_decision: int = config.DEFAULT_REWARD,
        fine_for_mistake: int = config.DEFAULT_FINE,
        dismissal_balance_limit: int = config.DEFAULT_DISMISSAL_BALANCE,
        current_date: Optional[date] = None,
    ):
        self.min_age = min_age
        self.group_pattern = group_pattern
        self.valid_group_prefixes = valid_group_prefixes
        self.reward_for_correct_decision = reward_for_correct_decision
        self.fine_for_mistake = fine_for_mistake
        self.dismissal_balance_limit = dismissal_balance_limit
        self.current_date = current_date or date.today()

    def instruction_lines(self) -> List[str]:
        prefixes = ", ".join(self.valid_group_prefixes)
        return [
            config.INSTRUCTION_HAS_DOCUMENT,
            config.INSTRUCTION_NOT_EXPIRED,
            config.INSTRUCTION_MIN_AGE.format(min_age=self.min_age),
            config.INSTRUCTION_GROUP.format(prefixes=prefixes),
            config.INSTRUCTION_DATA_MATCH,
        ]


class Economy:
    def __init__(
        self,
        money: int = config.DEFAULT_MONEY,
        reward: int = config.DEFAULT_REWARD,
        fine_amount: int = config.DEFAULT_FINE,
    ):
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
        age: int = config.DEFAULT_AGE,
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
            return config.NO_DATE_TEXT
        return self.valid_until.strftime(config.DATE_FORMAT)


class Person:
    def __init__(
        self,
        name: str = "",
        age: int = config.DEFAULT_AGE,
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
            f"{config.PERSON_NAME_TEXT}: {self.name}",
            f"{config.PERSON_AGE_TEXT}: {self.age}",
            f"{config.PERSON_GROUP_TEXT}: {self.group}",
        ]

    def document_data(self) -> List[str]:
        if self.document is None:
            return [config.NO_DOCUMENT_TEXT]

        return [
            f"{config.PERSON_NAME_TEXT}: {self.document.name}",
            f"{config.PERSON_AGE_TEXT}: {self.document.age}",
            f"{config.PERSON_GROUP_TEXT}: {self.document.group}",
            f"{config.DOCUMENT_VALID_UNTIL_TEXT}: {self.document.display_valid_until()}",
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
        self.names = config.PERSON_NAMES
        self.invalid_reasons = [
            config.NO_DOCUMENT,
            config.EXPIRED_DOCUMENT,
            config.TOO_YOUNG,
            config.BAD_GROUP_FORMAT,
            config.BAD_GROUP_PREFIX_ERROR,
            config.WRONG_NAME,
            config.WRONG_AGE,
            config.WRONG_GROUP,
        ]

    def generate(self) -> Person:
        person = self._generate_valid_person()

        should_be_invalid = self.random.random() < config.INVALID_PERSON_CHANCE
        if should_be_invalid:
            self._apply_random_error(person)

        return person

    def _generate_valid_person(self) -> Person:
        name = self.random.choice(self.names)
        age = self.random.randint(self.rules.min_age, config.DEFAULT_MAX_AGE)
        group = self._generate_valid_group()
        valid_days = self.random.randint(config.MIN_PASS_DAYS, config.MAX_PASS_DAYS)
        valid_until = self.rules.current_date + timedelta(days=valid_days)

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

        if reason == config.NO_DOCUMENT:
            person.document = None
            return

        document = person.document
        if document is None:
            return

        if reason == config.EXPIRED_DOCUMENT:
            expired_days = self.random.randint(config.MIN_PASS_DAYS, config.MAX_EXPIRED_DAYS)
            document.valid_until = self.rules.current_date - timedelta(days=expired_days)
        elif reason == config.TOO_YOUNG:
            person.age = self.random.randint(config.MIN_TOO_YOUNG_AGE, self.rules.min_age - 1)
            document.age = person.age
        elif reason == config.BAD_GROUP_FORMAT:
            document.group = self.random.choice(config.BAD_GROUP_VARIANTS)
        elif reason == config.BAD_GROUP_PREFIX_ERROR:
            group_number = self.random.randint(config.MIN_GROUP_NUMBER, config.MAX_GROUP_NUMBER)
            document.group = f"{config.BAD_GROUP_PREFIX}{config.GROUP_SEPARATOR}{group_number}"
        elif reason == config.WRONG_NAME:
            possible_names = [name for name in self.names if name != person.name]
            document.name = self.random.choice(possible_names)
        elif reason == config.WRONG_AGE:
            document.age = person.age + self.random.choice(config.AGE_MISTAKE_VARIANTS)
        elif reason == config.WRONG_GROUP:
            document.group = self._generate_valid_group(exclude=person.group)

    def _generate_valid_group(self, exclude: Optional[str] = None) -> str:
        while True:
            prefix = self.random.choice(self.rules.valid_group_prefixes)
            group_number = self.random.randint(config.MIN_GROUP_NUMBER, config.MAX_GROUP_NUMBER)
            group = f"{prefix}{config.GROUP_SEPARATOR}{group_number}"
            if group != exclude:
                return group


class Checker:
    def __init__(self, rules: Optional[GameRules] = None):
        self.rules = rules or GameRules()

    def check_exists(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            errors.append(config.ERROR_NO_DOCUMENT)

    def check_expired(self, person: Person, errors: List[str]) -> None:
        if person.document is not None:
            if person.document.is_expired(self.rules.current_date):
                errors.append(config.ERROR_EXPIRED_DOCUMENT)

    def check_age(self, person: Person, errors: List[str]) -> None:
        if person.age < self.rules.min_age:
            errors.append(config.ERROR_TOO_YOUNG)

    def check_name(self, person: Person, errors: List[str]) -> None:
        if person.document is not None and person.document.name != person.name:
            errors.append(config.ERROR_WRONG_NAME)

    def check_document_age(self, person: Person, errors: List[str]) -> None:
        if person.document is not None and person.document.age != person.age:
            errors.append(config.ERROR_WRONG_AGE)

    def check_group(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        group = person.document.group

        if not re.match(self.rules.group_pattern, group):
            errors.append(config.ERROR_BAD_GROUP_FORMAT)
            return

        prefix = group.split(config.GROUP_SEPARATOR, config.GROUP_SPLIT_MAX_COUNT)[0]
        if prefix not in self.rules.valid_group_prefixes:
            errors.append(config.ERROR_BAD_GROUP_PREFIX)

        if group != person.group:
            errors.append(config.ERROR_WRONG_GROUP)

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
            raise RuntimeError(config.MESSAGE_NO_CURRENT_PERSON)
        if self.game_over:
            raise RuntimeError(config.MESSAGE_GAME_ALREADY_OVER)

        player_decision = self._normalize_decision(decision)
        check_result = self.checker.get_result(self.current_person)
        correct_decision = Decision.ALLOW if check_result.allow else Decision.DENY
        is_correct = player_decision == correct_decision
        money_delta = self.economy.apply_result(is_correct)

        if self.economy.money <= self.rules.dismissal_balance_limit:
            self.game_over = True
            self.game_over_reason = config.MESSAGE_DISMISSED

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

        if value in config.ALLOW_DECISIONS:
            return Decision.ALLOW
        if value in config.DENY_DECISIONS:
            return Decision.DENY

        raise ValueError(config.MESSAGE_UNKNOWN_DECISION.format(decision=decision))
