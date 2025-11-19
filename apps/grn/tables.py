import django_tables2 as tables
from django_tables2 import TemplateColumn
from django.conf import settings
from .models import GRN, Customer, GoodsItem

# Override checkbox header
class CheckBoxCustomColumn(tables.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name

class GRNTable(tables.Table):
    select = CheckBoxCustomColumn(
        verbose_name="Select",
        accessor="pk"
        )

    contact = TemplateColumn(
        template_code="{{ record.contact_person.name }} {{ record.contact_person.surname }}",
        verbose_name="Contact Person"
    )

    customer = TemplateColumn(template_code=
    "{{ record.contact_person.customer.name }} " \
    "{% if record.contact_person.customer.branch %}{{ record.contact_person.customer.branch }}{% endif %}" \
    "{% if record.contact_person.customer.farm %}{{ record.contact_person.customer.farm }}{% endif %}",
      verbose_name="Customer")


    goods = TemplateColumn(
        template_code="{{ record.goods_item.count }}",
        verbose_name="Goods"
        )

    class Meta:
        model = GRN
        exclude = ("id", "updated_at", "created_at", "contact_person")

        attrs = {
            "class": "table text-base table-pin-rows table-pin-cols",
            "thead":{"class":"text-sky-900"},
            "th":{"class":"text-center"},
            "tbody":{"class":"text-sky-800 whitespace-nowrap"},
            "tr":{"class":"h-1"},
            "td":{"class":"text-center"},
        }
        sequence = ("select", "grn_number", "date_returned", "contact", "customer", "goods") 

#--->>> Customer table 
class CustomerTable(tables.Table):
    expand = TemplateColumn(
        template_code="""
        <a  
        id="view_contacts_modal"
        type='button'  
        class='btn btn-sm font-medium' 
        href="{% url  'grn:contact_persons' record.pk %}"> 
        View more</a>
        """,
        verbose_name="Actions"
    )
    class Meta:
        model = Customer

        exclude = ("id", "updated_at", "created_at")

        attrs = {
            "class": "table text-base table-pin-rows table-pin-cols",
            "thead":{"class":"text-sky-900"},
            "th":{"class":"text-center"},
            "tbody":{"class":"text-sky-800 whitespace-nowrap"},
            "tr":{"class":"h-1"},
            "td":{"class":"text-center"},
        }


class GoodsItemTable(tables.Table):
    grn_number = tables.Column(accessor="grn__grn_number")
    customer_name = tables.Column(accessor="grn__customer__name")


    class Meta:
        model = GoodsItem
        exclude = ("id", "updated_at", "credit_request_reason")
