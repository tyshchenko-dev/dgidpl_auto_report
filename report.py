import pandas as pd
import os
from datetime import datetime


def search_files(files, selected_regions, start_month, end_month, start_year, end_year):
    filtered_files = []
    for file in files:
        parts = file.split("_")
        if len(parts) == 3:
            name, file_month, file_year = parts
            file_year = file_year.replace(".xlsx", "").strip()
            name = name.strip()
            if name in selected_regions:
                file_month = int(file_month)
                file_year = int(file_year)
                if file_year >= start_year and file_year <= end_year:
                    if file_month >= start_month and file_month <= end_month:
                        filtered_files.append(file)
    return filtered_files

def summ_files(files, reports_folder):
    dataframes = [pd.read_excel(os.path.join(reports_folder, file)) for file in files if file != ".DS_Store"]
    combined_df = pd.concat(dataframes, ignore_index=True)
    result = combined_df.groupby("Критерії", as_index=False)[
        ["К-сть де є CR", "К-сть де немає CR", "Загальна к-сть"]
    ].sum()
    return result

def parse_date(date):
    chunks = date.split("-")
    start_date = chunks[0]
    end_date = chunks[1]
    start_month = int(start_date.split("_")[0])
    start_year = int(start_date.split("_")[1])
    end_month = int(end_date.split("_")[0])
    end_year = int(end_date.split("_")[1])
    return {
        "start_month": start_month,
        "start_year": start_year,
        "end_month": end_month,
        "end_year": end_year,
    }

def generate_report(settings = None):
    print("Generating report...")

    folder_path = os.path.dirname(os.path.realpath(__file__))

    reports_folder = os.path.join(folder_path, "reports")

    files = os.listdir(reports_folder)

    if settings:
        date = settings["date"]
        selected_regions = settings["selected_regions"]
        print(selected_regions)
        parsed_date = parse_date(date)
        print(parsed_date)
        files = search_files(files, selected_regions, parsed_date["start_month"], parsed_date["end_month"], parsed_date["start_year"], parsed_date["end_year"])

    if files:
        result = summ_files(files, reports_folder)
        current_date = datetime.now().strftime("%m_%d_%Y")
        result_file_name = f"dgidpl_report_summary_{current_date}.xlsx"
        result.to_excel(result_file_name, index=False)
        print(f"Файл з результатом збережений: {result_file_name}")


generate_report()