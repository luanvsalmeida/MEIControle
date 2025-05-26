# api/events/handlers/chart.py
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from sqlmodel import Session, select, func
from pathlib import Path
import os
from typing import Dict, Any, Optional

from api.flows.models.inflow import InflowModel
from api.flows.models.outflow import OutflowModel

def generate_chart(user_id: int, session: Session) -> Dict[str, Any]:
    """
    Generate daily line chart with points and CSV report for user's inflows and outflows
    
    Args:
        user_id: User ID to filter data
        session: Database session
        
    Returns:
        Dictionary containing message, chart path, and CSV report path
    """
    
    # Query inflows and outflows for the user
    inflow_query = select(InflowModel).where(InflowModel.userId == user_id)
    outflow_query = select(OutflowModel).where(OutflowModel.userId == user_id)
    
    inflows = session.exec(inflow_query).all()
    outflows = session.exec(outflow_query).all()
    
    if not inflows and not outflows:
        return {
            "message": "Nenhum dado encontrado para gerar relatório.",
            "chart": None,
            "report": None
        }
    
    # Convert to DataFrames for easier manipulation
    inflow_data = [
        {
            "date": inflow.date.date(),
            "value": inflow.value,
            "product": inflow.product,
            "client": inflow.client,
            "type": inflow.type,
            "payment_form": inflow.paymentForm
        }
        for inflow in inflows
    ]
    
    outflow_data = [
        {
            "date": outflow.date.date(),
            "value": outflow.value,
            "product": outflow.product,
            "supplier": outflow.supplier,
            "type": outflow.type,
            "payment_form": outflow.paymentForm
        }
        for outflow in outflows
    ]
    
    # Create DataFrames
    df_inflows = pd.DataFrame(inflow_data) if inflow_data else pd.DataFrame()
    df_outflows = pd.DataFrame(outflow_data) if outflow_data else pd.DataFrame()
    
    # Generate CSV report
    csv_path = generate_csv_report(df_inflows, df_outflows, user_id)
    
    # Generate daily aggregated data for chart
    chart_data = prepare_daily_chart_data(df_inflows, df_outflows)
    
    # Generate line chart
    chart_path = generate_line_chart(chart_data, user_id)
    
    # Calculate totals
    total_inflows = df_inflows["value"].sum() if not df_inflows.empty else 0
    total_outflows = df_outflows["value"].sum() if not df_outflows.empty else 0
    balance = total_inflows - total_outflows
    
    # Create message
    message = f"""Relatório gerado com sucesso!
    
📊 Resumo Financeiro:
• Total de Vendas: R$ {total_inflows:.2f}
• Total de Compras: R$ {total_outflows:.2f}
• Saldo: R$ {balance:.2f}

📈 Gráfico diário e relatório CSV foram gerados."""
    
    return {
        "message": message,
        "chart": chart_path,
        "report": csv_path
    }


def prepare_daily_chart_data(df_inflows: pd.DataFrame, df_outflows: pd.DataFrame) -> Dict[str, Any]:
    """
    Prepare daily aggregated data for line chart
    
    Args:
        df_inflows: DataFrame with inflow data
        df_outflows: DataFrame with outflow data
        
    Returns:
        Dictionary with daily aggregated data
    """
    
    # Get date range
    all_dates = []
    if not df_inflows.empty:
        all_dates.extend(df_inflows["date"].tolist())
    if not df_outflows.empty:
        all_dates.extend(df_outflows["date"].tolist())
    
    if not all_dates:
        return {"dates": [], "inflows": [], "outflows": []}
    
    min_date = min(all_dates)
    max_date = max(all_dates)
    
    # Create date range
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # Aggregate daily data
    daily_data = []
    for date in date_range:
        date_obj = date.date()
        
        # Sum inflows for this date
        daily_inflows = df_inflows[df_inflows["date"] == date_obj]["value"].sum() if not df_inflows.empty else 0
        
        # Sum outflows for this date
        daily_outflows = df_outflows[df_outflows["date"] == date_obj]["value"].sum() if not df_outflows.empty else 0
        
        daily_data.append({
            "date": date_obj,
            "inflows": daily_inflows,
            "outflows": daily_outflows
        })
    
    return {
        "dates": [item["date"] for item in daily_data],
        "inflows": [item["inflows"] for item in daily_data],
        "outflows": [item["outflows"] for item in daily_data]
    }


def generate_line_chart(chart_data: Dict[str, Any], user_id: int) -> Optional[str]:
    """
    Generate daily line chart with points
    
    Args:
        chart_data: Dictionary with daily aggregated data
        user_id: User ID for filename
        
    Returns:
        Path to generated chart file
    """
    
    if not chart_data["dates"]:
        return None
    
    # Create figure and axis
    plt.figure(figsize=(12, 6))
    
    # Plot inflows line with points
    plt.plot(chart_data["dates"], chart_data["inflows"], 
             marker='o', linewidth=2, markersize=6, 
             color='#2E8B57', label='Vendas (Inflows)',
             markerfacecolor='#2E8B57', markeredgecolor='white', markeredgewidth=1)
    
    # Plot outflows line with points
    plt.plot(chart_data["dates"], chart_data["outflows"], 
             marker='s', linewidth=2, markersize=6, 
             color='#DC143C', label='Compras (Outflows)',
             markerfacecolor='#DC143C', markeredgecolor='white', markeredgewidth=1)
    
    # Customize chart
    plt.title('Fluxo Financeiro Diário', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Valor (R$)', fontsize=12)
    plt.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
    
    # Format y-axis to show currency
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:.0f}'))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add grid
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save chart
    charts_dir = Path(__file__).resolve().parent.parent.parent / "static" / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    
    chart_filename = f"daily_flow_chart_user_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    chart_path = charts_dir / chart_filename
    
    plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return str(chart_path)


def generate_csv_report(df_inflows: pd.DataFrame, df_outflows: pd.DataFrame, user_id: int) -> str:
    """
    Generate CSV report with all transactions and totals
    
    Args:
        df_inflows: DataFrame with inflow data
        df_outflows: DataFrame with outflow data
        user_id: User ID for filename
        
    Returns:
        Path to generated CSV file
    """
    
    # Create reports directory
    reports_dir = Path(__file__).resolve().parent.parent.parent / "static" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    report_filename = f"financial_report_user_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    report_path = reports_dir / report_filename
    
    # Prepare data for CSV
    csv_data = []
    
    # Add header
    csv_data.append(["RELATÓRIO FINANCEIRO"])
    csv_data.append([""])
    csv_data.append(["=== VENDAS (INFLOWS) ==="])
    csv_data.append(["Data", "Valor", "Produto", "Cliente", "Tipo", "Forma de Pagamento"])
    
    # Add inflow data
    if not df_inflows.empty:
        for _, row in df_inflows.iterrows():
            csv_data.append([
                row["date"].strftime("%d/%m/%Y"),
                f"R$ {row['value']:.2f}",
                row["product"],
                row["client"] or "N/A",
                row["type"] or "N/A",
                row["payment_form"] or "N/A"
            ])
        
        total_inflows = df_inflows["value"].sum()
        csv_data.append(["", "", "", "", "", ""])
        csv_data.append(["TOTAL VENDAS:", f"R$ {total_inflows:.2f}", "", "", "", ""])
    else:
        csv_data.append(["Nenhuma venda registrada"])
        total_inflows = 0
    
    # Add separator
    csv_data.append([""])
    csv_data.append(["=== COMPRAS (OUTFLOWS) ==="])
    csv_data.append(["Data", "Valor", "Produto", "Fornecedor", "Tipo", "Forma de Pagamento"])
    
    # Add outflow data
    if not df_outflows.empty:
        for _, row in df_outflows.iterrows():
            csv_data.append([
                row["date"].strftime("%d/%m/%Y"),
                f"R$ {row['value']:.2f}",
                row["product"],
                row["supplier"] or "N/A",
                row["type"] or "N/A",
                row["payment_form"] or "N/A"
            ])
        
        total_outflows = df_outflows["value"].sum()
        csv_data.append(["", "", "", "", "", ""])
        csv_data.append(["TOTAL COMPRAS:", f"R$ {total_outflows:.2f}", "", "", "", ""])
    else:
        csv_data.append(["Nenhuma compra registrada"])
        total_outflows = 0
    
    # Add summary
    balance = total_inflows - total_outflows
    csv_data.append([""])
    csv_data.append(["=== RESUMO ==="])
    csv_data.append(["Total Vendas:", f"R$ {total_inflows:.2f}"])
    csv_data.append(["Total Compras:", f"R$ {total_outflows:.2f}"])
    csv_data.append(["Saldo:", f"R$ {balance:.2f}"])
    
    # Write CSV file
    df_report = pd.DataFrame(csv_data)
    df_report.to_csv(report_path, index=False, header=False, encoding='utf-8-sig')
    
    return str(report_path)