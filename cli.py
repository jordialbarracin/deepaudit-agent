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
    table = Table(title="[bold cyan]Available Corporate Vendor Audit Profiles[/bold cyan]", show_header=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Company / Vendor Name", style="bold white")
    table.add_column("Tax ID / CIF", style="yellow")
    table.add_column("Industry Sector", style="magenta")
    table.add_column("Annual Volume", style="green")

    for i, c in enumerate(cases, 1):
        table.add_row(str(i), c["company_name"], c["cif"], c["sector"], c["annual_volume_invoiced"])

    console.print(table)
    console.print("\n[dim]Select case number (1-5) or press Enter to audit 'Iberia Logistics Global SL' (Case 1):[/dim]")
    choice = input("Option [default 1]: ").strip()

    idx = 0
    if choice.isdigit() and 1 <= int(choice) <= len(cases):
        idx = int(choice) - 1

    selected_case = cases[idx]["id"]
    case_meta = get_case(selected_case)

    console.print(Panel(
        f"[bold]Company Name:[/bold] {case_meta['company_name']}\n"
        f"[bold]Tax ID (CIF/VAT):[/bold] {case_meta['cif']}\n"
        f"[bold]Industry Sector:[/bold] {case_meta['sector']}\n"
        f"[bold]Audit Context:[/bold] {case_meta['description']}",
        title="[bold #00D4FF]Audited Vendor Profile Dossier[/bold #00D4FF]",
        border_style="#00D4FF"
    ))

    agent = DeepAuditAgent()
    with Progress(
        SpinnerColumn(style="bold #76B900"),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task(description="Executing autonomous forensics (Benford + Altman Z + Tavily Web + Nemotron)...", total=None)
        audit_res = agent.run_audit(selected_case)

    # 1. Risk Score
    score = audit_res["risk_score"]
    level = audit_res["risk_level"]
    color = "bold red" if score >= 75 else ("bold yellow" if score >= 40 else "bold green")
    
    console.print(Panel(
        f"Forensic Risk Score: [{color}]{score} / 100[/{color}] — Level: [{color}]{level}[/{color}]\n"
        f"Verdict: [{color}]{audit_res['audit_verdict']}[/{color}]\n"
        f"Audit Latency: [cyan]{audit_res['model_metadata']['latency_seconds']} s[/cyan] ({audit_res['model_metadata']['tokens']} tokens)\n"
        f"Reasoning Engine: [green]{audit_res['model_metadata']['model']}[/green] via [bold green]Nebius Token Factory[/bold green]",
        title="[bold]Comprehensive Corporate Risk Assessment[/bold]",
        border_style=color.split()[-1]
    ))

    # 2. Forensics: Benford & Altman Z
    benford = audit_res["forensics"]["benford"]
    altman = audit_res["forensics"]["altman_z"]

    stat_table = Table(title="[bold yellow]Internal Quantitative Telemetry (Ledgers & Invoices)[/bold yellow]")
    stat_table.add_column("Forensic Indicator", style="bold")
    stat_table.add_column("Computed Value", style="cyan")
    stat_table.add_column("Technical Assessment", style="bold white")

    b_color = "red" if benford.get("anomaly_detected") else "green"
    stat_table.add_row(
        "Benford's Law Chi-Square Test",
        f"{benford.get('chi_square_statistic')} (Threshold 15.51)",
        f"[{b_color}]{benford.get('risk_classification')}[/{b_color}]"
    )

    stat_table.add_row(
        "Altman Z''-Score Model",
        f"Z'' = {altman.get('z_score')}",
        f"[{altman.get('color')}]{altman.get('zone')}: {altman.get('description')}[/{altman.get('color')}]"
    )

    stat_table.add_row(
        "Working Capital / Liquidity",
        f"{altman.get('working_capital_euros')} EUR (Current Ratio: {altman.get('current_ratio')})",
        "Severe working capital deficit" if altman.get('working_capital_euros', 0) < 0 else "Sound working capital"
    )
    console.print(stat_table)

    # 3. Invoice Irregularities
    irregs = audit_res["forensics"]["irregularities"]
    if irregs:
        irreg_table = Table(title="[bold red]Flagged Invoice Ledger Red Flags[/bold red]")
        irreg_table.add_column("Severity", style="bold red")
        irreg_table.add_column("Rule Code", style="yellow")
        irreg_table.add_column("Forensic Description", style="white")

        for irr in irregs:
            irreg_table.add_row(irr["severity"], irr["code"], irr["description"])
        console.print(irreg_table)

    # 4. Tavily External Intel
    tavily = audit_res["external_intel"]
    console.print(Panel(
        f"[bold]Official Gazette & Public Registry Summary:[/bold] {tavily.get('answer')}\n\n" +
        "\n".join([f"• [bold cyan]{r['title']}[/bold cyan]\n  [dim]{r['url']}[/dim]\n  {r['snippet'][:160]}..." for r in tavily.get("results", [])]),
        title="[bold #00D4FF]Real-Time Web Intelligence (Tavily Search API & Official Bulletins)[/bold #00D4FF]",
        border_style="#00D4FF"
    ))

    # 5. Executive Report
    console.print("\n[bold #76B900]Forensic Auditor Formal Dictum (NVIDIA Nemotron):[/bold #76B900]")
    console.print(Panel(audit_res["executive_report"], border_style="#76B900"))

if __name__ == "__main__":
    main()
