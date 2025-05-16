import matplotlib.pyplot as plt
import pandas as pd
from sqlmodel import Session, select
from fastapi import HTTPException
from api.flows.models.inflow import InflowModel
from api.flows.models.outflow import OutflowModel
from datetime import datetime
import os

def generate_chart(user_id: int, session: Session, output_format="png") -> dict:
    inflows = session.exec(select(InflowModel).where(InflowModel.userId == user_id)).all()
    outflows = session.exec(select(OutflowModel).where(OutflowModel.userId == user_id)).all()

    if not inflows and not outflows:
        raise HTTPException(status_code=404, detail="Sem dados para gerar o gráfico.")

    def to_df(transacoes, tipo):
        return pd.DataFrame([{
            "data": t.date,
            "valor": t.value,
            "tipo": tipo
        } for t in transacoes])

    df = pd.concat([to_df(inflows, "inflow"), to_df(outflows, "outflow")])
    df["mes"] = pd.to_datetime(df["data"]).dt.to_period("M").dt.to_timestamp()
    df_grouped = df.groupby(["mes", "tipo"])["valor"].sum().unstack(fill_value=0).reset_index()

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"chart_{user_id}_{timestamp}"

    os.makedirs("static", exist_ok=True)

    if output_format == "csv":
        path = f"static/{filename}.csv"
        df_grouped.to_csv(path, index=False)
    else:
        path = f"static/{filename}.png"
        df_grouped.plot(x="mes", y=["inflow", "outflow"], kind="bar", figsize=(10, 6))
        plt.title("Entradas e Saídas por Mês")
        plt.xlabel("Mês")
        plt.ylabel("Valor (R$)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()

    return {
        "mensagem": f"📊 Gráfico/relatório gerado com sucesso.",
        "arquivo": path,
        "labels": df_grouped["mes"].dt.strftime("%Y-%m").tolist(),
        "inflows": df_grouped.get("inflow", pd.Series([0]*len(df_grouped))).tolist(),
        "outflows": df_grouped.get("outflow", pd.Series([0]*len(df_grouped))).tolist()
    }


"""from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import pandas as pd
from api.db.session import get_session
from api.flows.models.inflow import InflowModel
from api.flows.models.outflow import OutflowModel

router = APIRouter()

@router.get("/{user_id}")
def get_chart_data(user_id: int, session: Session = Depends(get_session)):
    inflows = session.exec(select(InflowModel).where(InflowModel.userId == user_id)).all()
    outflows = session.exec(select(OutflowModel).where(OutflowModel.userId == user_id)).all()

    if not inflows and not outflows:
        raise HTTPException(status_code=404, detail="Sem dados suficientes para gerar gráfico.")

    def to_df(transacoes, tipo):
        return pd.DataFrame([{
            "data": t.date,
            "valor": t.value,
            "tipo": tipo
        } for t in transacoes])

    df_in = to_df(inflows, "inflow")
    df_out = to_df(outflows, "outflow")
    df = pd.concat([df_in, df_out])

    # Agrupa por mês e tipo (entrada/saída)
    df["mes"] = pd.to_datetime(df["data"]).dt.to_period("M").dt.to_timestamp()
    grouped = df.groupby(["mes", "tipo"])["valor"].sum().unstack(fill_value=0).reset_index()

    # Prepara dados para frontend
    chart_data = {
        "labels": grouped["mes"].dt.strftime("%Y-%m").tolist(),
        "inflows": grouped.get("inflow", pd.Series([0]*len(grouped))).tolist(),
        "outflows": grouped.get("outflow", pd.Series([0]*len(grouped))).tolist()
    }

    return chart_data


# chart_handler.py
from sqlmodel import Session, select
import pandas as pd
from api.flows.models.inflow import InflowModel
from api.flows.models.outflow import OutflowModel

def get_chart(user_id: int, session: Session):
    inflows = session.exec(select(InflowModel).where(InflowModel.userId == user_id)).all()
    outflows = session.exec(select(OutflowModel).where(OutflowModel.userId == user_id)).all()

    if not inflows and not outflows:
        return {
            "mensagem": "Sem dados suficientes para gerar o gráfico."
        }

    def to_df(transacoes, tipo):
        return pd.DataFrame([{
            "data": t.date,
            "valor": t.value,
            "tipo": tipo
        } for t in transacoes])

    df_in = to_df(inflows, "inflow")
    df_out = to_df(outflows, "outflow")
    df = pd.concat([df_in, df_out])

    df["mes"] = pd.to_datetime(df["data"]).dt.to_period("M").dt.to_timestamp()
    grouped = df.groupby(["mes", "tipo"])["valor"].sum().unstack(fill_value=0).reset_index()

    chart_data = {
        "labels": grouped["mes"].dt.strftime("%Y-%m").tolist(),
        "inflows": grouped.get("inflow", pd.Series([0]*len(grouped))).tolist(),
        "outflows": grouped.get("outflow", pd.Series([0]*len(grouped))).tolist(),
        "mensagem": "Aqui está o resumo gráfico de suas entradas e saídas mensais."
    }

    return chart_data

    """


