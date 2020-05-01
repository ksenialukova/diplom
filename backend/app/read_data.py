import pandas as pd


def return_entities():
    df = pd.read_csv('../../data/cash_entities/cash_entities.csv')
    return df
