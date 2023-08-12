import os
from datetime import datetime

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from OttAgent import *
from OttMap import *
from OttObject import *

OUTPUT_DIR = "output"
LENGTH = 60
WIDTH = 60
TASK_LENGTH = 120


def main():
    ott_map_type = OttCmdMap

    object_time_appearance_list = {
        OttCircleObject(
            name="Main-object",
            position=(LENGTH // 2, WIDTH // 2 + 10),
            radius=10,
            color="red",
            meaning=1,
            is_target=True,
        ): 0,
        OttDiagonalLineObject(
            name="Distracting-object",
            position=(0, 0),
            end=(min(LENGTH, WIDTH), min(LENGTH, WIDTH)),
            color="green",
            meaning=0.5,
            is_target=False,
        ): 50,
    }

    current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    out_dir_files = os.path.join(OUTPUT_DIR, f"{OUTPUT_DIR}_{current_date}")
    os.makedirs(out_dir_files, exist_ok=True)

    i = 0
    alpha_range = np.linspace(0.1, 5, 40)
    g_range = np.linspace(0.1, 5, 40)
    results_df = pd.DataFrame(columns=["alpha", "g", "p_of_steps_on_target", "number_of_alternations"])

    for alpha in alpha_range:
        for g in g_range:
            ott_map = ott_map_type(
                length=LENGTH,
                width=WIDTH,
                object_time_appearance_list=object_time_appearance_list,
            )

            agent = OttAgent(
                ott_map=ott_map,
                g=g,
                alpha=alpha,
                max_steps=TASK_LENGTH,
                starting_position=(30, 30),
            )

            agent.sim()

            number_of_alternations = agent.number_of_alternations
            total_step_spent_on_target = agent.total_step_spent_on_target
            total_steps = agent.max_steps
            p_of_steps_on_target = (total_step_spent_on_target / total_steps) * 100

            results_df.loc[i] = [alpha, g, p_of_steps_on_target, number_of_alternations]
            i += 1
            print(f"run {i} done out of {len(alpha_range) * len(g_range)}")

    plt_filename = os.path.join(out_dir_files, f"p_on_target_scatter_max_alpha_{alpha_range[-1]}.png")
    plot_data(results_df, plt_filename, color_by="p_of_steps_on_target", color_by_name="Percentage of Steps on Target")

    plt_filename = os.path.join(out_dir_files, f"number_of_alternations_max_alpha{alpha_range[-1]}.png")
    plot_data(results_df, plt_filename, color_by="number_of_alternations", color_by_name="Number of Alternations")

    csv_filename = os.path.join(out_dir_files, f"results_{current_date}.csv")
    results_df.to_csv(csv_filename, index=False)
    print("Results saved to", csv_filename)

    print("Done!")


def plot_data(results_df, file_name, color_by, color_by_name):
    plt.scatter(results_df["alpha"], results_df["g"], c=results_df[color_by], cmap="plasma")
    plt.colorbar(label=color_by_name)
    # plt.colorbar(label="Percentage of Steps on Target")
    plt.xlabel("Alpha")
    plt.ylabel("g")
    plt.title(f"{color_by_name} for Different Alpha and g Values")
    plt.grid()
    # plt_filename = os.path.join(out_dir_files, f"percentage_on_target_scatter_max_alpha_{alpha_range[-1]}.png")
    plt.savefig(file_name)
    plt.show()
    print("Scatter plot saved to", file_name)


if __name__ == "__main__":
    main()
