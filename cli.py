"""
DeepAudit CLI: High-Definition Terminal Forensics & Corporate Due Diligence.
Powered by NVIDIA Nemotron on Nebius Token Factory and Tavily AI Search.
"""

import sys
from pathlib import Path

# Force UTF-8 on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.append(str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from deepaudit.test_cases import list_cases, get_case
from deepaudit.auditor_agent import DeepAuditAgent

console = Console()

def print_banner():
    banner = """
[bold #00D4FF]██████╗ ███████╗███████╗██████╗  [/][bold #76B900]█████╗ ██╗   ██╗██████╗ ██╗████████╗[/]
[bold #00D4FF]██╔══██╗██╔════╝██╔════╝██╔══██╗ [/][bold #76B900]██╔══██╗██║   ██║██╔══██╗██║╚══██╔══╝[/]
[bold #00D4FF]██║  ██║█████╗  █████╗  ██████╔╝ [/][bold #76B900]███████║██║   ██║██║  ██║██║   ██║   [/]
[bold #00D4FF]██║  ██║██╔══╝  ██╔══╝  ██╔═══╝  [/][bold #76B900]██╔══██║██║   ██║██║  ██║██║   ██║   [/]
[bold #00D4FF]██████╔╝███████╗███████╗██║      [/][bold #76B900]██║  ██║╚██████╔╝██████╔╝██║   ██║   [/]
[dim]Autonomous Corporate Forensics & Vendor Due Diligence | Nebius x NVIDIA x Tavily[/dim]
"""
    console.print(banner)

def main():
    print_banner()

    cases = list_cases()
    table = Table(title="[bold cyan]Casos de Auditoría y Proveedores Disponibles[/bold cyan]", show_header=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Empresa / Proveedor", style="bold white")
    table.add_column("CIF", style="yellow")
    table.add_column("Sector", style="magenta")
    table.add_column("Volumen Anual", style="green")

    for i, c in enumerate(cases, 1):
        table.add_row(str(i), c["company_name"], c["cif"], c["sector"], c["annual_volume_invoiced"])

    console.print(table)
    console.print("\n[dim]Selecciona el número de caso (1-3) o pulsa Enter para auditar 'Iberia Logistics' (Caso 1):[/dim]")
    choice = input("Opción [default 1]: ").strip()

    idx = 0
    if choice.isdigit() and 1 <= int(choice) <= len(cases):
        idx = int(choice) - 1

    selected_case = cases[idx]["id"]
    case_meta = get_case(selected_case)

    console.print(Panel(
        f"[bold]Razón Social:[/bold] {case_meta['company_name']}\n"
        f"[bold]CIF / NIF:[/bold] {case_meta['cif']}\n"
        f"[bold]Sector:[/bold] {case_meta['sector']}\n"
        f"[bold]Motivo de Auditoría:[/bold] {case_meta['description']}",
        title="[bold #00D4FF]Ficha del Proveedor Auditado[/bold #00D4FF]",
        border_style="#00D4FF"
    ))

    agent = DeepAuditAgent()
    with Progress(
        SpinnerColumn(style="bold #76B900"),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task(description="Ejecutando análisis forense (Benford + Altman Z + Tavily Web + Nemotron)...", total=None)
        audit_res = agent.run_audit(selected_case)

    # 1. Risk Score
    score = audit_res["risk_score"]
    level = audit_res["risk_level"]
    color = "bold red" if score >= 75 else ("bold yellow" if score >= 40 else "bold green")
    
    console.print(Panel(
        f"Puntuación de Riesgo: [{color}]{score} / 100[/{color}] — Nivel: [{color}]{level}[/{color}]\n"
        f"Tiempo de Auditoría: [cyan]{audit_res['model_metadata']['latency_seconds']} s[/cyan] ({audit_res['model_metadata']['tokens']} tokens)\n"
        f"Motor LLM: [green]{audit_res['model_metadata']['model']}[/green] en [bold green]Nebius Token Factory[/bold green]",
        title="[bold]Evaluación Global de Riesgo Corporativo[/bold]",
        border_style=color.split()[-1]
    ))

    # 2. Forensics: Benford & Altman Z
    benford = audit_res["forensics"]["benford"]
    altman = audit_res["forensics"]["altman_z"]

    stat_table = Table(title="[bold yellow]Telemetría Cuantitativa Interna (Libros y Facturas)[/bold yellow]")
    stat_table.add_column("Métrica Forense", style="bold")
    stat_table.add_column("Valor Obtenido", style="cyan")
    stat_table.add_column("Diagnóstico Técnico", style="bold white")

    b_color = "red" if benford.get("anomaly_detected") else "green"
    stat_table.add_row(
        "Test Ley de Benford (Chi-Cuadrado)",
        f"{benford.get('chi_square_statistic')} (Umbral 15.51)",
        f"[{b_color}]{benford.get('risk_classification')}[/{b_color}]"
    )

    stat_table.add_row(
        "Modelo Altman Z-Score",
        f"Z = {altman.get('z_score')}",
        f"[{altman.get('color')}]{altman.get('zone')}: {altman.get('description')}[/{altman.get('color')}]"
    )

    stat_table.add_row(
        "Fondo de Maniobra / Liquidez",
        f"{altman.get('working_capital_euros')} € (Ratio: {altman.get('current_ratio')})",
        "Déficit severo de liquidez" if altman.get('working_capital_euros', 0) < 0 else "Liquidez operativa correcta"
    )
    console.print(stat_table)

    # 3. Invoice Irregularities
    irregs = audit_res["forensics"]["irregularities"]
    if irregs:
        irreg_table = Table(title="[bold red]Banderas Rojas en Facturación Comercial[/bold red]")
        irreg_table.add_column("Severidad", style="bold red")
        irreg_table.add_column("Código", style="yellow")
        irreg_table.add_column("Descripción Detallada", style="white")

        for irr in irregs:
            irreg_table.add_row(irr["severity"], irr["code"], irr["description"])
        console.print(irreg_table)

    # 4. Tavily External Intel
    tavily = audit_res["external_intel"]
    console.print(Panel(
        f"[bold]Resumen de Fuentes Oficiales:[/bold] {tavily.get('answer')}\n\n" +
        "\n".join([f"• [bold cyan]{r['title']}[/bold cyan]\n  [dim]{r['url']}[/dim]\n  {r['snippet'][:160]}..." for r in tavily.get("results", [])]),
        title="[bold #00D4FF]Evidencias Web en Tiempo Real (Tavily Search API & Boletines Oficiales)[/bold #00D4FF]",
        border_style="#00D4FF"
    ))

    # 5. Executive Report
    console.print("\n[bold #76B900]Dictamen Pericial del Socio de Auditoría (NVIDIA Nemotron):[/bold #76B900]")
    console.print(Panel(audit_res["executive_report"], border_style="#76B900"))

if __name__ == "__main__":
    main()
