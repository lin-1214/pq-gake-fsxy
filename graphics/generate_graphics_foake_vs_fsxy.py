#!/usr/bin/env python3

import subprocess
import pandas as pd
import seaborn as sns
import numpy as np
import yaml
import sys
import signal
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

COLORS = {
    'Classic-McEliece-348864': "#6F0062" ,
    'Classic-McEliece-348864f': "#A77500",
    'Classic-McEliece-460896': "#1CE6FF",
    'Classic-McEliece-460896f': "#FF34FF",
    'Classic-McEliece-6688128': "#FF4A46",
    'Classic-McEliece-6688128f': "#008941",
    'Classic-McEliece-6960119': "#006FA6",
    'Classic-McEliece-6960119f': "#A30059",
    'Classic-McEliece-8192128': "#6A3A4C",
    'Classic-McEliece-8192128f': "#7A4900",
    'Kyber512': "#0000A6",
    'Kyber768': "#63FFAC",
    'Kyber1024': "#B79762",
    'NTRU-HPS-2048-509': "#004D43",
    'NTRU-HPS-2048-677': "#5A0007",
    'NTRU-HRSS-701': "#809693",
    'NTRU-HPS-4096-821': "#0089A3",
    'LightSaber-KEM': "#FAD09F",
    'Saber-KEM': "#4FC601",
    'FireSaber-KEM': "#3B5DFF"
}

def plot_scalability_level(data, config):

    fig, axes = plt.subplots(1,3, figsize=(18,6), dpi=200, sharey=True)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)
    fig.tight_layout(pad=2)

    for (j, alg) in enumerate(["Kyber512", "Kyber768", "Kyber1024"]):
        df = data[data['algorithm'] == alg]
        df2 = df[['algorithm', 'mean_time_us', 'N', 'operation', 'type']]
        # print(data)
        df2 = df2.groupby(['algorithm', 'N', 'type'])['mean_time_us'].sum().reset_index()
        df2['mean_time_us'] = df2['mean_time_us']/df2['N']
        print(df2)
        sns.lineplot(ax=axes[j], x="N", y="mean_time_us", hue="type", data=df2, linewidth=2, markers=True, dashes=False)
        leg = axes[j].legend(loc='upper left', frameon=True)
        if(j > 0): leg.set_visible(False)
        # axes.set_title("Level {}".format(LEVELS_LABELS[j]), fontsize="x-large")
        axes[j].set_xlabel('Number of parties', fontsize="x-large")
        axes[j].set_ylabel('Time (us)', fontsize="x-large")
        axes[j].set_title(alg, fontsize="x-large")


    figname = "{}/{}/fsxy_vs_fo-ake-scalability.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname, bbox_inches="tight")
    print("Saved file to {}".format(figname), flush=True)

def plot_speed_gake(data, config):

    fig, axes = plt.subplots(1,4, figsize=(18,6), dpi=200, sharey=True)
    # fig.suptitle('GAKE operations', fontsize=30)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)
    fig.tight_layout(pad=2)

    operations = ['init', 'round12', 'round3', 'round4']
    operations_names = ['Init', 'Round 1-2', 'Round 3', 'Round 4']
    for (i, var) in enumerate(operations):

        df = data[(data['operation'] == var)]
        df2 = df[['algorithm','operation', 'mean_cpu_cycles', 'type']]

        sns.barplot(ax=axes[i], x="algorithm", y="mean_cpu_cycles", data=df2, hue="type", order=["Kyber512", "Kyber768", "Kyber1024"])
        axes[i].set_title(operations_names[i], fontsize="x-large")
        # axes[j].legend(loc='upper left')
        leg = axes[i].legend(loc='upper left', frameon=True)
        if(i >= 0): leg.set_visible(False)
        axes[i].tick_params(axis='x')
        axes[i].set(yscale="symlog")
        axes[i].set_xlabel('', fontsize="x-large")
        axes[i].set_ylabel('CPU Cycles', fontsize="x-large")
        # axes[j,i+1].axis('equal')

    figname = "{}/{}/fsxy_vs_fo-ake_gake.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname, bbox_inches="tight")
    print("Saved file to {}".format(figname), flush=True)

def plot_speed_ake(data, config):

    fig, axes = plt.subplots(1,3, figsize=(18,6), dpi=200, sharey=True)
    # fig.suptitle('FSXY vs FO_AKE', fontsize=30)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)
    fig.tight_layout(pad=2)

    operations = ['init', 'algB', 'algA']
    operations_names = ['Init', 'AlgB', 'AlgA']

    for (i, var) in enumerate(operations):
        df = data[(data['operation'] == var)]

        df2 = df[['algorithm', 'operation', 'mean_cpu_cycles', 'type']]

        sns.barplot(ax=axes[i], x="algorithm", y="mean_cpu_cycles", data=df2, hue="type", order=["Kyber512", "Kyber768", "Kyber1024"])
        axes[i].set_title(operations_names[i], fontsize="x-large")
        leg = axes[i].legend(loc='upper left', frameon=True)
        if(i > 0): leg.set_visible(False)
        # axes[i].tick_params(axis='x', rotation=90)
        axes[i].set(yscale="symlog")
        axes[i].set_xlabel('', fontsize="x-large")
        axes[i].set_ylabel('CPU Cycles', fontsize="x-large")
        # axes[j,i+1].axis('equal')

    figname = "{}/{}/fsxy_vs_fo-ake_ake.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname, bbox_inches="tight")
    print("Saved file to {}".format(figname), flush=True)

def main():
    pd.options.mode.chained_assignment = None

    if(len(sys.argv) != 2):
        print("You must provide a config file (e.g. config.yaml)", flush=True)
        sys.exit(1)

    file = sys.argv[1]
    if not Path(file).is_file():
        print("File {} does NOT exist".format(file), flush=True)
        sys.exit(1)

    with open(file) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    fsxy_ake_file = "{}/{}/ake.csv".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    if not Path(fsxy_ake_file).is_file():
        print("File {} does NOT exist".format(fsxy_ake_file), flush=True)
        sys.exit(1)

    fo_ake_file = "{}/{}/fo-ake-ake.csv".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    if not Path(fo_ake_file).is_file():
        print("File {} does NOT exist".format(fo_ake_file), flush=True)
        sys.exit(1)

    fsxy_gake_file = "{}/{}/gake.csv".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    if not Path(fsxy_gake_file).is_file():
        print("File {} does NOT exist".format(fsxy_gake_file), flush=True)
        sys.exit(1)

    fo_gake_file = "{}/{}/fo-ake-gake.csv".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    if not Path(fo_gake_file).is_file():
        print("File {} does NOT exist".format(fo_gake_file), flush=True)
        sys.exit(1)

    data_fsxy_ake = pd.read_csv(fsxy_ake_file)
    data_fo_ake = pd.read_csv(fo_ake_file)
    data_ake = pd.concat([data_fsxy_ake, data_fo_ake])
    data_ake = data_ake.loc[data_ake['algorithm'].isin(["Kyber512", "Kyber768", "Kyber1024"])]
    data_ake.loc[data_ake["type"] == "ake", 'type'] = "fsxy"
    data_ake.loc[data_ake["operation"] == "der_resp", 'operation'] = "algB"
    data_ake.loc[data_ake["operation"] == "der_init", 'operation'] = "algA"

    data_fsxy_gake = pd.read_csv(fsxy_gake_file)
    data_fo_gake = pd.read_csv(fo_gake_file)
    data_gake = pd.concat([data_fsxy_gake, data_fo_gake])
    data_gake = data_gake.loc[data_gake['algorithm'].isin(["Kyber512", "Kyber768", "Kyber1024"])]
    data_gake.loc[data_gake["type"] == "gake", 'type'] = "fsxy"
    data_gake.loc[data_gake["type"] == "fo-gake", 'type'] = "fo-ake"
    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(data_gake)

    plot_speed_ake(data_ake, config)
    plot_speed_gake(data_gake, config)
    plot_scalability_level(data_gake, config)

if __name__ == '__main__':
    main()
