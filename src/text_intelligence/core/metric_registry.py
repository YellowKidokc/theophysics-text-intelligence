"""Metric definitions and registration.

A metric cannot ship merely because code can calculate it. It must declare what
it measures, what it does not establish, its scope, and its provenance.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from text_intelligence.core.models import JudgmentLevel, MetricObservation, Scope

MetricFunction = Callable[[Any], Iterable[MetricObservation]]


@dataclass(frozen=True, slots=True)
class MetricDefinition:
    metric_id: str
    name: str
    family: str
    description: str
    scope: Scope
    judgment_level: JudgmentLevel
    unit: str = ""
    higher_is: str = "contextual"
    minimum_words: int = 0
    method: str = ""
    method_version: str = ""
    establishes: tuple[str, ...] = ()
    does_not_establish: tuple[str, ...] = ()
    references: tuple[str, ...] = ()


class MetricRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, MetricDefinition] = {}
        self._functions: dict[str, MetricFunction] = {}

    def register(self, definition: MetricDefinition, function: MetricFunction) -> None:
        if definition.metric_id in self._definitions:
            raise ValueError(f"Duplicate metric_id: {definition.metric_id}")
        self._definitions[definition.metric_id] = definition
        self._functions[definition.metric_id] = function

    def definition(self, metric_id: str) -> MetricDefinition:
        try:
            return self._definitions[metric_id]
        except KeyError as exc:
            raise KeyError(f"Unknown metric_id: {metric_id}") from exc

    def definitions(self, family: str | None = None) -> tuple[MetricDefinition, ...]:
        values = self._definitions.values()
        if family is not None:
            values = (item for item in values if item.family == family)
        return tuple(sorted(values, key=lambda item: item.metric_id))

    def run(self, metric_id: str, subject: Any) -> tuple[MetricObservation, ...]:
        definition = self.definition(metric_id)
        observations = tuple(self._functions[metric_id](subject))
        for observation in observations:
            if observation.metric_id != definition.metric_id:
                raise ValueError(
                    f"Metric function for {metric_id} returned {observation.metric_id}"
                )
        return observations

    def run_family(self, family: str, subject: Any) -> tuple[MetricObservation, ...]:
        output: list[MetricObservation] = []
        for definition in self.definitions(family=family):
            output.extend(self.run(definition.metric_id, subject))
        return tuple(output)

    def audit(self) -> list[str]:
        problems: list[str] = []
        for item in self.definitions():
            if not item.description.strip():
                problems.append(f"{item.metric_id}: missing description")
            if not item.method.strip():
                problems.append(f"{item.metric_id}: missing method")
            if not item.does_not_establish:
                problems.append(f"{item.metric_id}: missing boundary statement")
        return problems


registry = MetricRegistry()
