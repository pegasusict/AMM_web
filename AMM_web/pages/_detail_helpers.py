"""Shared helpers for detail pages."""

import reflex as rx

from ..components import breadcrumbs, ro_field


FieldDef = tuple[str, rx.Var, str]


def field(label: str, value: rx.Var, fallback: str = "") -> FieldDef:
    return (label, value, fallback)


def fields_block(fields: list[FieldDef]) -> rx.Component:
    return rx.vstack(
        *[
            ro_field(label, rx.cond(value, value.to(str), fallback))
            for label, value, fallback in fields
        ],
        spacing="2",
        width="100%",
    )


def detail_content(
    entity_label: str,
    entity: rx.Var,
    fields: list[FieldDef],
    edit_href: rx.Var | str | None = None,
) -> rx.Component:
    return rx.vstack(
        breadcrumbs(
            ("Search", "/search"),
            (entity_label, ""),
        ),
        rx.cond(
            entity,
            fields_block(fields),
            rx.text("Loading...", color="gray"),
        ),
        rx.hstack(
            rx.button(
                "Back",
                on_click=rx.redirect("/search"),
                variant="outline",
            ),
            *(
                [
                    rx.button(
                        "Edit",
                        on_click=rx.redirect(edit_href),
                    )
                ]
                if edit_href is not None
                else []
            ),
        ),
        spacing="4",
    )
