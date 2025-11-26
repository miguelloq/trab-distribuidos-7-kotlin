#!/usr/bin/env python3
"""
Script para gerar gráficos comparativos dos testes de carga
Compara os 4 tipos de comunicação (REST, GraphQL, SOAP, gRPC) em diferentes cargas
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from pathlib import Path

# Configuração de estilo
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

# Diretórios
RESULTS_DIR = "/teste-carga/results"
CHARTS_DIR = "/teste-carga/charts"

# Criar diretório de gráficos
os.makedirs(CHARTS_DIR, exist_ok=True)

# Protocolos e cargas
PROTOCOLS = ["rest", "graphql", "soap", "grpc"]
USER_COUNTS = [100, 1000, 10000]

# Mapeamento de nomes das tarefas
TASK_NAMES = {
    "REST - Listar Todas Músicas": "Listar Músicas",
    "REST - Listar Todos Usuários": "Listar Usuários",
    "REST - Listar Playlists de Usuário": "Listar Playlists",
    "GraphQL - Listar Todas Músicas": "Listar Músicas",
    "GraphQL - Listar Todos Usuários": "Listar Usuários",
    "GraphQL - Listar Playlists de Usuário": "Listar Playlists",
    "SOAP - Listar Todas Músicas": "Listar Músicas",
    "SOAP - Listar Todos Usuários": "Listar Usuários",
    "SOAP - Listar Playlists de Usuário": "Listar Playlists",
    "gRPC - Listar Todas Músicas": "Listar Músicas",
    "gRPC - Listar Todos Usuários": "Listar Usuários",
    "gRPC - Listar Playlists de Usuário": "Listar Playlists",
}

def load_test_results():
    """Carrega todos os resultados dos testes"""
    all_data = []

    for protocol in PROTOCOLS:
        for user_count in USER_COUNTS:
            csv_file = f"{RESULTS_DIR}/{protocol}_{user_count}_users_stats.csv"

            if not os.path.exists(csv_file):
                print(f"⚠️  Arquivo não encontrado: {csv_file}")
                continue

            try:
                df = pd.read_csv(csv_file)

                # Adicionar informações de protocolo e carga
                df['protocol'] = protocol.upper()
                df['user_count'] = user_count

                # Simplificar nomes das tarefas
                df['task'] = df['Name'].map(TASK_NAMES).fillna(df['Name'])

                all_data.append(df)
                print(f"✓ Carregado: {protocol.upper()} com {user_count} usuários")

            except Exception as e:
                print(f"❌ Erro ao carregar {csv_file}: {e}")

    if not all_data:
        print("❌ Nenhum dado foi carregado!")
        return None

    return pd.concat(all_data, ignore_index=True)

def plot_response_time_comparison(df):
    """Gráfico comparando tempo de resposta médio entre protocolos"""
    print("\n📊 Gerando gráfico: Tempo de Resposta Médio")

    # Filtrar apenas as linhas com dados válidos
    df_filtered = df[df['Name'] != 'Aggregated'].copy()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Comparação de Tempo de Resposta Médio por Protocolo', fontsize=16, fontweight='bold')

    for idx, user_count in enumerate(USER_COUNTS):
        ax = axes[idx]
        data = df_filtered[df_filtered['user_count'] == user_count]

        # Pivot para facilitar o plot
        pivot_data = data.pivot_table(
            values='Average Response Time',
            index='task',
            columns='protocol',
            aggfunc='mean'
        )

        pivot_data.plot(kind='bar', ax=ax)
        ax.set_title(f'{user_count} Usuários', fontsize=14, fontweight='bold')
        ax.set_xlabel('Funcionalidade', fontsize=12)
        ax.set_ylabel('Tempo Médio (ms)', fontsize=12)
        ax.legend(title='Protocolo', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/response_time_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Salvo: {CHARTS_DIR}/response_time_comparison.png")

def plot_requests_per_second(df):
    """Gráfico comparando requisições por segundo"""
    print("\n📊 Gerando gráfico: Requisições por Segundo")

    df_filtered = df[df['Name'] != 'Aggregated'].copy()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Comparação de Requisições por Segundo (RPS)', fontsize=16, fontweight='bold')

    for idx, user_count in enumerate(USER_COUNTS):
        ax = axes[idx]
        data = df_filtered[df_filtered['user_count'] == user_count]

        pivot_data = data.pivot_table(
            values='Requests/s',
            index='task',
            columns='protocol',
            aggfunc='mean'
        )

        pivot_data.plot(kind='bar', ax=ax)
        ax.set_title(f'{user_count} Usuários', fontsize=14, fontweight='bold')
        ax.set_xlabel('Funcionalidade', fontsize=12)
        ax.set_ylabel('Requisições/s', fontsize=12)
        ax.legend(title='Protocolo', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/requests_per_second.png', dpi=300, bbox_inches='tight')
    print(f"✓ Salvo: {CHARTS_DIR}/requests_per_second.png")

def plot_failure_rate(df):
    """Gráfico comparando taxa de falhas"""
    print("\n📊 Gerando gráfico: Taxa de Falhas")

    df_filtered = df[df['Name'] != 'Aggregated'].copy()

    # Calcular taxa de falhas
    df_filtered['failure_rate'] = (df_filtered['Failure Count'] / df_filtered['Request Count'] * 100).fillna(0)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Comparação de Taxa de Falhas (%)', fontsize=16, fontweight='bold')

    for idx, user_count in enumerate(USER_COUNTS):
        ax = axes[idx]
        data = df_filtered[df_filtered['user_count'] == user_count]

        pivot_data = data.pivot_table(
            values='failure_rate',
            index='task',
            columns='protocol',
            aggfunc='mean'
        )

        pivot_data.plot(kind='bar', ax=ax, color=['green', 'blue', 'orange', 'red'])
        ax.set_title(f'{user_count} Usuários', fontsize=14, fontweight='bold')
        ax.set_xlabel('Funcionalidade', fontsize=12)
        ax.set_ylabel('Taxa de Falhas (%)', fontsize=12)
        ax.legend(title='Protocolo', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/failure_rate.png', dpi=300, bbox_inches='tight')
    print(f"✓ Salvo: {CHARTS_DIR}/failure_rate.png")

def plot_percentiles_comparison(df):
    """Gráfico comparando percentis de tempo de resposta"""
    print("\n📊 Gerando gráfico: Comparação de Percentis")

    df_filtered = df[df['Name'] != 'Aggregated'].copy()

    fig, axes = plt.subplots(3, 3, figsize=(20, 18))
    fig.suptitle('Comparação de Percentis de Tempo de Resposta (p50, p95, p99)', fontsize=16, fontweight='bold')

    percentiles = ['50%', '95%', '99%']

    for row_idx, user_count in enumerate(USER_COUNTS):
        for col_idx, percentile in enumerate(percentiles):
            ax = axes[row_idx, col_idx]
            data = df_filtered[df_filtered['user_count'] == user_count]

            pivot_data = data.pivot_table(
                values=percentile,
                index='task',
                columns='protocol',
                aggfunc='mean'
            )

            pivot_data.plot(kind='bar', ax=ax)
            ax.set_title(f'{user_count} Usuários - Percentil {percentile}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Funcionalidade', fontsize=10)
            ax.set_ylabel('Tempo (ms)', fontsize=10)
            ax.legend(title='Protocolo', fontsize=8)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/percentiles_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Salvo: {CHARTS_DIR}/percentiles_comparison.png")

def plot_overall_performance(df):
    """Gráfico de performance geral agregada"""
    print("\n📊 Gerando gráfico: Performance Geral")

    # Usar apenas dados agregados
    df_aggregated = df[df['Name'] == 'Aggregated'].copy()

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Performance Geral por Protocolo', fontsize=16, fontweight='bold')

    # Gráfico 1: Tempo médio de resposta
    ax1 = axes[0, 0]
    pivot1 = df_aggregated.pivot_table(
        values='Average Response Time',
        index='user_count',
        columns='protocol'
    )
    pivot1.plot(kind='line', marker='o', ax=ax1, linewidth=2)
    ax1.set_title('Tempo Médio de Resposta', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Número de Usuários', fontsize=10)
    ax1.set_ylabel('Tempo Médio (ms)', fontsize=10)
    ax1.legend(title='Protocolo')
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Requisições por segundo
    ax2 = axes[0, 1]
    pivot2 = df_aggregated.pivot_table(
        values='Requests/s',
        index='user_count',
        columns='protocol'
    )
    pivot2.plot(kind='line', marker='s', ax=ax2, linewidth=2)
    ax2.set_title('Requisições por Segundo', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Número de Usuários', fontsize=10)
    ax2.set_ylabel('Requisições/s', fontsize=10)
    ax2.legend(title='Protocolo')
    ax2.grid(True, alpha=0.3)

    # Gráfico 3: Total de requisições
    ax3 = axes[1, 0]
    pivot3 = df_aggregated.pivot_table(
        values='Request Count',
        index='user_count',
        columns='protocol'
    )
    pivot3.plot(kind='bar', ax=ax3)
    ax3.set_title('Total de Requisições', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Número de Usuários', fontsize=10)
    ax3.set_ylabel('Total de Requisições', fontsize=10)
    ax3.legend(title='Protocolo')
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=0)

    # Gráfico 4: Taxa de falhas
    ax4 = axes[1, 1]
    df_aggregated['failure_rate'] = (df_aggregated['Failure Count'] / df_aggregated['Request Count'] * 100).fillna(0)
    pivot4 = df_aggregated.pivot_table(
        values='failure_rate',
        index='user_count',
        columns='protocol'
    )
    pivot4.plot(kind='line', marker='^', ax=ax4, linewidth=2)
    ax4.set_title('Taxa de Falhas', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Número de Usuários', fontsize=10)
    ax4.set_ylabel('Taxa de Falhas (%)', fontsize=10)
    ax4.legend(title='Protocolo')
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/overall_performance.png', dpi=300, bbox_inches='tight')
    print(f"✓ Salvo: {CHARTS_DIR}/overall_performance.png")

def generate_summary_report(df):
    """Gera relatório resumido em texto"""
    print("\n📄 Gerando relatório resumido")

    report_file = f'{CHARTS_DIR}/summary_report.txt'

    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("RELATÓRIO DE TESTES DE CARGA - MUSIC STREAMING API\n")
        f.write("=" * 80 + "\n\n")

        for user_count in USER_COUNTS:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"CARGA: {user_count} USUÁRIOS\n")
            f.write(f"{'=' * 80}\n\n")

            data = df[df['user_count'] == user_count]

            for protocol in PROTOCOLS:
                protocol_data = data[data['protocol'] == protocol.upper()]

                if protocol_data.empty:
                    continue

                f.write(f"\n{protocol.upper()}\n")
                f.write("-" * 40 + "\n")

                # Dados agregados
                aggregated = protocol_data[protocol_data['Name'] == 'Aggregated']

                if not aggregated.empty:
                    row = aggregated.iloc[0]
                    f.write(f"  Total de Requisições: {row['Request Count']:.0f}\n")
                    f.write(f"  Requisições/s: {row['Requests/s']:.2f}\n")
                    f.write(f"  Tempo Médio: {row['Average Response Time']:.2f} ms\n")
                    f.write(f"  Tempo Mínimo: {row['Min Response Time']:.2f} ms\n")
                    f.write(f"  Tempo Máximo: {row['Max Response Time']:.2f} ms\n")
                    f.write(f"  Percentil 50%: {row['50%']:.2f} ms\n")
                    f.write(f"  Percentil 95%: {row['95%']:.2f} ms\n")
                    f.write(f"  Percentil 99%: {row['99%']:.2f} ms\n")
                    f.write(f"  Falhas: {row['Failure Count']:.0f}\n")

                f.write("\n")

    print(f"✓ Salvo: {report_file}")

def main():
    print("=" * 80)
    print("GERAÇÃO DE GRÁFICOS COMPARATIVOS - TESTES DE CARGA")
    print("=" * 80)

    # Carregar dados
    print("\n📂 Carregando resultados dos testes...")
    df = load_test_results()

    if df is None or df.empty:
        print("\n❌ Nenhum dado disponível para gerar gráficos!")
        print("Execute os testes primeiro com: ./run_tests.sh")
        return

    print(f"\n✓ Total de registros carregados: {len(df)}")

    # Gerar gráficos
    print("\n📊 Gerando gráficos...")
    plot_response_time_comparison(df)
    plot_requests_per_second(df)
    plot_failure_rate(df)
    plot_percentiles_comparison(df)
    plot_overall_performance(df)

    # Gerar relatório
    generate_summary_report(df)

    print("\n" + "=" * 80)
    print("✅ TODOS OS GRÁFICOS FORAM GERADOS COM SUCESSO!")
    print("=" * 80)
    print(f"\n📁 Gráficos salvos em: {CHARTS_DIR}")
    print("\nGráficos gerados:")
    print("  - response_time_comparison.png")
    print("  - requests_per_second.png")
    print("  - failure_rate.png")
    print("  - percentiles_comparison.png")
    print("  - overall_performance.png")
    print("  - summary_report.txt")
    print()

if __name__ == "__main__":
    main()
