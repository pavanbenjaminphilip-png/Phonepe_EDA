import os
import json
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# --- Configuration ---
DB_USER = "root"
DB_PASSWORD = "pavan"
DB_HOST = "localhost"
DB_NAME = "phonepe_pulse"
PULSE_DATA_PATH = "c:/Users/rehan/Desktop/Project/pulse/data"

def extract_aggregated_transaction():
    path = f"{PULSE_DATA_PATH}/aggregated/transaction/country/india/state/"
    states = os.listdir(path)
    data = []
    for state in states:
        state_path = os.path.join(path, state)
        years = os.listdir(state_path)
        for year in years:
            year_path = os.path.join(state_path, year)
            files = os.listdir(year_path)
            for file in files:
                quarter = file.split(".")[0]
                with open(os.path.join(year_path, file), "r") as f:
                    json_data = json.load(f)
                    for i in json_data["data"]["transactionData"]:
                        name = i["name"]
                        count = i["paymentInstruments"][0]["count"]
                        amount = i["paymentInstruments"][0]["amount"]
                        data.append({
                            "State": state,
                            "Year": int(year),
                            "Quarter": int(quarter),
                            "Transaction_type": name,
                            "Transaction_count": count,
                            "Transaction_amount": amount
                        })
    return pd.DataFrame(data)

def extract_aggregated_user():
    path = f"{PULSE_DATA_PATH}/aggregated/user/country/india/state/"
    states = os.listdir(path)
    data = []
    for state in states:
        state_path = os.path.join(path, state)
        years = os.listdir(state_path)
        for year in years:
            year_path = os.path.join(state_path, year)
            files = os.listdir(year_path)
            for file in files:
                quarter = file.split(".")[0]
                with open(os.path.join(year_path, file), "r") as f:
                    json_data = json.load(f)
                    if json_data["data"]["usersByDevice"]:
                        for i in json_data["data"]["usersByDevice"]:
                            brand = i["brand"]
                            count = i["count"]
                            percentage = i["percentage"]
                            data.append({
                                "State": state,
                                "Year": int(year),
                                "Quarter": int(quarter),
                                "Brand": brand,
                                "Transaction_count": count,
                                "Percentage": percentage
                            })
    return pd.DataFrame(data)

def extract_aggregated_insurance():
    path = f"{PULSE_DATA_PATH}/aggregated/insurance/country/india/state/"
    states = os.listdir(path)
    data = []
    for state in states:
        state_path = os.path.join(path, state)
        years = os.listdir(state_path)
        for year in years:
            year_path = os.path.join(state_path, year)
            files = os.listdir(year_path)
            for file in files:
                quarter = file.split(".")[0]
                with open(os.path.join(year_path, file), "r") as f:
                    json_data = json.load(f)
                    if json_data["data"]["transactionData"]:
                        for i in json_data["data"]["transactionData"]:
                            name = i["name"]
                            count = i["paymentInstruments"][0]["count"]
                            amount = i["paymentInstruments"][0]["amount"]
                            data.append({
                                "State": state,
                                "Year": int(year),
                                "Quarter": int(quarter),
                                "Transaction_type": name,
                                "Transaction_count": count,
                                "Transaction_amount": amount
                            })
    return pd.DataFrame(data)

def extract_map_transaction():
    path = f"{PULSE_DATA_PATH}/map/transaction/hover/country/india/state/"
    states = os.listdir(path)
    data = []
    for state in states:
        state_path = os.path.join(path, state)
        years = os.listdir(state_path)
        for year in years:
            year_path = os.path.join(state_path, year)
            files = os.listdir(year_path)
            for file in files:
                quarter = file.split(".")[0]
                with open(os.path.join(year_path, file), "r") as f:
                    json_data = json.load(f)
                    for i in json_data["data"]["hoverDataList"]:
                        name = i["name"]
                        count = i["metric"][0]["count"]
                        amount = i["metric"][0]["amount"]
                        data.append({
                            "State": state,
                            "Year": int(year),
                            "Quarter": int(quarter),
                            "District": name,
                            "Count": count,
                            "Amount": amount
                        })
    return pd.DataFrame(data)

def extract_map_user():
    path = f"{PULSE_DATA_PATH}/map/user/hover/country/india/state/"
    states = os.listdir(path)
    data = []
    for state in states:
        state_path = os.path.join(path, state)
        years = os.listdir(state_path)
        for year in years:
            year_path = os.path.join(state_path, year)
            files = os.listdir(year_path)
            for file in files:
                quarter = file.split(".")[0]
                with open(os.path.join(year_path, file), "r") as f:
                    json_data = json.load(f)
                    if json_data["data"]["hoverData"]:
                        for district, info in json_data["data"]["hoverData"].items():
                            registered_users = info["registeredUsers"]
                            app_opens = info["appOpens"]
                            data.append({
                                "State": state,
                                "Year": int(year),
                                "Quarter": int(quarter),
                                "District": district,
                                "RegisteredUsers": registered_users,
                                "AppOpens": app_opens
                            })
    return pd.DataFrame(data)

def extract_map_insurance():
    path = f"{PULSE_DATA_PATH}/map/insurance/hover/country/india/state/"
    states = os.listdir(path)
    data = []
    for state in states:
        state_path = os.path.join(path, state)
        years = os.listdir(state_path)
        for year in years:
            year_path = os.path.join(state_path, year)
            files = os.listdir(year_path)
            for file in files:
                quarter = file.split(".")[0]
                with open(os.path.join(year_path, file), "r") as f:
                    json_data = json.load(f)
                    for i in json_data["data"]["hoverDataList"]:
                        name = i["name"]
                        count = i["metric"][0]["count"]
                        amount = i["metric"][0]["amount"]
                        data.append({
                            "State": state,
                            "Year": int(year),
                            "Quarter": int(quarter),
                            "District": name,
                            "Count": count,
                            "Amount": amount
                        })
    return pd.DataFrame(data)

def extract_top_transaction():
    path = f"{PULSE_DATA_PATH}/top/transaction/country/india/state/"
    states = os.listdir(path)
    data = []
    for state in states:
        state_path = os.path.join(path, state)
        years = os.listdir(state_path)
        for year in years:
            year_path = os.path.join(state_path, year)
            files = os.listdir(year_path)
            for file in files:
                quarter = file.split(".")[0]
                with open(os.path.join(year_path, file), "r") as f:
                    json_data = json.load(f)
                    for i in json_data["data"]["pincodes"]:
                        entity_name = i["entityName"]
                        count = i["metric"]["count"]
                        amount = i["metric"]["amount"]
                        data.append({
                            "State": state,
                            "Year": int(year),
                            "Quarter": int(quarter),
                            "Pincode": entity_name,
                            "Count": count,
                            "Amount": amount
                        })
    return pd.DataFrame(data)

def extract_top_user():
    path = f"{PULSE_DATA_PATH}/top/user/country/india/state/"
    states = os.listdir(path)
    data = []
    for state in states:
        state_path = os.path.join(path, state)
        years = os.listdir(state_path)
        for year in years:
            year_path = os.path.join(state_path, year)
            files = os.listdir(year_path)
            for file in files:
                quarter = file.split(".")[0]
                with open(os.path.join(year_path, file), "r") as f:
                    json_data = json.load(f)
                    for i in json_data["data"]["pincodes"]:
                        name = i["name"]
                        registered_users = i["registeredUsers"]
                        data.append({
                            "State": state,
                            "Year": int(year),
                            "Quarter": int(quarter),
                            "Pincode": name,
                            "RegisteredUsers": registered_users
                        })
    return pd.DataFrame(data)

def extract_top_insurance():
    path = f"{PULSE_DATA_PATH}/top/insurance/country/india/state/"
    states = os.listdir(path)
    data = []
    for state in states:
        state_path = os.path.join(path, state)
        years = os.listdir(state_path)
        for year in years:
            year_path = os.path.join(state_path, year)
            files = os.listdir(year_path)
            for file in files:
                quarter = file.split(".")[0]
                with open(os.path.join(year_path, file), "r") as f:
                    json_data = json.load(f)
                    for i in json_data["data"]["pincodes"]:
                        entity_name = i["entityName"]
                        count = i["metric"]["count"]
                        amount = i["metric"]["amount"]
                        data.append({
                            "State": state,
                            "Year": int(year),
                            "Quarter": int(quarter),
                            "Pincode": entity_name,
                            "Count": count,
                            "Amount": amount
                        })
    return pd.DataFrame(data)

def main():
    print("Extracting data...")
    df_agg_trans = extract_aggregated_transaction()
    df_agg_user = extract_aggregated_user()
    df_agg_ins = extract_aggregated_insurance()
    df_map_trans = extract_map_transaction()
    df_map_user = extract_map_user()
    df_map_ins = extract_map_insurance()
    df_top_trans = extract_top_transaction()
    df_top_user = extract_top_user()
    df_top_ins = extract_top_insurance()

    print("Data extraction complete.")

    # Create Database if it doesn't exist
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.close()

    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

    print("Loading data into SQL...")
    df_agg_trans.to_sql("aggregated_transaction", engine, if_exists="replace", index=False)
    df_agg_user.to_sql("aggregated_user", engine, if_exists="replace", index=False)
    df_agg_ins.to_sql("aggregated_insurance", engine, if_exists="replace", index=False)
    df_map_trans.to_sql("map_transaction", engine, if_exists="replace", index=False)
    df_map_user.to_sql("map_user", engine, if_exists="replace", index=False)
    df_map_ins.to_sql("map_insurance", engine, if_exists="replace", index=False)
    df_top_trans.to_sql("top_transaction", engine, if_exists="replace", index=False)
    df_top_user.to_sql("top_user", engine, if_exists="replace", index=False)
    df_top_ins.to_sql("top_insurance", engine, if_exists="replace", index=False)

    print("Data loading complete. 9 tables created.")

if __name__ == "__main__":
    main()
