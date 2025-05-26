# api/events/handlers/forecast.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from api.db.session import get_session
from api.flows.models.inflow import InflowModel
from api.flows.models.outflow import OutflowModel

router = APIRouter()

@router.get("/{user_id}")
def get_forecast(user_id: int, session: Session = Depends(get_session)):
    inflows = session.exec(select(InflowModel).where(InflowModel.userId == user_id)).all()
    outflows = session.exec(select(OutflowModel).where(OutflowModel.userId == user_id)).all()

    if not inflows and not outflows:
        raise HTTPException(status_code=404, detail="Sem dados suficientes para previsão.")

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
    grouped["mes_num"] = np.arange(len(grouped))

    def prever(coluna):
        if coluna not in grouped.columns:
            return 0.0  # Coluna inexistente

        count = grouped[coluna].count()

        if count == 0:
            return 0.0  # Nenhum dado

        if count == 1:
            # Apenas um ponto: retorna o próprio valor
            return float(grouped[coluna].iloc[0])

        # Regressão linear para previsão
        X = grouped[["mes_num"]]
        y = grouped[coluna]
        model = LinearRegression()
        model.fit(X, y)

        proximo_mes = [[grouped["mes_num"].iloc[-1] + 1]]
        return float(model.predict(proximo_mes)[0])

    inflow_prev = prever("inflow")
    outflow_prev = prever("outflow")

    return {
        "mensagem": (
            #f"Com base nas tendências anteriores, a previsão para o próximo mês "
            #f"é de entrada de R$ {inflow_prev:.2f} e saída de R$ {outflow_prev:.2f}."
            f"Com base nas tendencias anteriores, a previsao para o proximo mes "
            f"e de entrada de RS {inflow_prev:.2f} e saida de RS {outflow_prev:.2f}."
        )
    }
