#HW_lecture_6
import pandas as pd
import numpy as np
import scipy.stats as st
from statsmodels.stats.weightstats import ztest
from statsmodels.stats.multitest import multipletests as mpt

def check_intervals_intersect(first_ci, second_ci):
       first = st.t.interval(confidence=0.95,
              df=len(first_ci) - 1,
              loc=np.mean(first_ci),
              scale=st.sem(first_ci))
       second = st.t.interval(confidence=0.95,
              df=len(second_ci) - 1,
              loc=np.mean(second_ci),
              scale=st.sem(second_ci))
       are_intersect = second[0] <= first[1] <= second[1] or first[0] <= second[1] <= first[1]
       return are_intersect

def check_dge_with_ci(first_table, second_table):
    ci_test_results = []
    for a in first_table.columns[:-1].values:
        ci_test_results.append(check_intervals_intersect(
            first_table[a], second_table[a]))
    return ci_test_results

def check_dge_with_ztest(first_table, second_table):
    z_test_results = []
    z_test_pvalues = []
    for a in first_table.columns[:-1].values:
        test_val = ztest(first_table[a], second_table[a])
        z_test_pvalues.append(test_val[1])
        z_test_results.append(test_val[1] > 0.05)
    return [z_test_results, z_test_pvalues]

def check_dge_with_ztest_cor(p_values):
    z_test_results = []
    for a in p_values:
        z_test_results.append(a > 0.05)
    return z_test_results


def mean_differ(first_table, second_table):
    mean_diff = []
    for a in first_table.columns[:-1].values:
        mean_diff.append(np.mean(first_table[a])-np.mean(second_table[a]))
    return mean_diff

def create_table(first_cell_type_expressions_path, second_cell_type_expressions_path, save_results_table, method = None):
    first_table = pd.read_csv(f"{first_cell_type_expressions_path}", index_col=0)
    second_table = pd.read_csv(f"{second_cell_type_expressions_path}", index_col=0)
    ci_test_results = check_dge_with_ci(first_table, second_table)
    z_test = check_dge_with_ztest(first_table, second_table)
    mean_diff = mean_differ(first_table, second_table)
    results = {
        "ci_test_results": ci_test_results,
        "z_test_results": z_test[0],
        "z_test_pvalues": z_test[1],
        "mean_diff": mean_diff
    }
    if method:
        z_test_cor_p_val = mpt(z_test[1], method=method)[1]
        z_test_cor_res = check_dge_with_ztest_cor(z_test_cor_p_val)
        results["z_test_results"] = z_test_cor_res
        results["z_test_pvalues"] = z_test_cor_p_val
    df_results = pd.DataFrame(results)
    df_results.to_csv(f"{save_results_table}.csv")

if __name__ == "__main__":
    while True:
        print("Enter the path to the file with the first cell type")
        first = str(input())
        print("Enter the path to the file with the second cell type")
        second = str(input())
        print("Enter the path to the results")
        res = str(input())
        print("Enter the method for multiple comparisons")
        method = str(input())
        create_table(first, second, res, method)
        print("Congrats with results! Do you want to continue? y/n")
        command = str(input())
        command = command.lower()
        if command == "yes" or command == "y":
          pass
        else:
          print("bye)")
          break