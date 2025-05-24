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
        #"mensagem": f"📊 Gráfico/relatório gerado com sucesso.",
        "mensagem": f"Grafico/relatorio gerado com sucesso.",
        "arquivo": path,
        "labels": df_grouped["mes"].dt.strftime("%Y-%m").tolist(),
        "inflows": df_grouped.get("inflow", pd.Series([0]*len(df_grouped))).tolist(),
        "outflows": df_grouped.get("outflow", pd.Series([0]*len(df_grouped))).tolist()
    }

