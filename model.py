import random
import re
from datetime import date
from enum import Enum
from typing import List, Optional, Tuple, Union

import config


def display_date(value: Optional[date]) -> str:
    if value is None:
        return config.NO_DATE_TEXT

    return value.strftime(config.DATE_FORMAT)


class Decision(Enum):
    ALLOW = config.DECISION_ALLOW
    DENY = config.DECISION_DENY


class GameRules:
    def __init__(
        self,
        max_valid_birth_year: int = config.MAX_VALID_BIRTH_YEAR,
        group_pattern: str = config.GROUP_PATTERN,
        valid_group_prefixes: Tuple[str, ...] = config.VALID_GROUP_PREFIXES,
        valid_education_forms: Tuple[str, ...] = config.EDUCATION_FORMS,
        valid_education_levels: Tuple[str, ...] = config.EDUCATION_LEVELS,
        valid_institutes: Tuple[str, ...] = config.INSTITUTES,
        reward_for_correct_decision: int = config.DEFAULT_REWARD,
        fine_for_mistake: int = config.DEFAULT_FINE,
        dismissal_balance_limit: int = config.DEFAULT_DISMISSAL_BALANCE,
        current_date: Optional[date] = None,
    ):
        self.max_valid_birth_year = max_valid_birth_year
        self.group_pattern = group_pattern
        self.valid_group_prefixes = valid_group_prefixes
        self.valid_education_forms = valid_education_forms
        self.valid_education_levels = valid_education_levels
        self.valid_institutes = valid_institutes
        self.reward_for_correct_decision = reward_for_correct_decision
        self.fine_for_mistake = fine_for_mistake
        self.dismissal_balance_limit = dismissal_balance_limit
        self.current_date = current_date or date.today()

    def instruction_lines(self) -> List[str]:
        prefixes = ", ".join(self.valid_group_prefixes)
        forms = ", ".join(self.valid_education_forms)
        levels = ", ".join(self.valid_education_levels)
        institutes = ", ".join(self.valid_institutes)
        return [
            config.INSTRUCTION_HAS_DOCUMENT,
            config.INSTRUCTION_BIRTH_YEAR.format(max_year=self.max_valid_birth_year),
            config.INSTRUCTION_ISSUE_DATE,
            config.INSTRUCTION_GROUP.format(prefixes=prefixes),
            config.INSTRUCTION_EDUCATION_FORM.format(forms=forms),
            config.INSTRUCTION_EDUCATION_LEVEL.format(levels=levels),
            config.INSTRUCTION_INSTITUTE.format(institutes=institutes),
            config.INSTRUCTION_FULL_NAME,
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
        full_name: str = "",
        group: str = "",
        birth_date: Optional[date] = None,
        education_form: str = "",
        education_level: str = "",
        institute: str = "",
        issue_date: Optional[date] = None,
    ):
        self.full_name = full_name
        self.group = group
        self.birth_date = birth_date
        self.education_form = education_form
        self.education_level = education_level
        self.institute = institute
        self.issue_date = issue_date

    def display_birth_date(self) -> str:
        return display_date(self.birth_date)

    def display_issue_date(self) -> str:
        return display_date(self.issue_date)


class Person:
    def __init__(
        self,
        full_name: str = "",
        group: str = "",
        birth_date: Optional[date] = None,
        document: Optional[Document] = None,
        is_important: bool = False,
    ):
        self.full_name = full_name
        self.group = group
        self.birth_date = birth_date
        self.document = document
        self.is_important = is_important

    def display_data(self) -> List[str]:
        return [
            f"{config.PERSON_FULL_NAME_TEXT}: {self.full_name}",
            f"{config.PERSON_GROUP_TEXT}: {self.group}",
            f"{config.PERSON_BIRTH_DATE_TEXT}: {display_date(self.birth_date)}",
        ]

    def document_data(self) -> List[str]:
        if self.document is None:
            return [config.NO_DOCUMENT_TEXT]

        return [
            f"{config.STUDENT_CARD_TEXT}",
            f"{config.PERSON_FULL_NAME_TEXT}: {self.document.full_name}",
            f"{config.PERSON_GROUP_TEXT}: {self.document.group}",
            f"{config.PERSON_BIRTH_DATE_TEXT}: {self.document.display_birth_date()}",
            f"{config.EDUCATION_FORM_TEXT}: {self.document.education_form}",
            f"{config.EDUCATION_LEVEL_TEXT}: {self.document.education_level}",
            f"{config.INSTITUTE_TEXT}: {self.document.institute}",
            f"{config.ISSUE_DATE_TEXT}: {self.document.display_issue_date()}",
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
        self.invalid_reasons = [
            config.NO_DOCUMENT,
            config.BAD_BIRTH_DATE,
            config.BAD_ISSUE_DATE,
            config.BAD_GROUP_FORMAT,
            config.BAD_GROUP_PREFIX_ERROR,
            config.BAD_EDUCATION_FORM,
            config.BAD_EDUCATION_LEVEL,
            config.BAD_INSTITUTE,
        ]

    def generate(self) -> Person:
        person = self._generate_valid_person()

        should_be_invalid = self.random.random() < config.INVALID_PERSON_CHANCE
        if should_be_invalid:
            self._apply_random_error(person)

        return person

    def _generate_valid_person(self) -> Person:
        full_name = self._generate_full_name()
        group = self._generate_valid_group()
        birth_date = self._generate_valid_birth_date()
        education_form = self.random.choice(self.rules.valid_education_forms)
        education_level = self.random.choice(self.rules.valid_education_levels)
        institute = self.random.choice(self.rules.valid_institutes)
        issue_date = self._generate_valid_issue_date(birth_date)

        return Person(
            full_name=full_name,
            group=group,
            birth_date=birth_date,
            document=Document(
                full_name=full_name,
                group=group,
                birth_date=birth_date,
                education_form=education_form,
                education_level=education_level,
                institute=institute,
                issue_date=issue_date,
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

        if reason == config.BAD_BIRTH_DATE:
            document.birth_date = self._generate_invalid_birth_date()
            document.issue_date = self._generate_valid_issue_date(document.birth_date)
        elif reason == config.BAD_ISSUE_DATE:
            document.issue_date = self._generate_bad_issue_date(document.birth_date)
        elif reason == config.BAD_GROUP_FORMAT:
            document.group = self.random.choice(config.BAD_GROUP_VARIANTS)
        elif reason == config.BAD_GROUP_PREFIX_ERROR:
            group_number = self.random.randint(config.MIN_GROUP_NUMBER, config.MAX_GROUP_NUMBER)
            document.group = f"{config.BAD_GROUP_PREFIX}{config.GROUP_SEPARATOR}{group_number}"
        elif reason == config.BAD_EDUCATION_FORM:
            document.education_form = self.random.choice(config.BAD_EDUCATION_FORMS)
        elif reason == config.BAD_EDUCATION_LEVEL:
            document.education_level = self.random.choice(config.BAD_EDUCATION_LEVELS)
        elif reason == config.BAD_INSTITUTE:
            document.institute = self.random.choice(config.BAD_INSTITUTES)

    def _generate_full_name(self) -> str:
        gender = self.random.choice(config.GENDERS)

        if gender == config.GENDER_FEMALE:
            first_name = self.random.choice(config.FEMALE_NAMES)
            last_name = self.random.choice(config.FEMALE_LAST_NAMES)
            patronymic = self.random.choice(config.FEMALE_PATRONYMICS)
        else:
            first_name = self.random.choice(config.MALE_NAMES)
            last_name = self.random.choice(config.MALE_LAST_NAMES)
            patronymic = self.random.choice(config.MALE_PATRONYMICS)

        return f"{last_name} {first_name} {patronymic}"

    def _generate_valid_birth_date(self) -> date:
        return self._generate_birth_date(
            config.MIN_BIRTH_YEAR,
            self.rules.max_valid_birth_year,
        )

    def _generate_invalid_birth_date(self) -> date:
        return self._generate_birth_date(
            self.rules.max_valid_birth_year + 1,
            config.MAX_BIRTH_YEAR,
        )

    def _generate_birth_date(self, min_year: int, max_year: int) -> date:
        year = self.random.randint(min_year, max_year)
        month = self.random.randint(config.MIN_MONTH, config.MAX_MONTH)
        day = self.random.randint(config.MIN_DAY, config.MAX_SAFE_DAY)

        return date(year, month, day)

    def _generate_valid_issue_date(self, birth_date: date) -> date:
        issue_age = self.random.choice(config.VALID_ISSUE_AGES)
        issue_year = birth_date.year + issue_age

        return date(issue_year, config.ISSUE_DATE_MONTH, config.ISSUE_DATE_DAY)

    def _generate_bad_issue_date(self, birth_date: Optional[date]) -> date:
        if birth_date is None:
            birth_date = self._generate_valid_birth_date()

        issue_age = self.random.choice(config.BAD_ISSUE_AGES)
        issue_year = birth_date.year + issue_age

        return date(issue_year, config.ISSUE_DATE_MONTH, config.ISSUE_DATE_DAY)

    def _generate_valid_group(self) -> str:
        prefix = self.random.choice(self.rules.valid_group_prefixes)
        group_number = self.random.randint(config.MIN_GROUP_NUMBER, config.MAX_GROUP_NUMBER)

        return f"{prefix}{config.GROUP_SEPARATOR}{group_number}"


class Checker:
    def __init__(self, rules: Optional[GameRules] = None):
        self.rules = rules or GameRules()

    def check_exists(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            errors.append(config.ERROR_NO_DOCUMENT)

    def check_birth_date(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        birth_date = person.document.birth_date

        if birth_date is None or birth_date.year > self.rules.max_valid_birth_year:
            errors.append(config.ERROR_BAD_BIRTH_DATE)

    def check_issue_date(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        document = person.document

        if not self.is_issue_date_correct(document.birth_date, document.issue_date):
            errors.append(config.ERROR_BAD_ISSUE_DATE)

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

    def check_education_form(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        if person.document.education_form not in self.rules.valid_education_forms:
            errors.append(config.ERROR_BAD_EDUCATION_FORM)

    def check_education_level(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        if person.document.education_level not in self.rules.valid_education_levels:
            errors.append(config.ERROR_BAD_EDUCATION_LEVEL)

    def check_institute(self, person: Person, errors: List[str]) -> None:
        if person.document is None:
            return

        if person.document.institute not in self.rules.valid_institutes:
            errors.append(config.ERROR_BAD_INSTITUTE)

    def is_issue_date_correct(
        self,
        birth_date: Optional[date],
        issue_date: Optional[date],
    ) -> bool:
        if birth_date is None or issue_date is None:
            return False

        if issue_date.day != config.ISSUE_DATE_DAY:
            return False
        if issue_date.month != config.ISSUE_DATE_MONTH:
            return False

        valid_years = []
        for age in config.VALID_ISSUE_AGES:
            valid_years.append(birth_date.year + age)

        return issue_date.year in valid_years

    def check_all(self, person: Person) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        self.check_exists(person, errors)
        if person.document is None:
            return False, errors

        self.check_birth_date(person, errors)
        self.check_issue_date(person, errors)
        self.check_group(person, errors)
        self.check_education_form(person, errors)
        self.check_education_level(person, errors)
        self.check_institute(person, errors)

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
