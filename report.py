import pandas as pd
import os
import logging
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
    dataframes = [pd.read_excel(os.path.join(reports_folder, file)) for file in files]
    combined_df = pd.concat(dataframes, ignore_index=True)
    result = combined_df.groupby("Критерії", as_index=False)[
        ["К-сть де є CR", "К-сть де немає CR", "Загальна к-сть"]
    ].sum()
    return result

class DateFormatError(Exception):
    """Exception raised when a date format is incorrect."""
    pass


def parse_date(date):
    """
    Split date string "MM_YYYY-MM_YYYY" and return dict with date components.

    :param date: Date string in format "MM_YYYY-MM_YYYY", example, "01_2020-12_2020".
    :return: Dict with keys 'start_month', 'start_year', 'end_month', 'end_year'.
    :raises DateFormatError: If date format is invalid.
    """
    try:
        chunks = date.split("-")
        if len(chunks) != 2:
            raise DateFormatError

        start_date, end_date = chunks

        start_parts = start_date.split("_")
        end_parts = end_date.split("_")

        if len(start_parts) != 2 or len(end_parts) != 2:
            raise DateFormatError("Each date part must contains month and year, splited by dash")

        start_month, start_year = map(int, start_parts)
        end_month, end_year = map(int, end_parts)

        if not(start_month >= 1 or start_month >= 12):
            raise DateFormatError("Start month must be in range 1-12")
        if not(end_month >= 1 or end_month <= 12):
            raise DateFormatError("End month must be in range 1-12")
        if start_year > end_year or (start_year == end_year and start_month > end_month):
            raise DateFormatError("Start date must be before end date")

        return {
            "start_month": start_month,
            "start_year": start_year,
            "end_month": end_month,
            "end_year": end_year,
        }
    except (ValueError, IndexError) as e:
        raise DateFormatError("Cannot parse date, invalid format {date}") from e


def generate_report(settings = None):
    print("Generating report...")

    folder_path = os.path.dirname(os.path.realpath(__file__))

    reports_folder = os.path.join(folder_path, "reports")

    files = os.listdir(reports_folder)
    files = [file for file in files if file.endswith(".xlsx")]

    print("files:", files)

    # if settings:
    #     date = settings["date"]
    #     selected_regions = settings["selected_regions"]
    #     parsed_date = parse_date(date)
    #     files = search_files(files, selected_regions, parsed_date["start_month"], parsed_date["end_month"], parsed_date["start_year"], parsed_date["end_year"])
    #
    # if files:
    #     result = summ_files(files, reports_folder)
    #     current_date = datetime.now().strftime("%m_%d_%Y")
    #     result_file_name = f"dgidpl_report_summary_{current_date}.xlsx"
    #     result.to_excel(result_file_name, index=False)
    #     print(f"Файл з результатом збережений: {result_file_name}")


generate_report()