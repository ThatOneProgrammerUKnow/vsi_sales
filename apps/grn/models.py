from django.db import models

from django.db import models
from apps.shared.base_models import BaseModel



# ====================| Customers | ==================== #
class Customer(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.name} {self.branch}'

# ====================| Contact persons | ==================== #
class ContactPerson(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} from {self.Customer.name} {self.cusomer.branch}'

# ====================| GRN Class | ==================== #
class GRN(BaseModel):
    # Created automatically when the grn form is filled in, but also posible to insert another grn_number manually. 
    grn_number = models.CharField(max_length=20, unique=True, primary_key=True)
    date_returned = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f'GRN {self.grn_number} returned on {self.date_returned}'


# ====================| Goods class | ==================== #
class GoodsItem(BaseModel):
# Lists --------------------------------------------------------------------------------------------#

    # I would like to make add dynamic choices in the future. Where the Technician can add sublocations etc. 
    status_options = [
        ('awaiting_request', 'Awaiting Request'),
        ('test_and_report', 'Test & Report'),
        ('awaiting_client', 'Awaiting Client'),
        ('sent_for_repair', 'Sent for repair'),
        ('repairing', 'Repairing'),
        ('awaiting_parts', 'Awaiting parts'),
        ('awaiting_po', 'Awaiting PO'),
        ('out_for_delivery', 'Out for delivery'),
        ('awaiting_collection', 'Awaiting Collection'),
    ]

    location_options = [
        ('grn_section', 'GRN Section'),
        ('test_bay', 'Test Bay'),
        ('technicians_racks', 'Technicians racks'),
        ('dispatch_area', 'Dispatch Area'),
        ('out_for_delivery', 'Out for delivery'),
    ]

    urgency_options = [
        ('not_urgent', 'Not Urgent'),
        ('urgent', 'Urgent'),
    ]
    # The idea is that you can choose one of the most common types of goods, but also be able to add your own, 
    # when there is a unique case that something else is retured.
    type_of_good_options = [
        ('motor', 'motor'),
        ('vsd', 'VSD'),
        ('other', 'Other'),
    ]

    reason_for_return_options = [
        ('credit', 'Credit'),
        ('test_and_report', 'Test & Report'),
        ('return', 'Return'),
    ]

# Attributes --------------------------------------------------------------------------------------------#
    # Identification
    id = models.AutoField(primary_key=True)
    serial_number = models.CharField(max_length=100, db_index = True)
    grn = models.ForeignKey(GRN, on_delete=models.PROTECT, db_index=True)
    model_number = models.CharField(max_length=100)
    type_of_good = models.CharField(max_length=100, choices=type_of_good_options)
    urgency = models.CharField(max_length=50, choices=urgency_options, default="not_urgent")

    # Description 
    status = models.CharField(max_length=50, choices=status_options)
    location = models.CharField(max_length=100, choices=location_options)
    reason_for_return = models.CharField(choices=reason_for_return_options)
    credit_request_reason = models.TextField(blank=True, null=True)

    # Numbers
    job_card_number = models.CharField(max_length=100)
    report_quote_number = models.CharField(max_length=100, blank=True, null=True)
    customer_order_number = models.CharField(max_length=100)
    invoice_credit_number = models.CharField(max_length=100, blank=True, null=True)
    dispatch_note = models.CharField(max_length=100)
    invoice_credit_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Dates
    date_returned = models.DateField()
    credit_passed_date = models.DateField(blank=True, null=True)
    original_invoice_date = models.DateField(blank=True, null=True)

    # Duration (stored as integers, assuming days)
    days_in_warehouse = models.IntegerField(blank=True, null=True)
    days_awaiting_us = models.IntegerField(blank=True, null=True)
    days_awaiting_client = models.IntegerField(blank=True, null=True)

    

    def __str__(self):
        return f"{self.serial_number} - {self.customer.name} ({self.type_of_good})"