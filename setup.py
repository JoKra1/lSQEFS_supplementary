import os

if __name__ == "__main__":

    try:
        os.makedirs("./results")
    except:
        print("Result directories already exist.")

    try:
        os.makedirs("./results/sim")
        os.makedirs("./results/data")
        os.makedirs("./results/plots")
    except:
        print("Result sub-directory already exist.")

    try:
        os.makedirs("./results/data/sim1_exp")
        os.makedirs("./results/data/sim1_gen")
        os.makedirs("./results/sim/sim1_exp")
        os.makedirs("./results/sim/sim1_gen")
    except:
        print("Sim 1 Result sub-directory already exist.")

    try:
        os.makedirs("./results/data/sim2_exp")
        os.makedirs("./results/data/sim2_gen")
        os.makedirs("./results/sim/sim2_exp")
        os.makedirs("./results/sim/sim2_gen")
    except:
        print("Sim 2 Result sub-directory already exist.")

    try:
        os.makedirs("./results/data/sim3_exp")
        os.makedirs("./results/data/sim3_gen")
        os.makedirs("./results/sim/sim3_exp")
        os.makedirs("./results/sim/sim3_gen")
    except:
        print("Sim 3 Result sub-directory already exist.")

    try:
        os.makedirs("./results/data/sim4_gen")
        os.makedirs("./results/sim/sim4_gen")
    except:
        print("Sim 4 Result sub-directory already exist.")

    try:
        os.makedirs("./results/data/sim5_gen")
        os.makedirs("./results/sim/sim5_gen")
    except:
        print("Sim 5 Result sub-directory already exist.")
