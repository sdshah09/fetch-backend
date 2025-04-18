from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID

from .models import Receipt, ProcessResponse, PointsResponse
from .calc import CalculatePoints
from .store import StoreReceiptData
from utils.logging_module import setup_logger
app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AppRoutes:
    def __init__(self):
        self.logger = setup_logger('main.log')
        self.calc = CalculatePoints(self.logger)
        self.store = StoreReceiptData(self.logger)

        router.post(
            "/receipts/process",
            response_model=ProcessResponse,
            status_code=201,
            summary="Process a receipt and return its ID",
        )(self.process_receipt)

        router.get(
            "/receipts/{id}/points",
            response_model=PointsResponse,
            summary="Get points awarded to a receipt",
        )(self.get_points)

    async def process_receipt(self, receipt: Receipt):
        points = self.calc.calculate_total_points(receipt)
        uid = self.store.save_receipt(receipt, points)
        return ProcessResponse(id=uid)

    async def get_points(self, id: UUID):
        points = self.store.get_points(id)
        if points is None:
            raise HTTPException(status_code=404, detail="Receipt not Found")
        return PointsResponse(points=points)

AppRoutes()
app.include_router(router)
