__all__ = [
    "_SaleAmendmentLine",
    "SaleAmendment",
    "SaleLineAmendment",
]

import factory
import factory_trytond


class _SaleAmendmentLine(factory_trytond.TrytonFactory):
    class Meta:
        model = "sale.amendment.line"


class SaleAmendment(factory_trytond.TrytonFactory):
    class Meta:
        model = "sale.amendment"

    sale = None

    @factory.post_generation
    def state(obj, create, extracted, **kwargs):
        Model = obj.__class__
        state_transitions = {
            None: tuple(()),
            "draft": tuple(()),
            "validated": (
                Model.validate_amendment,
            ),
        }
        return state_transitions[extracted]

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super()._after_postgeneration(obj, create, results)
        if create and results:
            for button in results["state"]:
                button([obj])


class SaleLineAmendment(SaleAmendment):
    class Params:
        sale_line = None

    sale = factory.SelfAttribute("sale_line.sale")

    line = factory.RelatedFactory(
        _SaleAmendmentLine,
        factory_related_name="amendment",
        action="line",
        line=factory.SelfAttribute(
            "factory_parent.sale_line"),
        product=factory.SelfAttribute(
            "factory_parent.sale_line.product"),
        quantity=factory.SelfAttribute(
            "factory_parent.sale_line.quantity"),
        unit=factory.SelfAttribute(
            "factory_parent.sale_line.unit"),
        unit_price=factory.SelfAttribute(
            "factory_parent.sale_line.unit_price"),
    )
