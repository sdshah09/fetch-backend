'''
Purpose: To store the in-memory solution  to track any data generated through 
API /receipts/{id}/points

Thought Process |
                |-> We will use a hashmap to store the unique receipt ID as a key 
                    and storing (Receipt, points) as the value. Why hashmap because
                    to retrieve the receipt details and points it will take O(1) lookup time.

Reason to use threading:- we only want one thread at a time to read and write data. Due to uvicorn's concurrency
                          we want to prevent race conditions from happening

'''
import threading
from uuid import UUID, uuid4
from app.models import Receipt
from typing import Optional

class StoreReceiptData:
    def __init__(self,logger):
        self.logger = logger
        self._lock = threading.RLock()
        self._db: dict[UUID, tuple[Receipt, int]] = {}


    def save_receipt(self, receipt: Receipt, points: int) -> UUID:
        uid = UUID(str(uuid4()))
        with self._lock:
            self._db[uid] = (receipt, points)
        self.logger.info(f"Receipt {uid} have {points}")
        return uid

    def get_points(self, uid: UUID) -> Optional[int]:
        with self._lock:
            rec = self._db.get(uid)
        return rec[1] if rec else None
