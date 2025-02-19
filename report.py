import pandas as pd
import os
import logging
from datetime import datetime
import sys

class DateFormatError(Exception):
    """Exception raised when a date format is incorrect."""
    pass

def parse_from_filename(filename):
    """
    Split filename into region, month and year

    :param filename: String with name of the file, example: Київська_01_2025.xlsx

    :return: tuple (region, month_str, year_str)
    """

    try:
        parts = filename.split("_")

        if len(parts) != 3:
            raise ValueError(f"File {filename} has incorrect file format")

        region, month_str, year_str = parts
        year_str = year_str.replace(".xlsx", "").strip()
        region = region.strip()
        return (region, month_str, year_str)
    except ValueError:
        logging.error(f"File name {filename} has incorrect format")



def search_files(files, selected_regions, start_month, end_month, start_year, end_year):
    """
    Search and filter report files by date range and selected regions.
    The function filters a list of file paths based on the specified regions and date range.
    It expects file names to follow the format: <region>_<month>_<year>.xlsx.

    :param files: List of paths to report files.
    :param selected_regions: List of region names selected by the user.
    :param start_month: Selected start month (1-12).
    :param end_month: Selected end month (1-12).
    :param start_year: Selected start year (e.g., 2020).
    :param end_year: Selected end year (e.g., 2021).

    :return: List of filtered file paths that match the criteria.
    """

    filtered_files = []

    for file_path in files:
        try:
            (region, month_str, year_str) = parse_from_filename(file_path)

            if region not in selected_regions:
                continue

            file_month = int(month_str)
            file_year = int(year_str)

            if file_year >= start_year and file_year <= end_year and file_month >= start_month and file_month <= end_month:
                filtered_files.append(file_path)

        except ValueError:
            logging.error(f"File name {file_path} has incorrect format")
            continue

    return filtered_files


def summ_files(files, reports_folder):
    """
    Summarize report files by date range and selected regions.

    :param files: list of filenames in report folder
    :param reports_folder: string path to report folder
    :return: dataframe with summary
    """

    required_columns = ["Критерії", "К-сть де є CR", "К-сть де немає CR", "Загальна к-сть"]

    validated_dataframes = []

    for filename in files:
        full_path = os.path.join(reports_folder, filename)
        try:
            current_df = pd.read_excel(full_path)
            if not current_df.empty and set(required_columns).issubset(current_df.columns):
                validated_dataframes.append(current_df)
        except FileNotFoundError:
            logging.error(f"File {full_path} not found")
            continue
        except Exception as e:
            logging.error(f"Read file {full_path} error: {e}")
            continue


    combined_df = pd.concat(validated_dataframes, ignore_index=True)

    if not combined_df.empty:
        result = combined_df.groupby("Критерії", as_index=False)[
            ["К-сть де є CR", "К-сть де немає CR", "Загальна к-сть"]
        ].sum()

        return result
    else:
        return None



def parse_date_from_settings(date):
    """
    Split date string "MM_YYYY-MM_YYYY" and return dict with date components.

    :param date: String in format "MM_YYYY-MM_YYYY", example, "01_2020-12_2020".

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
        logging.error(f"Value error while parsing date '{date}': {e}")
        raise DateFormatError(f"Cannot parse date, invalid format {date}") from e


def generate_report(settings = None):
    logging.info(f"Generating report. Settings: {settings}")

    folder_path = os.path.dirname(os.path.realpath(__file__))

    reports_folder = os.path.join(folder_path, "reports")

    if not os.path.exists(reports_folder):
        logging.info(f"Folder {reports_folder} not found. Exiting.")
        sys.exit(0)

    files = os.listdir(reports_folder)
    files = [file for file in files if file.endswith(".xlsx")]

    if len(files) == 0:
        logging.info(f"No report files found in {reports_folder}")
        sys.exit(0)


    if settings:
        date = settings["date"]
        selected_regions = settings["selected_regions"]
        try:
            parsed_date = parse_date_from_settings(date)
        except DateFormatError as e:
            logging.error(e)
            sys.exit(0)
        files = search_files(files, selected_regions, parsed_date["start_month"], parsed_date["end_month"], parsed_date["start_year"], parsed_date["end_year"])

    if len(files) == 0:
        logging.info(f"No report files found in {reports_folder}")
        sys.exit(0)

    result = summ_files(files, reports_folder)
    if not result.empty:
        current_date = datetime.now().strftime("%m_%d_%Y")
        result_file_name = f"dgidpl_report_summary_{current_date}.xlsx"
        result.to_excel(result_file_name, index=False)
        logging.info(f"File with result saved: {result_file_name}")
    else:
        logging.info(f"Result is empty")
