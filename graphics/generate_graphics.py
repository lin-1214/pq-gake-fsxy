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

def plot_heatmap(data, config):

    df = data.copy()
    df["operation"] = data["type"].astype(str) + "-" + data["operation"].astype(str)
    df = df[['algorithm', 'operation', 'mean_cpu_cycles']]
    df['mean_cpu_cycles'] = np.log(df['mean_cpu_cycles'])
    df = df.pivot(index='operation', columns='algorithm', values='mean_cpu_cycles')
    print(df)
    fig, axes = plt.subplots(figsize=(25,25))
    fig.suptitle('Operations', fontsize=30)

    sns.heatmap(ax=axes, data=df)

    figname = "{}/{}/cycles_operations.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname)
    print("Saved file to {}".format(figname), flush=True)

def plot_speed_commitment(data, config):

    fig, axes = plt.subplots(3,4, figsize=(25,25))
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

            if i == 0:
                axes[j,i].text(0.8, 0.5, 'Level {}'.format(LEVELS_LABELS[j]),
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=axes[j,i].transAxes,
                    fontsize="xx-large"
                )
                axes[j,i].axis('off')


            sns.barplot(ax=axes[j,i+1], x="algorithm", y="mean_cpu_cycles", data=df2)
            axes[j,i+1].set_title(operations_names[i], fontsize="x-large")
            # axes[j,i+1].legend(loc='upper left')
            axes[j,i+1].tick_params(axis='x', rotation=90)
            axes[j,i+1].set(yscale="log")
            axes[j,i+1].set_xlabel('', fontsize="x-large")
            axes[j,i+1].set_ylabel('CPU Cycles', fontsize="x-large")
            # axes[j,i+1].axis('equal')

    figname = "{}/{}/cycles_level_commitment.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname)
    print("Saved file to {}".format(figname), flush=True)

def plot_speed_gake(data, config):

    fig, axes = plt.subplots(3,5, figsize=(25,25))
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

            if i == 0:
                axes[j,i].text(0.8, 0.5, 'Level {}'.format(LEVELS_LABELS[j]),
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=axes[j,i].transAxes,
                    fontsize="xx-large"
                )
                axes[j,i].axis('off')


            sns.barplot(ax=axes[j,i+1], x="algorithm", y="mean_cpu_cycles", data=df2)
            axes[j,i+1].set_title(operations_names[i], fontsize="x-large")
            # axes[j,i+1].legend(loc='upper left')
            axes[j,i+1].tick_params(axis='x', rotation=90)
            axes[j,i+1].set(yscale="log")
            axes[j,i+1].set_xlabel('', fontsize="x-large")
            axes[j,i+1].set_ylabel('CPU Cycles', fontsize="x-large")
            # axes[j,i+1].axis('equal')

    figname = "{}/{}/cycles_level_gake.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname)
    print("Saved file to {}".format(figname), flush=True)

def plot_speed_ake(data, config):

    fig, axes = plt.subplots(3,4, figsize=(25,25))
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

    operations = ['init', 'algA', 'algB']
    operations_names = ['Init', 'Alg A', 'Alg B']
    for (i, var) in enumerate(operations):
        for (j, level) in enumerate(LEVELS):
            df = data[(data['operation'] == var) & data['algorithm'].isin(level)]

            df2 = df[['algorithm','operation', 'mean_cpu_cycles']]
            print(df2)
            print(level)

            # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            #     print(df2)

            if i == 0:
                axes[j,i].text(0.8, 0.5, 'Level {}'.format(LEVELS_LABELS[j]),
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=axes[j,i].transAxes,
                    fontsize="xx-large"
                )
                axes[j,i].axis('off')


            sns.barplot(ax=axes[j,i+1], x="algorithm", y="mean_cpu_cycles", data=df2)
            axes[j,i+1].set_title(operations_names[i], fontsize="x-large")
            # axes[j,i+1].legend(loc='upper left')
            axes[j,i+1].tick_params(axis='x', rotation=90)
            axes[j,i+1].set(yscale="log")
            axes[j,i+1].set_xlabel('', fontsize="x-large")
            axes[j,i+1].set_ylabel('CPU Cycles', fontsize="x-large")
            # axes[j,i+1].axis('equal')

    figname = "{}/{}/cycles_level_ake.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname)
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

    fig, axes = plt.subplots(3,4, figsize=(25,25))
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

            if i == 0:
                axes[j,i].text(0.8, 0.5, 'Level {}'.format(LEVELS_LABELS[j]),
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=axes[j,i].transAxes,
                    fontsize="xx-large"
                )
                axes[j,i].axis('off')


            sns.barplot(ax=axes[j,i+1], x="algorithm", y="mean_cpu_cycles", data=df2)
            axes[j,i+1].set_title(operations_names[i], fontsize="x-large")
            # axes[j,i+1].legend(loc='upper left')
            axes[j,i+1].tick_params(axis='x', rotation=90)
            axes[j,i+1].set(yscale="log")
            axes[j,i+1].set_xlabel('', fontsize="x-large")
            axes[j,i+1].set_ylabel('CPU Cycles', fontsize="x-large")
            # axes[j,i+1].axis('equal')

    figname = "{}/{}/cycles_level_kem.png".format(config["FOLDER"], config["OUTPUT_FOLDER"])
    fig.savefig(figname)
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

    data_concat = pd.concat([data_ake, data_kem, data_commitment])

    # plot_total_time_by_time(data, config)
    # plot_total_time_by_round(data, config)
    # plot_speed_commitments(data_speed, config)
    # plot_speed_2_ake(data_speed, config)

    plot_speed_kem(data_kem, config)
    plot_speed_ake(data_ake, config)
    plot_speed_commitment(data_commitment, config)
    plot_speed_gake(data_gake, config)
    plot_heatmap(data_concat, config)

if __name__ == '__main__':
    main()
