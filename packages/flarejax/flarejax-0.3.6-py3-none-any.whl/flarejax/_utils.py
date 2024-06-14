import jax
import jax.numpy as jnp


def array_summary(array: jax.Array) -> str:
    dtype = array.dtype.str[1:]
    shape = list(array.shape)

    head = f"{dtype}{shape}"
    body = []

    if jnp.any(jnp.isnan(array)):
        body.append("nan")

    if jnp.any(jnp.isneginf(array)):
        body.append("-inf")

    if jnp.any(jnp.isposinf(array)):
        body.append("+inf")

    # check for constant values
    if len(jnp.unique(array)) == 1:
        body.append(f"const={array.flatten()[0]}")

    if body:
        body = " ".join(body)
        head = f"{head} {body}"

    return head
