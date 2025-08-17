import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED



def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> generate_components(None, 0)
    ...
    """

    gen = tg.MathsGenerator(seed)
    
    ...

    return {
        ...
    }

def solve(*, x, a, b):
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    ...
    >>> answer["maths_object"].simplified()
    ...
    """
    answer = ...
    return {
        "maths_object": answer,
    }


def render_question(*, x, a, b):
    r"""[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    ...
    """

    statement = ...
    
    return {
        "statement": statement,
    }

components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


missive({
    "statement": question["statement"],
    ...
    "answer": answer["maths_object"].latex(),
    "answer_simplified": answer["maths_object"].simplified().latex(),
}
)
# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("Simplified answer:", answer["maths_object"].simplified())
# print("LaTeX representation:", answer["maths_object"].latex())