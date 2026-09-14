def prune_context(entries: list[dict], current_task_files: set[str], max_entries: int = 20) -> tuple[list[dict], list[dict]]:
    kept = [e for e in entries if e["file_path"] in current_task_files]
    remaining_slots = max(0, max_entries - len(kept))

    rest = [e for e in entries if e["file_path"] not in current_task_files]
    rest_sorted = sorted(rest, key=lambda e: e["score"], reverse=True)

    kept_rest = rest_sorted[:remaining_slots]
    dropped = rest_sorted[remaining_slots:]

    return kept + kept_rest, dropped
