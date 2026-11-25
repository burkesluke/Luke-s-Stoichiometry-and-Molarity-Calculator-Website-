from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from molmass import Formula, FormulaError

app = FastAPI()
templates = Jinja2Templates(directory="templates")

BOT_NAME = "Luke"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "bot_name": BOT_NAME,
            "message": f"{BOT_NAME}: Hello, welcome to Luke's stoichiometry calculator! Choose a calculation below to get started.",
            "selected_calc": "concentration",
        },
    )

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    request: Request,
    calc_type: str = Form(...),
    val1: float = Form(None),
    val2: float = Form(None),
    compound: str = Form(""),
):
    message = ""
    error = False

    try:
        if calc_type == "concentration":
            if val2 == 0:
                raise ZeroDivisionError("Volume cannot be zero.")
            result = round(val1 / val2, 4)
            message = f"{BOT_NAME}: The molarity is {result} mol/L"

        elif calc_type == "moles":
            result = round(val1 * val2, 4)
            message = f"{BOT_NAME}: The number of moles is {result} mol"

        elif calc_type == "volume":
            if val2 == 0:
                raise ZeroDivisionError("Concentration cannot be zero.")
            result = round(val1 / val2, 4)
            message = f"{BOT_NAME}: The volume of the solution is {result} liters"

        elif calc_type == "mass":
            formula = Formula(compound.strip())
            result = round(formula.mass * val1, 4)
            message = f"{BOT_NAME}: The mass of {compound.strip()} is {result} grams"

        elif calc_type == "number_of_moles":
            formula = Formula(compound.strip())
            result = round(val1 / formula.mass, 4)
            message = f"{BOT_NAME}: The number of moles in {compound.strip()} is {result} mol"

        else:
            error = True
            message = f"{BOT_NAME}: Please select a valid calculation type."

    except FormulaError:
        error = True
        message = f"{BOT_NAME}: Invalid chemical formula '{compound}'. Check element capitalization (e.g., H2O, NaCl)."
    except (TypeError, ValueError):
        error = True
        message = f"{BOT_NAME}: Please enter valid numbers for all required fields."
    except ZeroDivisionError as e:
        error = True
        message = f"{BOT_NAME}: {str(e)}"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "bot_name": BOT_NAME,
            "message": message,
            "error": error,
            "selected_calc": calc_type,
        },
    )
