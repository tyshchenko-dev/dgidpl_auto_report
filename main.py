import pandas as pd
import os
from datetime import datetime

folder_path = os.path.dirname(os.path.realpath(__file__))

reports_folder = os.path.join(folder_path, "reports")

files = os.listdir(reports_folder)

dataframes = [pd.read_excel(os.path.join(reports_folder, file)) for file in files if file != ".DS_Store"]
combined_df = pd.concat(dataframes, ignore_index=True)

result = combined_df.groupby("Критерії", as_index=False)[
    ["К-сть де є CR", "К-сть де немає CR", "Загальна к-сть"]
].sum()

current_date = datetime.now().strftime("%m_%d_%Y")
result_file_name = f"dgidpl_report_summary_{current_date}.xlsx"

result.to_excel(result_file_name, index=False)

print(f"Файл з результатом збережений: {result_file_name}")
