def dedupe(ideas: list[str]) -> list[str]:
    return list(dict.fromkeys([i.strip() for i in ideas if i.strip()]))


def extract_numbered_ideas(text: str) -> list[str]:
    lines = text.splitlines()
    return [line for line in lines if line.strip() and line.strip()[0].isdigit()]
