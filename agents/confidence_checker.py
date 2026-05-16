import re

def confidence_checker(state: dict) -> dict:
    print(">> Confidence Checker running...")

    root_cause = state.get("root_cause", "")
    loop_count = state.get("loop_count", 0)

    confidence_match = re.search(r'CONFIDENCE:\s*(\d+)/100', root_cause)
    confidence = int(confidence_match.group(1)) if confidence_match else 0

    state["confidence_score"] = confidence
    state["loop_count"] = loop_count + 1

    if confidence >= 90:
        state["needs_reanalysis"] = False
        state["needs_human_input"] = False
        print(f">> Confidence {confidence}/100 — proceeding to fix agent")
    elif loop_count >= 2 and confidence < 85:
        state["needs_reanalysis"] = False
        state["needs_human_input"] = True
        print(f">> Confidence {confidence}/100 after {loop_count} loops — requesting human input")
    elif loop_count >= 2:
        state["needs_reanalysis"] = False
        state["needs_human_input"] = False
        print(f">> Max loops reached — proceeding with best result")
    else:
        state["needs_reanalysis"] = True
        state["needs_human_input"] = False
        print(f">> Confidence {confidence}/100 too low — looping back")

    return state