"""Explainable first-pass claim, evidence, assumption, and objection extraction."""
from __future__ import annotations

import re

from text_intelligence.core.models import Document, JudgmentLevel, MetricObservation, PassageEvidence, Scope

_CLAIM = re.compile(r"\b(we argue|we claim|we propose|we show|we demonstrate|this means|therefore|thus|must|requires|proves|establishes|implies)\b", re.I)
_EVIDENCE = re.compile(r"\b(evidence|data|study|studies|experiment|measured|observed|result|citation|according to|records show|analysis shows|p-value|confidence interval)\b|\[[0-9,\s]+\]|\([A-Z][A-Za-z-]+,\s*\d{4}\)", re.I)
_ASSUMPTION = re.compile(r"\b(assume|assumes|assuming|presupposes|depends on|given that|provided that|if and only if)\b", re.I)
_OBJECTION = re.compile(r"\b(however|objection|one might argue|critics|counterargument|alternatively|on the other hand|yet)\b", re.I)
_RESPONSE = re.compile(r"\b(nevertheless|nonetheless|in response|this objection|but this|the answer is|we reply)\b", re.I)
_HEDGE = re.compile(r"\b(may|might|could|appears|suggests|possibly|likely|perhaps|tentative)\b", re.I)
_ABSOLUTE = re.compile(r"\b(always|never|undeniable|certainly|obviously|impossible|proves)\b", re.I)


def analyze(document: Document) -> list[MetricObservation]:
    sentences = [s for sec in document.sections for p in sec.paragraphs for s in p.sentences]
    claims = [s for s in sentences if _CLAIM.search(s.span.text)]
    evidence = [s for s in sentences if _EVIDENCE.search(s.span.text)]
    assumptions = [s for s in sentences if _ASSUMPTION.search(s.span.text)]
    objections = [s for s in sentences if _OBJECTION.search(s.span.text)]
    responses = [s for s in sentences if _RESPONSE.search(s.span.text)]
    hedged = [s for s in claims if _HEDGE.search(s.span.text)]
    absolute = [s for s in claims if _ABSOLUTE.search(s.span.text)]
    claim_count = len(claims)
    evidence_ratio = len(evidence) / max(claim_count, 1)

    values = [
        ("argument.claim_marker_count", claim_count, "sentences", "Sentences containing explicit claim markers."),
        ("argument.evidence_marker_count", len(evidence), "sentences", "Sentences containing citation, data, study, measurement, or source markers."),
        ("argument.assumption_marker_count", len(assumptions), "sentences", "Sentences explicitly signaling assumptions or dependencies."),
        ("argument.objection_marker_count", len(objections), "sentences", "Sentences signaling contrast, objections, or counterarguments."),
        ("argument.response_marker_count", len(responses), "sentences", "Sentences signaling a reply to an objection."),
        ("argument.evidence_to_claim_ratio", round(evidence_ratio,4), "ratio", "Evidence-marker sentences divided by explicit claim-marker sentences."),
        ("argument.hedged_claim_ratio", round(len(hedged)/max(claim_count,1),4), "ratio", "Explicit claims containing uncertainty or qualification language."),
        ("argument.absolute_claim_ratio", round(len(absolute)/max(claim_count,1),4), "ratio", "Explicit claims containing absolute or certainty language."),
    ]
    out=[MetricObservation(metric_id=i,value=v,unit=u,scope=Scope.DOCUMENT,subject_id=document.id,judgment_level=JudgmentLevel.CALCULATED,method="argument-marker-regex",method_version="0.3.0",interpretation=d,limitations=("Marker detection is a candidate generator; it does not prove that a sentence is a valid claim or that evidence supports it.",)) for i,v,u,d in values]

    if claims and evidence_ratio < 0.5:
        out.append(MetricObservation(metric_id="argument.support_gap_diagnostic",value="high-claim-low-visible-support",scope=Scope.DOCUMENT,subject_id=document.id,judgment_level=JudgmentLevel.HUMAN_REVIEW_REQUIRED,method="claim-evidence-marker-ratio",method_version="0.3.0",confidence=0.68,interpretation="The article contains substantially more explicit claim language than visible evidence language.",revision_action="Attach a source, observation, derivation, example, or boundary statement to the strongest unsupported claims.",evidence=tuple(PassageEvidence(quote=s.span.text,explanation="Explicit claim candidate") for s in claims[:3]),limitations=("Evidence may be expressed without the current lexicon or supplied elsewhere in a series.",)))
    if objections and not responses:
        out.append(MetricObservation(metric_id="argument.unanswered_objection_diagnostic",value="possible-unanswered-objection",scope=Scope.DOCUMENT,subject_id=document.id,judgment_level=JudgmentLevel.HUMAN_REVIEW_REQUIRED,method="objection-response-marker-pairing",method_version="0.3.0",confidence=0.61,interpretation="The text signals an objection or contrast without an obvious response marker.",revision_action="Answer the objection explicitly or state that it remains unresolved.",evidence=tuple(PassageEvidence(quote=s.span.text,explanation="Objection candidate") for s in objections[:2]),limitations=("A response may be implicit or use vocabulary outside the current marker set.",)))
    return out
