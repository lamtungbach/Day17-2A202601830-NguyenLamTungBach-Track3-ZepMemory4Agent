from __future__ import annotations

import json
import re
from typing import Any

from .config import settings
from .context_budget import ContextBudgetManager
from .utils import cap_query
from .zep_common import prime_eval_thread, render_graph_search


class StudentMemory:
    """Only this file needs to be edited by students."""

    def __init__(self, client: Any):
        self.client = client
        self.budget = ContextBudgetManager(settings.context_tokens)

    # NOTE: Zep rejects graph.search queries longer than 400 characters. Some
    # eval queries are longer than that, so wrap every query with
    # `cap_query(query)` (see src/utils.py) before passing it to graph.search.

    def retrieve_long_term(self, user_id: str, thread_id: str, query: str) -> str:
        # LAB TODO 1/4
        # 1) prime_eval_thread(...) has already been provided as scaffolding.
        # 2) call thread.get_user_context(thread_id=...)
        # 3) return the .context string.
        # Bonus: append graph.search(scope="edges", limit>=20) facts with
        #        validity ranges (a low limit can miss deadline/open-loop facts).
        prime_eval_thread(self.client, user_id, thread_id, query)
        context_block = self.client.thread.get_user_context(thread_id=thread_id)
        context = getattr(context_block, "context", "") or ""

        # Context Block is the primary long-term representation. User-scoped
        # edges add explicit validity/provenance and make open loops or recent
        # project overrides visible without ever crossing user namespaces.
        try:
            facts = self.client.graph.search(
                user_id=user_id,
                query=cap_query(query),
                scope="edges",
                limit=20,
            )
            rendered_facts = render_graph_search(facts)
        except Exception:
            rendered_facts = ""

        return "\n".join(part for part in (context, rendered_facts) if part.strip())

    def retrieve_episodic(self, user_id: str, query: str) -> str:
        # LAB TODO 2/4
        # Use client.graph.search(user_id=..., query=cap_query(query),
        #     scope="episodes", limit=...) then render_graph_search(...).
        # Tip: verbose session episodes can crowd out concise, marker-bearing
        # reflections under the tight episodic budget — render_graph_search
        # accepts an `episode_char_cap` to keep more distinct episodes.
        results = self.client.graph.search(
            user_id=user_id,
            query=cap_query(query),
            scope="episodes",
            limit=20,
        )
        rendered = render_graph_search(results, episode_char_cap=600)

        # Evaluation/follow-up threads are also episodes and can crowd an older
        # outcome out of the first 3% context budget. Re-rank the returned set
        # locally: durable marker-bearing source episodes first, then lexical
        # overlap with the query, while preserving Zep rank as the tie-breaker.
        query_terms = set(re.findall(r"[a-z0-9-]{4,}", query.casefold()))
        ranked: list[tuple[tuple[int, int, int], str]] = []
        seen: set[str] = set()
        for index, episode in enumerate(getattr(results, "episodes", None) or []):
            content = str(getattr(episode, "content", "") or "").strip()
            if not content or content.casefold() in seen:
                continue
            seen.add(content.casefold())
            markers = re.findall(r"\b[A-Z][A-Z0-9-]{5,}\b", content)
            lowered = content.casefold()
            overlap = sum(term in lowered for term in query_terms)
            ranked.append(((1 if markers else 0, overlap, -index), content[:600]))

        ranked.sort(key=lambda item: item[0], reverse=True)
        compact_render = "\n".join(
            f"EPISODE: {content}" for _, content in ranked
        )
        return "\n".join(
            part for part in (compact_render, rendered) if part.strip()
        )

    def retrieve_semantic(self, graph_id: str, query: str) -> str:
        # LAB TODO 3/4
        # Search the standalone graph (graph_id, NOT user_id).
        # Recommended: scope="episodes" — it returns raw document text that keeps
        # literal markers (e.g. PAYMENT-RULE-3). The "auto" scope returns
        # extracted facts that DROP those literal codes, so avoid it here.
        # Fallback: scope="nodes".
        bounded_query = cap_query(query)
        try:
            results = self.client.graph.search(
                graph_id=graph_id,
                query=bounded_query,
                scope="episodes",
                limit=8,
            )
            rendered = render_graph_search(results)
            if rendered.strip():
                # Semantic documents are ingested as both JSON and summary
                # text. Zep can return both copies, which wastes the tight 3%
                # semantic budget and may trim a later relevant document. Put
                # one compact, marker-bearing summary per document first, then
                # keep the normal renderer for metadata/provenance.
                compact_by_marker: dict[str, str] = {}
                for episode in getattr(results, "episodes", None) or []:
                    raw = str(getattr(episode, "content", "") or "").strip()
                    if not raw:
                        continue
                    compact = raw
                    try:
                        payload = json.loads(raw)
                        if isinstance(payload, dict) and payload.get("summary"):
                            compact = str(payload["summary"]).strip()
                    except (TypeError, ValueError, json.JSONDecodeError):
                        pass

                    markers = re.findall(r"\b[A-Z][A-Z0-9-]{5,}\b", compact)
                    key = "|".join(markers) if markers else compact.casefold()
                    current = compact_by_marker.get(key)
                    if current is None or len(compact) < len(current):
                        compact_by_marker[key] = compact

                compact_render = "\n".join(
                    f"EPISODE: {content}" for content in compact_by_marker.values()
                )
                return "\n".join(
                    part for part in (compact_render, rendered) if part.strip()
                )
        except Exception:
            pass

        fallback = self.client.graph.search(
            graph_id=graph_id,
            query=bounded_query,
            scope="nodes",
            limit=8,
        )
        return render_graph_search(fallback)

    def assemble_context(self, layers: dict[str, str]) -> tuple[str, dict[str, dict[str, int]]]:
        # LAB TODO 4/4
        # Use ContextBudgetManager to enforce 10/4/3/3 budget and priority order.
        return self.budget.assemble(layers)
