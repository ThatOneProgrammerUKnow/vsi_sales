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

#==================================# Client #==================================#
class ClientTable(Base):
    edit = TemplateColumn(
        template_code="""
        <a  
        id="view_contacts_modal"
        type='button'  
        class='btn btn-sm font-medium' 
        href="{% url  'sales:update_client' record.id %}"> 
        Edit</a>
        """,
        verbose_name="Update"
    )
    delete = TemplateColumn(
        template_code="""
        <a  
            type='button'  
            class='text-xl
            hover:bg-gray-200 hover:cursor-pointer rounded p-1' 
            href="{% url  'sales:delete_client' record.id %}"> 
            🗑️</a>
        """,
        verbose_name="Delete"
    )

    class Meta(Base.Meta):
        model = Client
        exclude = ["id", "created_at", "updated_at", "company"]

#==================================# Orders #==================================#
class OrderTable(Base):
    expand = TemplateColumn(
        template_code="""
        <a  
        id="view_contacts_modal"
        type='button'  
        class='btn btn-sm font-medium' 
        href="{% url  'sales:expand_order' record.id %}"> 
        Expand</a>
        """,
        verbose_name="View More"
    )
    id = tables.Column(verbose_name="Order Number")

    class Meta(Base.Meta):
        model = Order
        fields = ["id", "date", "status", "client", "expand"]
    


#==================================# Product #==================================#
class ProductTable(Base):
    price_before_vat = tables.Column(verbose_name="Price before VAT (R)")
    price_after_vat = tables.Column(verbose_name="Price after VAT (R)")
    edit = TemplateColumn(
        template_code="""
        <a  
        id="view_contacts_modal"
        type='button'  
        class='btn btn-sm font-medium' 
        href="{% url  'sales:update_product' record.id %}"> 
        Edit</a>
        """,
        verbose_name="Update"
    )
    delete = TemplateColumn(
        template_code="""
        <a  
            type='button'  
            class='text-xl
            hover:bg-gray-200 hover:cursor-pointer rounded p-1' 
            href="{% url  'sales:delete_product' record.id %}"> 
            🗑️</a>
        """,
        verbose_name="Delete"
    )



    class Meta(Base.Meta):
        model = Product
        exclude = ["created_at", "updated_at", "company"]

#==================================# Invoice #==================================#
class InvoiceTable(Base):
    id = tables.Column()
    date = tables.DateColumn()
    pay_by_date = tables.DateColumn()
    order_id = tables.Column(accessor='order.id', verbose_name="Order ID")
    client = tables.Column(accessor="order.client", verbose_name="Client")


    Preview = TemplateColumn(
        template_code="""
        <a  
        type='button'  
        class='btn btn-sm font-medium' 
        href="{% url  'sales:preview_invoice' record.id %}"> 
        Preview</a>
        """,
        verbose_name="Preview"
    )
    delete = TemplateColumn(
        template_code="""
        <a  
            type='button'  
            class='text-xl
            hover:bg-gray-200 hover:cursor-pointer rounded p-1' 
            href="{% url  'sales:delete_invoice' record.id %}"> 
            🗑️</a>
        """,
        verbose_name="Delete"
    )


    class Meta(Base.Meta):
        model = Invoice
        fields = ('id', 'order_id', 'date', 'pay_by_date', 'client')

    
