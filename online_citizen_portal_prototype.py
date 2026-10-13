"""
Online Citizen Service Portal - Week 3 prototype
A simple command-line prototype of service request processing.
Uses sample/in-memory data only; not for production use.
"""
from dataclasses import dataclass
from datetime import datetime
from itertools import count

@dataclass
class ServiceRequest:
    reference_id: str
    citizen_name: str
    service_type: str
    description: str
    status: str
    created_at: str

class CitizenPortal:
    def __init__(self):
        self.requests = []
        self._counter = count(1)

    def submit_request(self, citizen_name, service_type, description):
        if not citizen_name.strip():
            raise ValueError("Citizen name is required.")
        if not service_type.strip():
            raise ValueError("Please select a service.")
        if len(description.strip()) < 10:
            raise ValueError("Description must contain at least 10 characters.")

        ref = f"CSR-{next(self._counter):04d}"
        request = ServiceRequest(
            reference_id=ref,
            citizen_name=citizen_name.strip(),
            service_type=service_type.strip(),
            description=description.strip(),
            status="Submitted",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        self.requests.append(request)
        return request

    def list_requests(self):
        return list(self.requests)

    def update_status(self, reference_id, new_status):
        allowed = {"Submitted", "Under Review", "More Information Required",
                   "Approved", "Rejected", "Completed"}
        if new_status not in allowed:
            raise ValueError("Invalid status.")
        for request in self.requests:
            if request.reference_id == reference_id:
                request.status = new_status
                return request
        raise LookupError("Request reference not found.")

    def get_request(self, reference_id):
        for request in self.requests:
            if request.reference_id == reference_id:
                return request
        return None

if __name__ == "__main__":
    portal = CitizenPortal()
    request = portal.submit_request(
        "Sample Citizen",
        "Residence Certificate",
        "Requesting a residence certificate for official use."
    )
    print("Request submitted:", request.reference_id, request.status)
    portal.update_status(request.reference_id, "Under Review")
    print("Updated status:", portal.get_request(request.reference_id).status)
