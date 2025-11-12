import uvicorn
from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from schemas import AppealCreate, AppealCreateMultiple, AppealResponse, ProblemInfo
from utils.file_handler import save_appeal_to_json, get_appeal_by_id

app = FastAPI(
    title="Сервис обращений абонентов",
    description="Сервис для сбора и обработки обращений абонентов",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Сервис обращений абонентов работает"}


@app.post("/appeal", response_model=AppealResponse, status_code=status.HTTP_201_CREATED)
async def create_appeal(appeal: AppealCreate):
    """
    Создание обращения с одной причиной (Задания 1 и 2)
    """
    try:
        appeal_data = appeal.dict()

        appeal_id = save_appeal_to_json(appeal_data)

        return AppealResponse(
            id=appeal_id,
            appeal_data=appeal_data,
            created_at=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении обращения: {str(e)}"
        )


@app.post("/appeal/multiple", response_model=AppealResponse, status_code=status.HTTP_201_CREATED)
async def create_appeal_multiple(appeal: AppealCreateMultiple):
    try:
        appeal_data = appeal.dict()
        appeal_id = save_appeal_to_json(appeal_data)

        return AppealResponse(
            id=appeal_id,
            appeal_data=appeal_data,
            created_at=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении обращения: {str(e)}"
        )


@app.get("/appeal/{appeal_id}", response_model=AppealResponse)
async def get_appeal(appeal_id: str):
    appeal_data = get_appeal_by_id(appeal_id)

    if not appeal_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Обращение не найдено"
        )

    return appeal_data


@app.post("/appeal/simple", status_code=status.HTTP_201_CREATED)
async def create_simple_appeal(
        last_name: str,
        first_name: str,
        birth_date: str,
        phone: str,
        email: str,
        problem_type: str,
        detection_datetime: str
):

    try:
        problem = ProblemInfo(
            problem_type=problem_type,
            detection_datetime=datetime.fromisoformat(detection_datetime)
        )

        appeal = AppealCreate(
            last_name=last_name,
            first_name=first_name,
            birth_date=datetime.strptime(birth_date, "%Y-%m-%d").date(),
            phone=phone,
            email=email,
            problem=problem
        )

        appeal_data = appeal.dict()
        appeal_id = save_appeal_to_json(appeal_data)

        return {
            "id": appeal_id,
            "message": "Обращение успешно создано",
            "data": appeal_data
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании обращения: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
