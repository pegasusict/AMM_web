"""Shared helpers for edit pages."""

import reflex as rx

from ..components import breadcrumbs, ro_field


def edit_field(
    label: str,
    value: rx.Var,
    on_change,
    placeholder: str = "",
) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", color="gray"),
        rx.input(value=value, on_change=on_change, placeholder=placeholder),
        spacing="1",
        width="100%",
        align_items="start",
    )


def edit_textarea(
    label: str,
    value: rx.Var,
    on_change,
    placeholder: str = "",
) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", color="gray"),
        rx.text_area(value=value, on_change=on_change, placeholder=placeholder, width="100%"),
        spacing="1",
        width="100%",
        align_items="start",
    )


def edit_header(entity_label: str, detail_href: rx.Var | str) -> rx.Component:
    return breadcrumbs(
        ("Search", "/search"),
        (f"{entity_label} Detail", detail_href),
        ("Edit", ""),
    )


def edit_messages(error: rx.Var, success: rx.Var) -> rx.Component:
    return rx.vstack(
        rx.cond(error, rx.text(error, color="red"), rx.fragment()),
        rx.cond(success, rx.text(success, color="green"), rx.fragment()),
        spacing="2",
        width="100%",
        align_items="start",
    )


def id_field(value: rx.Var) -> rx.Component:
    return ro_field("ID", rx.cond(value, value.to(str), ""))
