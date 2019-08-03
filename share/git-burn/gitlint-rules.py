import re

from gitlint.rules import (
    LineRule,
    CommitRule,
    CommitMessageTitle,
    ListOption,
    RuleViolation,
)


class TitleCapitalized(LineRule):
    name = "title-capitalized"
    id = "UT1"
    target = CommitMessageTitle
    violation_message = "Title should start with a capital letter"

    def validate(self, line, _commit):
        if line == "":
            return
        if not line[0].isupper():
            return [RuleViolation(self.id, self.violation_message, line)]


class TitleImperativeMood(LineRule):
    name = "title-imperative-mood"
    id = "UT2"
    target = CommitMessageTitle
    violation_message = "Title should use imperative mood"
    options_spec = [ListOption("suffixes", ["ed", "ing"], "Comma separated \
list of suffixes that should not be found in the first word")]

    def validate(self, line, _commit):
        if line == "":
            return
        first_word = line.split()[0]
        for suffix in self.options['suffixes'].value:
            if first_word.endswith(suffix):
                return [RuleViolation(self.id, self.violation_message, line)]


class TitleNoIssueReferences(LineRule):
    name = "title-no-issue-references"
    id = "UT3"
    target = CommitMessageTitle
    violation_message = "Title should not contain issue references; \
use last body paragraph"

    def validate(self, line, _commit):
        if re.search(r"#\d+", line):
            return [RuleViolation(self.id, self.violation_message, line)]


class BodySeparateReferences(CommitRule):
    name = "body-separate-references"
    id = "UT4"
    violation_message = "'See/Fixes/Closes' issue reference should be placed \
in separate paragraph"

    def validate(self, commit):
        paragraphs = "\n".join(commit.message.body[1:]).split("\n\n")
        for para in paragraphs:
            if re.search(r".+(See|Fixes|Closes) #\d+", para, re.I | re.S):
                return [RuleViolation(self.id, self.violation_message)]


class MergeContainReference(CommitRule):
    name = "merge-contain-reference"
    id = "UT5"
    violation_message = "Merge commit should contain issue reference"

    def validate(self, commit):
        if not commit.is_merge_commit:
            return
        if re.search(r"(See|Fixes|Closes) #\d+", commit.message.full):
            return
        return [RuleViolation(self.id, self.violation_message)]
