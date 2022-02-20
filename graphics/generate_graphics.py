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
    'Classic-McEliece-348864': "#372101" ,
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
    'LightSaber-KEM': "#1B4400",
    'Saber-KEM': "#4FC601",
    'FireSaber-KEM': "#3B5DFF"
}

def plot_scalability_level(data, config):

    LEVELS = [config["L1"], config["L3"], config["L5"]]
    LEVELS_LABELS = [1,3,5]

    def conditions(s):
        if (s['algorithm'] in (LEVELS[0])):
            return "Level 1"
        if (s['algorithm'] in (LEVELS[1])):
            return "Level 3"
        if (s['algorithm'] in (LEVELS[2])):
            return "Level 5"
        else:
            return ""

    fig, axes = plt.subplots(3, figsize=(15,15), dpi=200, sharey=True)
    fig.suptitle('Scalability', fontsize=30)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)

    for (j, level) in enumerate(LEVELS):
        df = data[data['algorithm'].isin(level)]

        df2 = df[['algorithm', 'mean_cpu_cycles', 'N', 'operation']]
        print(data)
        df2 = df2.groupby(['algorithm','N'])['mean_cpu_cycles'].sum().reset_index()
        print(df2)
        p = sns.lineplot(ax=axes[j], x="N", y="mean_cpu_cycles", hue="algorithm", data=df2, palette=COLORS, linewidth=2, style="algorithm", markers=True, dashes=False)
        axes[j].set_title("Level {}".format(LEVELS_LABELS[j]), fontsize="x-large")
        axes[j].set_xlabel('Number of parties', fontsize="x-large")
        axes[j].set_ylabel('CPU Cycles', fontsize="x-large")

        h, l = p.get_legend_handles_labels()
        l, h = zip(*sorted(zip(l, h)))
        p.legend(h, l)

        figname = "{}/{}/scalability_level.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
        fig.savefig(figname, bbox_inches="tight")
        print("Saved file to {}".format(figname), flush=True)

def plot_scalability(data, config):

    fig, axes = plt.subplots(1, figsize=(25,25), dpi=200, dpi=200)
    fig.suptitle('Scalability', fontsize=30)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)

    df2 = data[['algorithm', 'mean_cpu_cycles', 'N', 'operation']]
    print(data)
    df2 = df2.groupby(['algorithm','N'])['mean_cpu_cycles'].sum().reset_index()
    print(df2)
    p = sns.lineplot(ax=axes, x="N", y="mean_cpu_cycles", hue="algorithm", data=df2, palette=COLORS, linewidth=2, style="algorithm", markers=True, dashes=False)
    axes.set_xlabel('Number of parties', fontsize="x-large")
    axes.set_ylabel('CPU Cycles', fontsize="x-large")

    h, l = p.get_legend_handles_labels()
    l, h = zip(*sorted(zip(l, h)))
    p.legend(h, l)

    figname = "{}/{}/scalability.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname, bbox_inches="tight")
    print("Saved file to {}".format(figname), flush=True)

def plot_heatmap_level(data, config):

    cmap = LinearSegmentedColormap.from_list('RedGreenRed', ['lime', 'crimson'])

    LEVELS = [config["L1"], config["L3"], config["L5"]]
    LEVELS_LABELS = [1,3,5]

    def conditions(s):
        if (s['algorithm'] in (LEVELS[0])):
            return "Level 1"
        if (s['algorithm'] in (LEVELS[1])):
            return "Level 3"
        if (s['algorithm'] in (LEVELS[2])):
            return "Level 5"
        else:
            return ""

    fig, axes2 = plt.subplots(1, 3, figsize=(30, 18), dpi=200)
    fig.suptitle('Operation heatmap', fontsize=30)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)

    df = data.copy()
    data["operation"] = data["type"].astype(str) + "-" + data["operation"].astype(str)
    data["level"] = data.apply(conditions, axis=1)

    for (j, level) in enumerate(LEVELS):
        df = data[data['algorithm'].isin(level)]
        df2 = df.reset_index(drop = True)
        df2 = df[['algorithm', 'operation', 'mean_cpu_cycles']]
        df2['mean_cpu_cycles'] = np.log(df2['mean_cpu_cycles'])
        df2 = df2.pivot(index='operation', columns='algorithm', values='mean_cpu_cycles')

        grid_kws = {"height_ratios": (.9, .1), "hspace": .001}
        f, (axes, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws)
        ax = sns.heatmap(ax=axes2[j],
                         data=df2,
                         annot=True,
                         fmt="0.2f",
                         linewidths=0.5,
                         cmap=cmap,
                         # square=True,
                         cbar_ax=cbar_ax,
                         cbar_kws={"orientation": "horizontal"})

        axes2[j].set_title("Level {}".format(LEVELS_LABELS[j]), fontsize="x-large")
        axes2[j].set_xlabel('', fontsize="x-large")
        axes2[j].set_ylabel('Operation', fontsize="x-large")
        axes2[j].tick_params(axis='y', rotation=0)


    fig.suptitle('Operations heatmap', fontsize=30)
    plt.yticks(rotation=0)

    figname = "{}/{}/cycles_operations_level.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname, bbox_inches="tight")
    print("Saved file to {}".format(figname), flush=True)

def plot_heatmap(data, config):

    cmap = LinearSegmentedColormap.from_list('RedGreenRed', ['lime', 'crimson'])


    df = data.copy()
    df["operation"] = data["type"].astype(str) + "-" + data["operation"].astype(str)
    df = df[['algorithm', 'operation', 'mean_cpu_cycles']]
    df['mean_cpu_cycles'] = np.log(df['mean_cpu_cycles'])
    df = df.pivot(index='operation', columns='algorithm', values='mean_cpu_cycles')
    print(df)

    grid_kws = {"height_ratios": (.9, .01), "hspace": .001}
    fig, (axes, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws, figsize=(15,15))
    ax = sns.heatmap(ax=axes,
                     data=df,
                     annot=True,
                     fmt="0.2f",
                     linewidths=0.5,
                     cmap=cmap,
                     square=True,
                     cbar_ax=cbar_ax,
                     cbar_kws={"orientation": "horizontal"})

    fig.suptitle('Operations heatmap', fontsize=30)
    axes.set_xlabel('', fontsize="x-large")
    axes.set_ylabel('Operation', fontsize="x-large")

    plt.yticks(rotation=0)

    figname = "{}/{}/cycles_operations.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname, bbox_inches="tight")
    print("Saved file to {}".format(figname), flush=True)

def plot_speed_commitment(data, config):

    fig, axes = plt.subplots(3,3, figsize=(25,25), dpi=200, sharey=True)
    fig.suptitle('Commitment operations', fontsize=30)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)

    LEVELS = [config["L1"], config["L3"], config["L5"]]
    LEVELS_LABELS = [1,3,5]

    def conditions(s):
        if (s['algorithm'] in (LEVELS[0])):
            return "Level 1"
        if (s['algorithm'] in (LEVELS[1])):
            return "Level 3"
        if (s['algorithm'] in (LEVELS[2])):
            return "Level 5"
        else:
            return ""

    data["level"] = data.apply(conditions, axis=1)

    operations = ['init', 'commit', 'check']
    operations_names = ['Init', 'Commit', 'Check']
    for (i, var) in enumerate(operations):
        for (j, level) in enumerate(LEVELS):
            df = data[(data['operation'] == var) & data['algorithm'].isin(level)]

            df2 = df[['algorithm','operation', 'mean_cpu_cycles']]
            print(df2)
            print(level)

            # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            #     print(df2)

            # if i == 0:
            #     axes[j,i].text(0.8, 0.5, 'Level {}'.format(LEVELS_LABELS[j]),
            #         horizontalalignment='center',
            #         verticalalignment='center',
            #         transform=axes[j,i].transAxes,
            #         fontsize="xx-large"
            #     )
            #     axes[j,i].axis('off')


            sns.barplot(ax=axes[j,i], x="algorithm", y="mean_cpu_cycles", data=df2, palette=COLORS)
            axes[j,i].set_title(operations_names[i], fontsize="x-large")
            # axes[j,i].legend(loc='upper left')
            axes[j,i].tick_params(axis='x', rotation=90)
            axes[j,i].set(yscale="symlog")
            axes[j,i].set_xlabel('', fontsize="x-large")
            axes[j,i].set_ylabel('CPU Cycles', fontsize="x-large")
            # axes[j,i+1].axis('equal')

    figname = "{}/{}/cycles_level_commitment.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname, bbox_inches="tight")
    print("Saved file to {}".format(figname), flush=True)

def plot_speed_gake(data, config):

    fig, axes = plt.subplots(3,4, figsize=(25,25), dpi=200, sharey=True)
    fig.suptitle('GAKE operations', fontsize=30)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)

    LEVELS = [config["L1"], config["L3"], config["L5"]]
    LEVELS_LABELS = [1,3,5]

    def conditions(s):
        if (s['algorithm'] in (LEVELS[0])):
            return "Level 1"
        if (s['algorithm'] in (LEVELS[1])):
            return "Level 3"
        if (s['algorithm'] in (LEVELS[2])):
            return "Level 5"
        else:
            return ""

    data["level"] = data.apply(conditions, axis=1)

    operations = ['init', 'round12', 'round3', 'round4']
    operations_names = ['Init', 'Round 1-2', 'Round 3', 'Round 4']
    for (i, var) in enumerate(operations):
        for (j, level) in enumerate(LEVELS):
            df = data[(data['operation'] == var) & data['algorithm'].isin(level)]

            df2 = df[['algorithm','operation', 'mean_cpu_cycles']]
            print(df2)
            print(level)

            # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            #     print(df2)

            # if i == 0:
            #     axes[j,i].text(0.8, 0.5, 'Level {}'.format(LEVELS_LABELS[j]),
            #         horizontalalignment='center',
            #         verticalalignment='center',
            #         transform=axes[j,i].transAxes,
            #         fontsize="xx-large"
            #     )
            #     axes[j,i].axis('off')


            sns.barplot(ax=axes[j,i], x="algorithm", y="mean_cpu_cycles", data=df2, palette=COLORS)
            axes[j,i].set_title(operations_names[i], fontsize="x-large")
            # axes[j,i].legend(loc='upper left')
            axes[j,i].tick_params(axis='x', rotation=90)
            axes[j,i].set(yscale="symlog")
            axes[j,i].set_xlabel('', fontsize="x-large")
            axes[j,i].set_ylabel('CPU Cycles', fontsize="x-large")
            # axes[j,i+1].axis('equal')

    figname = "{}/{}/cycles_level_gake.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname, bbox_inches="tight")
    print("Saved file to {}".format(figname), flush=True)

def plot_speed_ake(data, config):

    fig, axes = plt.subplots(3,3, figsize=(25,25), dpi=200, sharey=True)
    fig.suptitle('AKE operations', fontsize=30)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)

    LEVELS = [config["L1"], config["L3"], config["L5"]]
    LEVELS_LABELS = [1,3,5]

    def conditions(s):
        if (s['algorithm'] in (LEVELS[0])):
            return "Level 1"
        if (s['algorithm'] in (LEVELS[1])):
            return "Level 3"
        if (s['algorithm'] in (LEVELS[2])):
            return "Level 5"
        else:
            return ""

    data["level"] = data.apply(conditions, axis=1)

    operations = ['init', 'algB', 'algA']
    operations_names = ['Init', 'AlgB', 'AlgA']
    for (i, var) in enumerate(operations):
        for (j, level) in enumerate(LEVELS):
            df = data[(data['operation'] == var) & data['algorithm'].isin(level)]

            df2 = df[['algorithm','operation', 'mean_cpu_cycles']]
            print(df2)
            print(level)

            # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            #     print(df2)

            # if i == 0:
            #     axes[j,i].text(0.8, 0.5, 'Level {}'.format(LEVELS_LABELS[j]),
            #         horizontalalignment='center',
            #         verticalalignment='center',
            #         transform=axes[j,i].transAxes,
            #         fontsize="xx-large"
            #     )
            #     axes[j,i].axis('off')

            sns.barplot(ax=axes[j,i], x="algorithm", y="mean_cpu_cycles", data=df2, palette=COLORS)
            axes[j,i].set_title(operations_names[i], fontsize="x-large")
            # axes[j,i].legend(loc='upper left')
            axes[j,i].tick_params(axis='x', rotation=90)
            axes[j,i].set(yscale="symlog")
            axes[j,i].set_xlabel('', fontsize="x-large")
            axes[j,i].set_ylabel('CPU Cycles', fontsize="x-large")
            # axes[j,i+1].axis('equal')

    figname = "{}/{}/cycles_level_ake.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname, bbox_inches="tight")
    print("Saved file to {}".format(figname), flush=True)

def plot_speed_kem(data, config):

    LEVELS = [config["L1"], config["L3"], config["L5"]]
    LEVELS_LABELS = [1,3,5]

    def conditions(s):
        if (s['algorithm'] in (LEVELS[0])):
            return "Level 1"
        if (s['algorithm'] in (LEVELS[1])):
            return "Level 3"
        if (s['algorithm'] in (LEVELS[2])):
            return "Level 5"
        else:
            return ""

    fig, axes = plt.subplots(3,3, figsize=(25,25), dpi=200, sharey=True)
    fig.suptitle('KEM operations', fontsize=30)
    fig.subplots_adjust(hspace=0.75, wspace=0.4)

    data["level"] = data.apply(conditions, axis=1)

    operations = ['keygen', 'encaps', 'decaps']
    operations_names = ['Key generation', 'Encapsulation', 'Decapsulation']
    for (i, var) in enumerate(operations):
        for (j, level) in enumerate(LEVELS):
            df = data[(data['operation'] == var) & data['algorithm'].isin(level)]

            df2 = df[['algorithm','operation', 'mean_cpu_cycles']]
            print(df2)
            print(level)

            # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            #     print(df2)

            # if i == 0:
            #     axes[j,i].text(0.8, 0.5, 'Level {}'.format(LEVELS_LABELS[j]),
            #         horizontalalignment='center',
            #         verticalalignment='center',
            #         transform=axes[j,i].transAxes,
            #         fontsize="xx-large"
            #     )
            #     axes[j,i].axis('off')


            sns.barplot(ax=axes[j,i], x="algorithm", y="mean_cpu_cycles", data=df2, palette=COLORS)
            axes[j,i].set_title(operations_names[i], fontsize="x-large")
            # axes[j,i].legend(loc='upper left')
            axes[j,i].tick_params(axis='x', rotation=90)
            axes[j,i].set(yscale="symlog")
            axes[j,i].set_xlabel('', fontsize="x-large")
            axes[j,i].set_ylabel('CPU Cycles', fontsize="x-large")
            # axes[j,i+1].axis('equal')

    figname = "{}/{}/cycles_level_kem.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
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

    ake_file = "{}/{}/ake.csv".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    if not Path(ake_file).is_file():
        print("File {} does NOT exist".format(ake_file), flush=True)
        sys.exit(1)

    kem_file = "{}/{}/kem.csv".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    if not Path(kem_file).is_file():
        print("File {} does NOT exist".format(kem_file), flush=True)
        sys.exit(1)

    gake_file = "{}/{}/gake.csv".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    if not Path(gake_file).is_file():
        print("File {} does NOT exist".format(gake_file), flush=True)
        sys.exit(1)

    commitment_file = "{}/{}/commitment.csv".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    if not Path(commitment_file).is_file():
        print("File {} does NOT exist".format(commitment_file), flush=True)
        sys.exit(1)

    data_ake = pd.read_csv(ake_file)
    data_kem = pd.read_csv(kem_file)
    data_gake = pd.read_csv(gake_file)
    data_commitment = pd.read_csv(commitment_file)

    data_concat = pd.concat([data_kem, data_commitment, data_ake])

    plot_speed_kem(data_kem, config)
    plot_speed_ake(data_ake, config)
    plot_speed_commitment(data_commitment, config)
    plot_speed_gake(data_gake, config)
    plot_heatmap(data_concat, config)
    plot_heatmap_level(data_concat, config)
    plot_scalability(data_gake, config)
    plot_scalability_level(data_gake, config)

if __name__ == '__main__':
    main()
