#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@author: rivera
@author: V00962128
"""
import yaml
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def main():
    args: dict = getArgs()                                                  # Get arguments from command line and store them as a dictionary
    airlines = getDataSet(args['AIRLINES'], 'airlines')                     # Get Dataframe from .yaml file
    airport = getDataSet(args['AIRPORTS'], 'airports')                      # ''
    routes = getDataSet(args['ROUTES'], 'routes')                           # ''
    results = findQuestion(args['QUESTION'], airlines, airport, routes)     # Get updated Dataframe based on the question number from command line
    toCSV(results, args['QUESTION'])                                        # Converts updated Dataframe into a .csv file
    if (args['GRAPH_TYPE'] == 'pie'):                                       # Converts updated Dataframe into a .pdf of either a pie chart or bar graph
        createPie(results, args['QUESTION'])
    else:
        createHist(results, args['QUESTION'])


def findQuestion(question_num: str, airlines: pd, airports: pd, routes: pd) -> pd:
    """
    Calls a function to get a dataframe with it's structure depending on the question number
    Returns Dataframe received from function call
    """
    if (question_num == 'q1'):
        result = topAirlines(airlines, airports, routes)
    elif(question_num == 'q2'):
        result = lowestCountries(airlines, airports, routes)
    elif(question_num == 'q3'):
        result = topDestinations(airlines, airports, routes)
    elif(question_num == 'q4'):
        result = topCities(airlines, airports, routes)
    else:
        result = altitudeDif(airlines, airports, routes)
    return result


def getDataSet(filename: str, title: str) -> pd:
    """
    Converts content of a .yaml file into a Dataframe
    """
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)[title]
    df = pd.json_normalize(data)
    return df


def getArgs() -> dict:
    """
    Returns the arguments from the commandline as a dictionary
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--AIRLINES')
    parser.add_argument('--AIRPORTS')
    parser.add_argument('--ROUTES')
    parser.add_argument('--QUESTION')
    parser.add_argument('--GRAPH_TYPE')

    args = parser.parse_args()
    args = vars(args)
    return args

def topAirlines(airlines: pd, airports: pd, routes: pd) -> pd:
    """
    Returns a DataFrame of 20 flights with the most destination country as 'Cananda'
    Dataframe is structured highest to lowest flight count
    """
    airlines.drop(['airline_country'], inplace=True, axis=1)
    airports.drop(['airport_altitude', 'airport_name', 'airport_icao_unique_code', 'airport_city'], inplace=True, axis=1)
    routes.drop(['route_from_aiport_id'], inplace=True, axis=1)

    routes.rename({'route_to_airport_id': 'airport_id', 'route_airline_id': 'airline_id'}, axis=1, inplace=True)
    airports = airports[airports['airport_country'] == 'Canada']

    merged_df: pd.DataFrame = airports.merge(routes, on='airport_id', how='inner')
    merged_df: pd.DataFrame = merged_df.merge(airlines, on='airline_id', how='inner')

    answer: pd.DataFrame = merged_df.groupby(by=['airline_name', 'airline_icao_unique_code'], as_index=False).size().sort_values(by=['size', 'airline_name'], ascending=[False,True]).head(20)
    answer.insert(0, 'airlines', answer['airline_name'] + ' (' + answer['airline_icao_unique_code'] + ')')
    answer.drop(['airline_name', 'airline_icao_unique_code'], axis=1, inplace=True)
    answer = answer.rename(columns={'airlines': 'subject', 'size': 'statistic'})
    return answer


def lowestCountries(airlines: pd, airports: pd, routes: pd) -> pd:
    """
    Returns a Dataframe of 20 countries whose airport_id appears the least as 'route_to_airport_id'
    Dataframe is structured lowest to highest
    """
    airports.drop(['airport_name', 'airport_city', 'airport_altitude'], inplace=True, axis=1)
    routes.drop(['route_from_aiport_id', 'route_airline_id'], inplace=True, axis=1)
    routes.rename({'route_to_airport_id': 'airport_id'}, axis=1, inplace=True)

    merged_df: pd.DataFrame = airports.merge(routes, on='airport_id', how='inner')  #Merge by destination airports with the same airport_id
    merged_df['airport_country'] = merged_df['airport_country'].str.lstrip()

    answer: pd.DataFrame = merged_df.groupby(by='airport_country', as_index=False).size().sort_values(by=['size', 'airport_country'], ascending=[True,True]).head(30)
    answer = answer.rename(columns={'airport_country': 'subject', 'size': 'statistic'})
    return answer


def topDestinations(airlines: pd, airports: pd, routes: pd) -> pd:
    """
    Returns a Dataframe of 10 airports whose airport_id appears the most as 'route_to_airport_id'
    Dataframe is structured highest to lowest
    """
    airports.drop(['airport_altitude'], inplace=True, axis=1)
    routes.drop(['route_from_aiport_id', 'route_airline_id'], inplace=True, axis=1)
    routes.rename({'route_to_airport_id': 'airport_id'}, axis=1, inplace=True)

    merged_df: pd.DataFrame = airports.merge(routes, on='airport_id', how='inner')  #Merge by destination airports with the same airport_id
    merged_df['airport_country'] = merged_df['airport_country'].str.lstrip()

    answer: pd.DataFrame = merged_df.groupby(by=['airport_name', 'airport_city', 'airport_country', 'airport_icao_unique_code'], as_index=False).size().sort_values(by='size', ascending=False).head(10)
    answer.insert(0, 'flights', answer['airport_name'] + ' (' + answer['airport_icao_unique_code'] + '), ' + answer['airport_city'] + ', ' + answer['airport_country'])
    answer.drop(['airport_name', 'airport_city', 'airport_country', 'airport_icao_unique_code'], axis=1, inplace=True)
    answer = answer.rename(columns={'flights': 'subject', 'size': 'statistic'})
    return answer


def topCities(airlines: pd, airports: pd, routes: pd) -> pd:
    """
    Returns a Dataframe of 15 cities whose airport_id appears the most as 'route_to_airport_id'
    Dataframe is structured highest to lowest
    """
    airports.drop(['airport_name', 'airport_altitude', 'airport_icao_unique_code'], inplace=True, axis=1)
    routes.drop(['route_from_aiport_id', 'route_airline_id'], inplace=True, axis=1)
    routes.rename({'route_to_airport_id': 'airport_id'}, axis=1, inplace=True)

    merged_df: pd.DataFrame = airports.merge(routes, on='airport_id', how='inner')  #Merge by destination airports with the same airport_id
    merged_df['airport_country'] = merged_df['airport_country'].str.lstrip()

    answer: pd.DataFrame = merged_df.groupby(by=['airport_city', 'airport_country'], as_index=False).size().sort_values(by='size', ascending=False).head(15)
    answer.insert(0, 'location', answer['airport_city'] + ', ' + answer['airport_country']) 
    answer.drop(['airport_city', 'airport_country'], axis=1, inplace=True)
    answer = answer.rename(columns={'location': 'subject', 'size':'statistic'})
    return answer


def altitudeDif(airlines: pd, airports: pd, routes: pd) -> pd:
    """
    Returns a Dataframe of 10 airport routes (icao_to - icao_from) with the biggest difference in airport alititudes
    Dataframe is structured biggest to smallest difference
    """
    routes.drop(['route_airline_id'], inplace=True, axis=1)
    airports.drop(['airport_name', 'airport_city'], inplace=True, axis=1)

    airports2 = airports.copy()
    airports.rename({'airport_id':'route_from_aiport_id', 'airport_icao_unique_code': 'airport_icao_from', 'airport_altitude': 'altitude_from'}, axis=1, inplace=True)  #Dataframe to have airport info of airports_from
    airports2.rename({'airport_id':'route_to_airport_id', 'airport_icao_unique_code': 'airport_icao_to', 'airport_altitude': 'altitude_to'}, axis=1, inplace=True)  #Dataframe to have airport info of airports_to
    
    merged_df: pd.DataFrame = routes.merge(airports, on='route_from_aiport_id', how='inner')
    merged_df = merged_df.merge(airports2, on='route_to_airport_id', how='inner')

    merged_df.drop_duplicates(subset=['airport_icao_from', 'airport_icao_to'], keep=False, inplace=True)                    # Deletes all columns that have the same destination or arrival airport, regardless of order
    merged_df = merged_df.loc[(merged_df['airport_country_x']=='Canada') & (merged_df['airport_country_y']=='Canada')]   
    
    merged_df['altitude_to'] = merged_df['altitude_to'].astype(float)
    merged_df['altitude_from'] = merged_df['altitude_from'].astype(float)
    merged_df['alt_dif'] = abs(merged_df['altitude_to'] - merged_df['altitude_from'])                                       # Calculates the difference of altitude heights

    df_sorted = merged_df.sort_values(by='alt_dif', ascending=False).sort_values(by='alt_dif', ascending=False).head(10)
    df_sorted.insert(0, 'flights', df_sorted['airport_icao_from'] + '-' + df_sorted['airport_icao_to']) 
    df_sorted.drop(['route_from_aiport_id', 'route_to_airport_id', 'airport_country_x', 'altitude_from', 'airport_country_y', 'altitude_to', 'airport_icao_from', 'airport_icao_to'], inplace=True, axis=1)
    answer = df_sorted.rename(columns={'flights': 'subject', 'alt_dif':'statistic'})
    return answer


def toCSV(results: pd, question: str):
    """
    Takes a Dataframe and converts it's content into a .csv
    CSV filename will be the question number
    """
    filename = question.lower() + '.csv'
    results.to_csv(filename, index=False)


def createPie(results: pd, question: str):
    """
    Takes a Dataframe and creates a pie chart
    Pie chart will be saved as a .pdf file with the filename being the question number
    """
    filename = question.lower() + '.pdf'
    plt.pie(results['statistic'], labels =results['subject'], autopct='%1.1f%%', pctdistance=0.9, textprops={'fontsize': 6})
    if(question == 'q1'):
        plt.title('Top 20 airlines with the most flights to Canada', fontsize=12)
    elif(question == 'q2'):
        plt.title('Lowest 30 countries for flight destinations', fontsize=12)
    elif(question == 'q3'):
        plt.title('Top 10 destination airports', fontsize=12)
    elif(question == 'q4'):
        plt.title('Top 15 destination cities', fontsize=12)
    else:
        plt.title('Top 10 unique flights in Canada with biggest altitude\n difference between to and from airports', fontsize=12)
    plt.savefig(filename, bbox_inches='tight')
    

def createHist(results: pd, question: str):
    """
    Takes a Dataframe and creates a bar graph
    Bar graph will be saved as a .pdf file with the filename being the question number
    """
    filename = question.lower() + '.pdf'
    plt.bar(results['subject'], results['statistic'])
    plt.xticks(results['subject'], rotation=90, fontsize=8)
    if(question == 'q1'):
        plt.title('Top 20 airlines with the most flights to Canada', fontsize=12)
        plt.xlabel('Airlines')
        plt.ylabel('Number of flights')
    elif(question == 'q2'):
        plt.title('Lowest 30 countries for flight destinations', fontsize=12)
        plt.xlabel('Countries')
        plt.ylabel('Number of flights to country')
    elif(question == 'q3'):
        plt.title('Top 10 destination airports', fontsize=12)
        plt.xlabel('Airports')
        plt.ylabel('Number of flights to airport')
    elif(question == 'q4'):
        plt.title('Top 15 destination cities', fontsize=12)
        plt.xlabel('Cities')
        plt.ylabel('Number of flights to city')
    else:
        plt.title('Top 10 unique flights in Canada with biggest altitude\n difference between departure and arrival airports', fontsize=12)
        plt.xlabel('Airport ID: Departure - Arrival')
        plt.ylabel('Difference in altitude(in meters)')
    plt.savefig(filename, bbox_inches='tight')


if __name__ == '__main__':
    main()
