import uuid

class Vendor:
    """Represents a vendor in the global address book."""
    def __init__(self, name, contact_person, address, is_approved=False):
        self.vendor_id = str(uuid.uuid4())[:8] # Unique ID for the vendor
        self.name = name
        self.contact_person = contact_person
        self.address = address
        self.is_approved = is_approved # Central approval status

    def __str__(self):
        status = "Approved" if self.is_approved else "Pending Approval"
        return f"Vendor ID: {self.vendor_id}, Name: {self.name}, Contact: {self.contact_person}, Status: {status}"

class GlobalVendorRegistry:
    """A centralized repository for all vendor information (Global Address Book concept)."""
    def __init__(self):
        self.vendors = {}

    def add_vendor(self, vendor):
        # Centralized addition of a new vendor
        if vendor.vendor_id in self.vendors:
            print(f"Warning: Vendor with ID {vendor.vendor_id} already exists.")
            return False
        self.vendors[vendor.vendor_id] = vendor
        print(f"Added vendor: {vendor.name} (ID: {vendor.vendor_id})")
        return True

    def get_vendor(self, vendor_id):
        # Centralized retrieval of vendor details
        return self.vendors.get(vendor_id)

    def approve_vendor(self, vendor_id):
        # Centralized approval process for a vendor
        vendor = self.get_vendor(vendor_id)
        if vendor and not vendor.is_approved:
            vendor.is_approved = True
            print(f"Vendor {vendor.name} (ID: {vendor_id}) has been centrally approved.")
            return True
        elif vendor and vendor.is_approved:
            print(f"Vendor {vendor.name} (ID: {vendor_id}) is already approved.")
        else:
            print(f"Vendor with ID {vendor_id} not found for approval.")
        return False

    def list_vendors(self):
        print("\n--- Current Vendors in Global Registry ---")
        if not self.vendors:
            print("No vendors registered.")
            return
        for vendor in self.vendors.values():
            print(vendor)
        print("------------------------------------------")

class PurchaseRequest:
    """Represents a purchase request from a department."""
    def __init__(self, department, item, quantity, preferred_vendor_id=None):
        self.request_id = str(uuid.uuid4())[:8]
        self.department = department
        self.item = item
        self.quantity = quantity
        self.preferred_vendor_id = preferred_vendor_id
        self.status = "Pending"

    def __str__(self):
        vendor_info = f", Preferred Vendor ID: {self.preferred_vendor_id}" if self.preferred_vendor_id else ""
        return f"Request ID: {self.request_id}, Dept: {self.department}, Item: {self.item} (x{self.quantity}){vendor_info}, Status: {self.status}"

class CentralProcurementSystem:
    """Manages and processes purchase requests using the centralized vendor registry."""
    def __init__(self, vendor_registry):
        self.vendor_registry = vendor_registry
        self.purchase_requests = []

    def submit_request(self, department, item, quantity, preferred_vendor_id=None):
        # Departments submit requests to the central system
        request = PurchaseRequest(department, item, quantity, preferred_vendor_id)
        self.purchase_requests.append(request)
        print(f"\n{department} submitted a request: {request.item} (x{request.quantity})")
        return request

    def process_all_requests(self):
        print("\n--- Processing All Pending Purchase Requests ---")
        for request in self.purchase_requests:
            if request.status == "Pending":
                print(f"Processing Request ID: {request.request_id} for {request.item}...")
                vendor = None
                if request.preferred_vendor_id:
                    vendor = self.vendor_registry.get_vendor(request.preferred_vendor_id)

                # Centralized validation of vendor and approval status
                if vendor and vendor.is_approved:
                    request.status = "Approved"
                    print(f"  -> APPROVED. Using approved vendor: {vendor.name}.")
                elif vendor and not vendor.is_approved:
                    request.status = "Rejected - Vendor Not Approved"
                    print(f"  -> REJECTED. Preferred vendor {vendor.name} (ID: {vendor.vendor_id}) is not centrally approved.")
                else:
                    request.status = "Rejected - Vendor Not Found or Invalid"
                    print(f"  -> REJECTED. Preferred vendor ID {request.preferred_vendor_id} not found or invalid.")
            else:
                print(f"Request ID: {request.request_id} already {request.status}.")
        print("------------------------------------------------")

    def list_requests(self):
        print("\n--- All Purchase Requests ---")
        if not self.purchase_requests:
            print("No purchase requests submitted.")
            return
        for req in self.purchase_requests:
            print(req)
        print("-----------------------------")

if __name__ == "__main__":
    # 1. Initialize the Global Vendor Registry and Central Procurement System
    global_registry = GlobalVendorRegistry()
    procurement_system = CentralProcurementSystem(global_registry)

    # 2. Add vendors to the centralized registry
    print("\n--- Initializing Global Vendor Registry ---")
    vendor_A = Vendor("Global Supplies Inc.", "Alice Smith", "123 Main St.", is_approved=True)
    vendor_B = Vendor("Local Parts Co.", "Bob Johnson", "456 Oak Ave.") # Not yet approved
    vendor_C = Vendor("Tech Solutions Ltd.", "Charlie Brown", "789 Pine Ln.", is_approved=True)

    global_registry.add_vendor(vendor_A)
    global_registry.add_vendor(vendor_B)
    global_registry.add_vendor(vendor_C)
    global_registry.list_vendors()

    # 3. Simulate departments submitting purchase requests
    print("\n--- Departments Submitting Requests ---")
    procurement_system.submit_request("IT Department", "Server Rack", 2, vendor_C.vendor_id) # Approved vendor
    procurement_system.submit_request("HR Department", "Office Chairs", 10, vendor_B.vendor_id) # Unapproved vendor
    procurement_system.submit_request("Marketing Dept.", "Promotional Pens", 500, "NONEXISTENT") # Invalid vendor ID
    procurement_system.submit_request("Operations", "Raw Material X", 100, vendor_A.vendor_id) # Approved vendor

    procurement_system.list_requests()

    # 4. Central Procurement processes the requests
    procurement_system.process_all_requests()

    # 5. Review requests after processing
    procurement_system.list_requests()

    # 6. A vendor gets approved later
    print("\n--- Approving a Vendor Later ---")
    global_registry.approve_vendor(vendor_B.vendor_id)
    global_registry.list_vendors()

    # 7. Resubmit a request for the newly approved vendor (or process existing if status allows)
    print("\n--- Resubmitting/Processing Request for Newly Approved Vendor ---")
    # For simplicity, let's submit a new request with the now approved vendor
    procurement_system.submit_request("HR Department", "Desk Lamps", 20, vendor_B.vendor_id)
    procurement_system.process_all_requests()
    procurement_system.list_requests()
