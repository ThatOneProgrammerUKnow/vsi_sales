import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import Invoice, Client, Product, Order

# Override checkbox header
class CheckBoxCustomColumn(tables.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name
    
# Base table
class Base(tables.Table):
    class Meta:
        attrs = {
            "class": "table text-base table-pin-rows table-pin-cols",
            "thead":{"class":"text-sky-900"},
            "th":{"class":"text-center"},
            "tbody":{"class":"text-sky-800 whitespace-nowrap"},
            "tr":{"class":"h-1"},
            "td":{"class":"text-center"},
        }

#=====# Client #=====#
class ClientTable(Base):
    class Meta(Base.Meta):
        model = Client
        exclude = ["id", "created_at", "updated_at"]

#=====# Orders #=====#
class OrderTable(Base):
    class Meta(Base.Meta):
        model = Order
        exclude = ["company"]
        sequence = ["id"]


#=====# Product #=====#
class ProductTable(Base):
    class Meta(Base.Meta):
        model = Product
        exclude = ["created_at", "updated_at"]

#=====# Invoice #=====#
class InvoiceTable(Base):
    id = tables.Column()
    date = tables.DateColumn()
    pay_by_date = tables.DateColumn()
    order_id = tables.Column(accessor='order.id', verbose_name="Order ID")

    class Meta(Base.Meta):
        model = Invoice
        fields = ('id', 'order_id', 'date', 'pay_by_date')

    
