from django import template

from mizdb_inlines.renderers import InlineFormsetRenderer, TabularInlineFormsetRenderer

register = template.Library()


@register.simple_tag
def inline_formset(formset, **kwargs):
    return InlineFormsetRenderer(formset, **kwargs).render()


@register.inclusion_tag("mizdb_inlines/tabular_inline_formset.html")
def tabular_inline_formset(formset, **kwargs):
    return {"formset": formset, "rendered_formset": TabularInlineFormsetRenderer(formset, **kwargs).render()}
