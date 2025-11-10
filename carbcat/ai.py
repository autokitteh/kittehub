"""AI interaction module for food id and carbohydrate calculation using Claude."""

from dataclasses import asdict
from dataclasses import dataclass
import json
from os import getenv
import typing

from anthropic.types.beta import BetaMessageParam

from anthropic import Anthropic
from anthropic import beta_tool
import autokitteh
from autokitteh.anthropic import anthropic_client
from autokitteh.errors import ConnectionInitError
from data import find_foods_by_name
from data import Food
from data import get_food_by_index
from data import Portion


_MODEL = getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

try:
    _client = anthropic_client("anthropic")
except ConnectionInitError:
    # Fallback to basic client if no special config is found, e.g. for local testing.
    _client = Anthropic(api_key=getenv("ANTHROPIC_API_KEY"))

_SYSTEM_PROMPT = """
You are a helpful assistant that determines what food item the user is referring to.
You also need to determine how much, in grams, did the user eat.

The food item and the portion size must match one of the items in the database.
To find the food item, use the `find_foods_by_name` tool. This will return a list of
possible foods, along with known portion sizes. You must use this information to
determine the food item and the number of portions that the user are.

If you cannot determine the food item, or if the food item is not in the database,
respond with a message instructing the user to improve their answer.

If the user specifies more than one food item, consider only the main one, and instruct
them to ask separately for each food item.

Use the `update` tool to update the context with the food item index, portion index,
and amount of portions. NEVER tell the user you're updating the context - this is an
internal detail that the user should not be aware of.

The `food_index` is the field `index` in the foods you receive from the
`find_foods_by_name` tool. The `portion_index` is the index of the portion in the
`portions` list in the relevant food item. The `amount` is the number of portions
consumed.

You MUST use the update tool to set `food_index`, `portion_index`, and `amount` to
non-null values, and set `done` to true, when you have determined the food item
and the amount in portions. You MUST NOT set `done` to true unless all the other
fields are set to non-null values.

So far this is what you gathered: {ctx}
"""


@dataclass(frozen=True, kw_only=True)
class _InteractionContext:
    """Agent interaction context."""

    food_index: int | None
    """Index of the food in the database."""

    portion_index: int | None
    """Index of the portion in the food's portions list."""

    amount: float | None
    """Number of portions consumed."""

    done: bool = False
    """Whether the determination is complete. Set this only if all the other fields are set."""  # noqa: E501

    def adopt(self, other: "_InteractionContext") -> "_InteractionContext":
        """Adopt non-None values from another context."""

        def bora(a, b):
            return b if b is not None else a

        return _InteractionContext(
            food_index=bora(self.food_index, other.food_index),
            portion_index=bora(self.portion_index, other.portion_index),
            amount=bora(self.amount, other.amount),
            done=other.done or self.done,
        )

    @property
    def complete(self) -> bool:
        """Whether the context is complete."""
        return (
            self.food_index is not None
            and self.portion_index is not None
            and self.amount is not None
            and self.done
        )  # noqa: E501


@beta_tool
def _find_foods_by_name_tool(name: str) -> str:
    return json.dumps(
        [
            {"food": asdict(food), "score": score}
            for food, score in find_foods_by_name(name)
        ]
    )


@autokitteh.activity
def interact(
    q0: str | None,
    get_next: typing.Callable[[], str],
    say: typing.Callable[[str], None],
) -> tuple[Food, Portion, float] | None:
    """Determine the food and grams from the history and current context.

    Args:
        q0: initial message from the user.
        get_next: function to get the next message from the user.
        say: function to say something to the user.

    Returns:
        A tuple of (context, history, response).
    """
    ctx = _InteractionContext(food_index=None, portion_index=None, amount=None)

    @beta_tool
    def update_tool(
        food_index: int | None = None,
        portion_index: int | None = None,
        amount: float | None = None,
        done: bool = False,
    ) -> str:
        """Update the determination context with new information.

        Args:
            ctx: The current determination context.
        """
        nonlocal ctx

        ctx1 = _InteractionContext(
            food_index=food_index,
            portion_index=portion_index,
            amount=amount,
            done=done,
        )

        ctx = ctx.adopt(ctx1) if ctx else ctx1

        return f"Context updated: {ctx}"

    q = q0
    history = []

    while not ctx.complete:
        if ctx.done:
            q = "you marked as done, but you did not set all the fields. please fix."

        if not q:
            q = get_next()

        history.append(BetaMessageParam(role="user", content=q.strip()))

        q = None

        runner = _client.beta.messages.tool_runner(
            model=_MODEL,
            max_tokens=1024,
            system=_SYSTEM_PROMPT.format(ctx=ctx),
            messages=history,
            tools=[_find_foods_by_name_tool, update_tool],
        )

        # Collect all messages from the runner
        # The runner handles tool execution internally and yields messages
        final_message = None

        for msg in runner:
            final_message = msg

            for block in msg.content:
                match block.type:
                    case "text":
                        say(block.text)
                    case "tool_use":
                        match block.name:
                            case "_find_foods_by_name_tool":
                                name = typing.cast(dict, block.input).get("name", "")
                                say(
                                    f"(Looking for {name} in the database...)"  # noqa: E501
                                )
                            case _:
                                pass
                    case _:
                        pass

        # Only add the final assistant message to history
        # Don't add intermediate tool_use/tool_result messages
        if final_message:
            history.append(
                BetaMessageParam(role=final_message.role, content=final_message.content)
            )

    if ctx.food_index is None or ctx.portion_index is None or ctx.amount is None:
        return None

    food = get_food_by_index(ctx.food_index)
    return food, food.portions[ctx.portion_index], ctx.amount
