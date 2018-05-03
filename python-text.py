from base_request import BaseRequest
import frappe


class GenerateCnoteRequest(BaseRequest, object):

    def __init__(self):
        super(GenerateCnoteRequest, self).__init__()
        self.assign_credentials()
        self.olshop_branch = ""
        self.olshop_cust = ""
        self.olshop_orig = ""
        self.olshop_orderid = ""
        self.olshop_shipper_name = ""
        self.olshop_shipper_addr1 = ""
        self.olshop_shipper_addr2 = ""
        self.olshop_shipper_addr3 = ""
        self.olshop_shipper_city = ""
        self.olshop_shipper_region = ""
        self.olshop_shipper_zip = ""
        self.olshop_shipper_phone = ""
        self.olshop_receiver_name = ""
        self.olshop_receiver_addr1 = ""
        self.olshop_receiver_addr2 = ""
        self.olshop_receiver_addr3 = ""
        self.olshop_receiver_city = ""
        self.olshop_receiver_region = ""
        self.olshop_receiver_zip = ""
        self.olshop_receiver_phone = ""
        self.olshop_dest = ""
        self.olshop_service = ""
        self.olshop_qty = ""
        self.olshop_weight = ""
        self.olshop_goodstype = ""
        self.olshop_goodsdesc = ""
        self.olshop_inst = ""
        self.olshop_goodsvalue = ""
        self.olshop_ins_flag = ""
        self.error = False

    def __init__(self, delivery_note):
        super(GenerateCnoteRequest, self).__init__()
        self.error = False
        # frappe.msgprint("brand invoice number: {b}".format(b=delivery_note.brand_invoice_number))
        self.set_olshop_orderid( delivery_note.brand_invoice_number )

        #Get Warehouse From Sales Order
        # frappe.msgprint(delivery_note.name)
        if frappe.db.exists( "Delivery Note Item", { "parent":delivery_note.name }  ):
            delivery_note_items = frappe.get_doc( "Delivery Note Item", { "parent":delivery_note.name }  )
        # frappe.msgprint(delivery_note_items.against_sales_order)
        if frappe.db.exists( "Sales Order Item", {"parent": delivery_note_items.against_sales_order} ):
            sales_order_items = frappe.get_doc( "Sales Order Item", { "parent":delivery_note_items.against_sales_order }  )

        customer = delivery_note.customer
        self.set_olshop_cust("10833200")

        company_name = delivery_note.company
        company = frappe.get_doc("Company", company_name)
        print "company: {0}".format(company)
        self.assign_credentials()
        self.set_olshop_shipper_name(company.company_name)

        # city_mapping_name = company.city_mapping
        # city_mapping = frappe.get_doc("City Mapping", city_mapping_name)
        # print "city_mapping: {0}".format(city_mapping)
        # self.set_olshop_orig("CGK10000")
        self.set_olshop_service(delivery_note.shipping_service)

        #Shipper detail
        warehouse_name = sales_order_items.warehouse
        # frappe.msgprint("warehouse name: {wn}".format(wn=warehouse_name))
        if not frappe.db.exists( "Warehouse", warehouse_name ):
            self.error = True
            frappe.msgprint("Generate CNote - Warehouse " + warehouse_name + " is not found!!")
            return
        else:
            warehouse = frappe.get_doc( "Warehouse", warehouse_name )


        if warehouse is None:
            frappe.msgprint( "Generate CNote - Warehouse " + warehouse_name + " is not found!!" )
            self.error = True
            return

        if warehouse.address_line_1 is None:
            frappe.msgprint( "Generate CNote - Warehouse " + warehouse_name + " address is not complete in line 1" )
            self.error = True
            return

        if warehouse.address_line_2 is None:
            frappe.msgprint( "Generate CNote - Warehouse " + warehouse_name + " address is not complete in line 2" )
            self.error = True
            return

        if warehouse.city is None:
            frappe.msgprint( "Generate CNote - Warehouse " + warehouse_name + " address is not complete in city" )
            self.error = True
            return

        if warehouse.state is None:
            frappe.msgprint( "Generate CNote - Warehouse " + warehouse_name + " address is not complete in state" )
            self.error = True
            return

        if warehouse.postal_code is None:
            frappe.msgprint( "Generate CNote - Warehouse " + warehouse_name + " address is not complete in postal code" )
            self.error = True
            return

        if warehouse.phone_no is None:
            frappe.msgprint( "Generate CNote - Warehouse " + warehouse_name + " address is not complete in phone number" )
            self.error = True
            return


        #Check warehouse complete contact address
        if len(warehouse.address_line_1) == 0 | len(warehouse.address_line_2) == 0 | len(warehouse.city) == 0  | len(warehouse.state) == 0 | len(warehouse.postal_code) == 0  | len(warehouse.phone_no) == 0:
            self.error = True
            frappe.msgprint( "Generate CNote - Empty Warehouse address : " + warehouse )
            return

        self.set_olshop_shipper_addr1( warehouse.address_line_1 )
        self.set_olshop_shipper_addr2( warehouse.address_line_2 )
        self.set_olshop_shipper_city( warehouse.city )
        self.set_olshop_shipper_region( warehouse.state )
        self.set_olshop_shipper_zip( warehouse.postal_code )
        self.set_olshop_shipper_phone( warehouse.phone_no )

        #Warehouse City Mapping as Origin Code
        warehouse_origin_jne_code = "BDO10000"
        warehouse_city_mapping_name = warehouse.city_mapping
        if frappe.db.exists( "City Mapping", warehouse_city_mapping_name ):
            warehouse_city_mapping = frappe.get_doc( "City Mapping", warehouse_city_mapping_name )
            warehouse_origin_jne_code = warehouse_city_mapping.jne_code

        self.set_olshop_orig( warehouse_origin_jne_code )

        #Receiver detail
        address_name = delivery_note.shipping_address_name
        # frappe.msgprint("address name: {an}".format(an=address_name))
        print "address_name: {0}".format(address_name)
        address = frappe.get_doc("Address", address_name)
        # if(address):
        #     frappe.msgprint("address is true")
        # else:
        #     frappe.msgprint("address is false")
        self.set_olshop_receiver_name( customer )
        self.set_olshop_receiver_addr1( address.address_line1 )
        self.set_olshop_receiver_addr2( address.address_line2 )
        self.set_olshop_receiver_city( address.city )
        self.set_olshop_receiver_region( address.county )
        self.set_olshop_receiver_zip( address.pincode )
        self.set_olshop_receiver_phone( address.phone )

        #Destination JNE by City Mapping
        customer_city_mapping_name = address.city_mapping
        frappe.msgprint("city mapping: {cp}".format(cp=customer_city_mapping_name))
        if not frappe.db.exists("City Mapping", customer_city_mapping_name):
            self.error = True
            frappe.msgprint("customer city mapping is none")
            return
        customer_city_mapping = frappe.get_doc("City Mapping", customer_city_mapping_name)
        if customer_city_mapping.jne_code is None:
            self.error = True
            frappe.msgprint("jne code is none")
            return
        self.set_olshop_dest(customer_city_mapping.jne_code)

        #Good's details
        qty = 0
        weight = 0
        desc = ""
        deliver_note_items = delivery_note.items

        for deliver_note_item in deliver_note_items:
            item = frappe.get_doc("Item", {"item_code": deliver_note_item.item_code})
            print "item: {0}".format(item)
            qty += deliver_note_item.qty
            # weight += item.weightage
            desc += str(deliver_note_item.qty) + " " + item.item_name + "\n"

        #Get weight and parse to JNE Format
        #Convert to JNE Regulation
        total_net_weight = delivery_note.total_net_weight
        behind_weight = total_net_weight%1000
        front_weight = total_net_weight - behind_weight;

        front_weight = front_weight/1000

        if behind_weight > 300 :
            behind_weight = 1
        else:
            behind_weight = 0

        weight = front_weight + behind_weight

        if weight == 0:
            weight = 1

        goodsvalue = delivery_note.total
        # frappe.msgprint("olshop_goodsvalue: {o}".format(o=goodsvalue))

        self.set_olshop_qty(qty)
        self.set_olshop_weight(weight)
        self.set_olshop_goodsdesc(desc)
        self.set_olshop_goodsvalue(goodsvalue)

    def set_username(self, username):
        self.username = username
        # frappe.msgprint("usename: {u}".format(u=username))

    def set_api_key(self, api_key):
        self.api_key = api_key
        # frappe.msgprint("api_key: {a}".format(a=api_key))

    def set_olshop_branch(self, olshop_branch):
        self.olshop_branch = olshop_branch
        # frappe.msgprint("olshop_branch: {a}".format(a=olshop_branch))

    def set_olshop_cust(self, olshop_cust):
        self.olshop_cust = olshop_cust
        # frappe.msgprint("olshop_cust: {a}".format(a=olshop_cust))

    def set_olshop_orig(self, olshop_orig):
        self.olshop_orig = olshop_orig
        # frappe.msgprint("olshop_orig: {a}".format(a=olshop_orig))

    def set_olshop_orderid(self, olshop_orderid):
        self.olshop_orderid = olshop_orderid
        # frappe.msgprint("olshop_orderid: {a}".format(a=olshop_orderid))

    def set_olshop_shipper_name(self, olshop_shipper_name):
        self.olshop_shipper_name = olshop_shipper_name
        # frappe.msgprint("olshop_shipper_name: {a}".format(a=olshop_shipper_name))

    def set_olshop_shipper_addr1(self, olshop_shipper_addr1):
        self.olshop_shipper_addr1 = olshop_shipper_addr1
        # frappe.msgprint("olshop_shipper_addr1: {a}".format(a=olshop_shipper_addr1))

    def set_olshop_shipper_addr2(self, olshop_shipper_addr2):
        self.olshop_shipper_addr2 = olshop_shipper_addr2
        # frappe.msgprint("olshop_shipper_addr2: {a}".format(a=olshop_shipper_addr2))

    def set_olshop_shipper_addr3(self, olshop_shipper_addr3):
        self.olshop_shipper_addr3 = olshop_shipper_addr3
        # frappe.msgprint("olshop_shipper_addr3: {a}".format(a=olshop_shipper_addr3))

    def set_olshop_shipper_city(self, olshop_shipper_city):
        self.olshop_shipper_city = olshop_shipper_city
        # frappe.msgprint("olshop_shipper_city: {a}".format(a=olshop_shipper_city))

    def set_olshop_shipper_region(self, olshop_shipper_region):
        self.olshop_shipper_region = olshop_shipper_region
        # frappe.msgprint("olshop_shipper_region: {a}".format(a=olshop_shipper_region))

    def set_olshop_shipper_zip(self, olshop_shipper_zip):
        self.olshop_shipper_zip = olshop_shipper_zip
        # frappe.msgprint("olshop_shipper_zip: {a}".format(a=olshop_shipper_zip))

    def set_olshop_shipper_phone(self, olshop_shipper_phone):
        self.olshop_shipper_phone = olshop_shipper_phone
        # frappe.msgprint("olshop_shipper_phone: {a}".format(a=olshop_shipper_phone))

    def set_olshop_receiver_name(self, olshop_receiver_name):
        self.olshop_receiver_name = olshop_receiver_name
        # frappe.msgprint("olshop_receiver_name: {a}".format(a=olshop_receiver_name))

    def set_olshop_receiver_addr1(self, olshop_receiver_addr1):
        self.olshop_receiver_addr1 = olshop_receiver_addr1
        # frappe.msgprint("olshop_receiver_addr1: {a}".format(a=olshop_receiver_addr1))

    def set_olshop_receiver_addr2(self, olshop_receiver_addr2):
        self.olshop_receiver_addr2 = olshop_receiver_addr2
        # frappe.msgprint("olshop_receiver_addr2: {a}".format(a=olshop_receiver_addr2))

    def set_olshop_receiver_addr3(self, olshop_receiver_addr3):
        self.olshop_receiver_addr3 = olshop_receiver_addr3
        # frappe.msgprint("olshop_receiver_addr3: {a}".format(a=olshop_receiver_addr3))

    def set_olshop_receiver_city(self, olshop_receiver_city):
        self.olshop_receiver_city = olshop_receiver_city
        # frappe.msgprint("olshop_receiver_city: {a}".format(a=olshop_receiver_city))

    def set_olshop_receiver_region(self, olshop_receiver_region):
        self.olshop_receiver_region = olshop_receiver_region
        # frappe.msgprint("olshop_receiver_region: {a}".format(a=olshop_receiver_region))

    def set_olshop_receiver_zip(self, olshop_receiver_zip):
        self.olshop_receiver_zip = olshop_receiver_zip
        # frappe.msgprint("olshop_receiver_zip: {a}".format(a=olshop_receiver_zip))

    def set_olshop_receiver_phone(self, olshop_receiver_phone):
        self.olshop_receiver_phone = olshop_receiver_phone
        # frappe.msgprint("olshop_receiver_phone: {a}".format(a=olshop_receiver_phone))

    def set_olshop_dest(self, olshop_dest):
        self.olshop_dest = olshop_dest
        # frappe.msgprint("olshop_dest: {a}".format(a=olshop_dest))

    def set_olshop_qty(self, olshop_qty):
        self.olshop_qty = olshop_qty
        # frappe.msgprint("olshop_qty: {a}".format(a=olshop_qty))

    def set_olshop_weight(self, olshop_weight):
        self.olshop_weight = olshop_weight
        # frappe.msgprint("olshop_weight: {a}".format(a=olshop_weight))

    def set_olshop_goodsdesc(self, olshop_goodsdesc):
        self.olshop_goodsdesc = olshop_goodsdesc
        # frappe.msgprint("olshop_goodsdesc: {a}".format(a=olshop_goodsdesc))

    def set_olshop_goodsvalue(self, olshop_goodsvalue):
        self.olshop_goodsvalue = olshop_goodsvalue
        # frappe.msgprint("olshop_goodsvalue: {a}".format(a=olshop_goodsvalue))

    def set_olshop_service(self, olshop_service):
        self.olshop_service = olshop_service
        # frappe.msgprint("olshop_service: {a}".format(a=olshop_service))



    def get_cnote_requests(self):
        if self.error:
            # frappe.msgprint("get cnote request error")
            return None
        else:
            # frappe.msgprint("get cnote request is not error")
            return {
                "username": self.username,
                "api_key": self.api_key,
                "OLSHOP_BRANCH": "BDO000",
                "OLSHOP_CUST": self.olshop_cust,
                "OLSHOP_ORIG": self.olshop_orig,
                "OLSHOP_SHIPPER_NAME": self.olshop_shipper_name,
                "OLSHOP_SHIPPER_ADDR1": self.olshop_shipper_addr1,
                "OLSHOP_SHIPPER_ADDR2": self.olshop_shipper_addr2,
                "OLSHOP_SHIPPER_CITY": self.olshop_shipper_city,
                "OLSHOP_SHIPPER_ZIP": self.olshop_shipper_zip,
                "OLSHOP_SHIPPER_PHONE": self.olshop_shipper_phone,
                "OLSHOP_RECEIVER_NAME": self.olshop_receiver_name,
                "OLSHOP_RECEIVER_ADDR1": self.olshop_receiver_addr1,
                "OLSHOP_RECEIVER_ADDR2": self.olshop_receiver_addr2,
                "OLSHOP_RECEIVER_CITY": self.olshop_receiver_city,
                "OLSHOP_RECEIVER_ZIP": self.olshop_receiver_zip,
                "OLSHOP_RECEIVER_PHONE": self.olshop_receiver_phone,
                "OLSHOP_DEST": self.olshop_dest,
                "OLSHOP_SERVICE":  self.olshop_service,
                "OLSHOP_QTY": self.olshop_qty,
                "OLSHOP_WEIGHT": self.olshop_weight,
                "OLSHOP_GOODSTYPE": 2,
                "OLSHOP_GOODSDESC": self.olshop_goodsdesc,
                "OLSHOP_GOODSVALUE": self.olshop_goodsvalue,
                "OLSHOP_INS_FLAG": "N",
                "OLSHOP_ORDERID": self.olshop_orderid
            }

    def assign_credentials(self):
        self.username = "BRODO" #TESTAPI
        self.api_key = "4eee577760a31b59dc5e29fe5a5f4b6f" #25c898a9faea1a100859ecd9ef674548
