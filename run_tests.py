import asyncio
import sys

from rag import RAGResponse, get_rag_response

TESTS = [
    {
        "name": "Pregunta CON respuesta en los documentos",
        "query": "Tengo 5 años de antigüedad, ¿cuántos días hábiles de vacaciones me corresponden?",
        "expect_answer": True,
        "must_contain": "20",
    },
    {
        "name": "Pregunta TRAMPA (tema de la empresa, pero ausente)",
        "query": "¿Cuál es el sueldo del gerente general de NovaTech?",
        "expect_answer": False,
        "must_contain": None,
    },
    {
        "name": "Pregunta TRAMPA extra (fuera de dominio)",
        "query": "¿Cuál es la capital de Francia?",
        "expect_answer": False,
        "must_contain": None,
    },
]


def check(test: dict, resp: RAGResponse) -> bool:
    if resp.has_answer != test["expect_answer"]:
        return False
    if test["expect_answer"]:
        return bool(resp.references) and test["must_contain"] in resp.answer
    return resp.answer.startswith("No lo sé") and not resp.references


async def main() -> int:
    failures = 0
    for t in TESTS:
        resp = await get_rag_response(t["query"])
        ok = check(t, resp)
        failures += not ok
        print(f"\n{'✅' if ok else '❌'} {t['name']}")
        print(f"   Pregunta   : {t['query']}")
        print(f"   Respuesta  : {resp.answer}")
        print(f"   has_answer : {resp.has_answer}")
        print(f"   Referencias: {resp.references}")
    print(f"\nResultado: {len(TESTS) - failures}/{len(TESTS)} pruebas OK")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
