"""
An example of sum types in Python using Dataclasses and Union.

A sum type is a type that can be one of multiple different types. This is
written in Python using Union[A,B] or A | B. A type of A | B can be one of A or B.

Sum types can be useful for preventing invalid state. If an object can only
have certain fields on them in certain cases, then a sum type can allow you to
push those fields into subtypes. If one class was used for all variants, it
would be easy to end up with an instance that had an invalid variant.

In the below example, we use emailing as a case where we want to prevent
invalid variants. We have a MailPayload that needs to handle HTML and text
data. HTML and text data have their own fields that must be set properly for
downstream logic to work. We don't want to stuff all of the fields into the
MailPayload object as we could easily forget to set encoding when using a text
payload (or any other invariant).

We use dataclasses to define the different variants and Union to combine them
together. When accessing the body field, we must check which type of body it
is. This is easily done with a match statement.
"""

from dataclasses import dataclass
from collections.abc import Sequence
from typing import assert_never


@dataclass
class TextBody:
    text: str
    encoding: str = "utf-8"


@dataclass
class HTMLBody:
    html: str
    escape: bool = True


@dataclass
class MailPayload:
    to: str
    source: str
    body: HTMLBody | TextBody | Sequence[HTMLBody | TextBody]


body = TextBody("Hello")

payload1 = MailPayload(to="test@example.com", source="another@example.com", body=body)
payload2 = MailPayload(
    to="test@example.com", source="another@example.com", body=[body, HTMLBody("test")]
)

match payload1.body:
    case HTMLBody(html=html):
        print(html)
    case TextBody(text=text):
        print(text)
    case [*elems]:
        print(elems[0])
    case _:
        # We can use type checking to save us if we ever add a new value to the
        # Union but forget to handle it in the match statement. assert_never
        # asserts if the given variable is not of type Never. If we handle all
        # of the cases, the variable is always of type Never.
        assert_never(payload1.body)
