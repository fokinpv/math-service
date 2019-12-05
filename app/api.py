from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette.requests import Request

from .solver import Solver, SolverTaskTimeout

router = APIRouter()


class AckermannRequest(BaseModel):
    m: int = Field(..., ge=0)
    n: int = Field(..., ge=0)


class ComputationRequest(BaseModel):
    n: int = Field(..., ge=0)


class ComputationResponse(BaseModel):
    answer: int = Field(..., ge=0)


def get_solver(request: Request):
    """Solver injector."""
    return request.app.solver


@router.post('/api/ackermann', response_model=ComputationResponse)
async def ackermann(
        request: AckermannRequest,
        timeout: float = None,
        solver: Solver = Depends(get_solver),
):
    try:
        result = await solver.ackermann(
            m=request.m, n=request.n, timeout=timeout
        )
    except SolverTaskTimeout:
        raise HTTPException(status_code=404, detail="TimeoutError")
    else:
        return ComputationResponse(answer=result)


@router.post('/api/factorial', response_model=ComputationResponse)
async def factorial(
        request: ComputationRequest,
        timeout: float = None,
        solver: Solver = Depends(get_solver),
):
    try:
        result = await solver.factorial(n=request.n, timeout=timeout)
    except SolverTaskTimeout:
        raise HTTPException(status_code=404, detail="TimeoutError")
    else:
        return ComputationResponse(answer=result)


@router.post('/api/fibonacci', response_model=ComputationResponse)
async def fibonacci(
        request: ComputationRequest,
        timeout: float = None,
        solver: Solver = Depends(get_solver),
):
    try:
        result = await solver.fibonacci(n=request.n, timeout=timeout)
    except SolverTaskTimeout:
        raise HTTPException(status_code=404, detail="TimeoutError")
    else:
        return ComputationResponse(answer=result)
