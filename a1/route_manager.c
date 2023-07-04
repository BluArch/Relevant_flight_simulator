/** @file route_manager.c
 *  @brief A pipes & filters program that uses conditionals, loops, and string processing tools in C to process airline routes.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Jose O.
 *  @author Saasha J.
 *  @author Victoria L.
 *  @author STUDENT_NAME
 *
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * Function: main
 * --------------
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */

void getArgs(int argc, char *argv[], char holdArgs[200]);
void cycleCSV(int argc, char filename[100], char arguments[200], FILE* writeTo);
FILE *createFile(char* filename);
void closeFile(FILE *file);
void searchArguments(char curLine[1024], char arguments[200], int *counter, int numArgs);
void getChar(int index, char arguments[200], char holder[100]);
void findKeyword(int **counter, char targetChar[100], char parseLine[1024], int column);
void flightToFrom(char parseLine[1024], FILE *writeTo, int option);
void outputFlight(char parseLine[1024], FILE *writeTo, int boolean);


int main(int argc, char *argv[])
{   
    char csvFile[100];                                          //Holds csv file name
    sscanf(argv[1], "--DATA=%[^\t\n]", csvFile);                //Grabs csv filename
    FILE *writeTo = createFile("output.txt");                   //Creates file to write output to

    char strArgs[200];                                          //Holds a string of all the wanted flight arguments
    strArgs[0]='\0';

    getArgs(argc, argv, strArgs);                               //Concatenate arguments into one string
    cycleCSV(argc, csvFile, strArgs, writeTo);                  //Cycles through given csv file
    closeFile(writeTo);                                         //Closes output file
    exit(0);
}

void getArgs(int argc, char* argv[], char holdArgs[200]){
// Function will parse arguments from argv and place them 
// in holdArgs, values seperated by ",".
    char SRC_CITY[100];
    char SRC_COUNTRY[100];
    char DEST_CITY[100];
    char AIRLINE[100];
    char DEST_COUNTRY[100];

    for(int i=2; i<argc; i++) {                                  //Loop checks if argument has been parsed, adds to holdArgs if true
        if (sscanf(argv[i], "--SRC_CITY=%[^\t\n]", SRC_CITY)==1){
            strcat(holdArgs, SRC_CITY);
        } else if (sscanf(argv[i], "--SRC_COUNTRY=%[^\t\n]", SRC_COUNTRY)==1){
            strcat(holdArgs, SRC_COUNTRY);
        } else if (sscanf(argv[i], "--DEST_CITY=%[^\t\n]", DEST_CITY)==1){
            strcat(holdArgs, DEST_CITY);
        } else if(sscanf(argv[i], "--AIRLINE=%[^\t\n]", AIRLINE)==1){
            strcat(holdArgs, AIRLINE);
        } else if (sscanf(argv[i], "--DEST_COUNTRY=%[^\t\n]", DEST_COUNTRY)==1){
            strcat(holdArgs, DEST_COUNTRY);
        }
        if (i+1!=argc){
            strcat(holdArgs, ",");
        }
    }
}


void cycleCSV(int argc, char filename[100], char arguments[200], FILE *writeTo){
// Function checks line by line for wanted arguments, will send line to be output
// if line is a flight we are looking for.
    argc = argc-2;                                              //How many arguments were inputed

    FILE *readFrom = fopen(filename, "r");                      //Opens csv file to read from

    char buffer[1024];
    int counter = 0;                                            //Totals how many arguments are in the current line
    int numFlights= 0;                                          //Checks how many flights satisfy the given arguments
    int itCount= 0;                                             //Checks if the first flight has been found (will be either 1 or 0)

    while(fgets(buffer, 1024, readFrom))                        //Cycling through the csv file
    {                                                           
        searchArguments(buffer,arguments, &counter, argc);      //Find how many arguments are on current line

        if(counter == argc){                                    //All wanted variables are on the current line
            if(itCount == 0){                                   //Print ToFROM statement when first flight is found
                flightToFrom(buffer, writeTo, argc-1);
                itCount++;
            }
            if(argc==2){
                 outputFlight(buffer, writeTo, argc-1);
            }else if(argc==3){
                outputFlight(buffer, writeTo, argc-1);
            }else if(argc==4){
                outputFlight(buffer, writeTo, argc-1);
            }
            numFlights++;                                       //+1 flights found!
        }
        counter = 0;                                            //Resets number of found arguments on current line
    }
    if (numFlights == 0){                                       //If no flights
            outputFlight(buffer, writeTo, 0);                   
        }
    closeFile(readFrom);                                        //Close csv file
}


FILE* createFile(char* filename){             
//Creates a file.
    FILE* writeTo = fopen(filename, "w");
    if(writeTo == NULL){
        printf("File open error %s", filename);
        exit(EXIT_FAILURE);
    }
    return writeTo;
}


void closeFile(FILE *file){                   
//Closes a file.                  
    if (file!= NULL){
        fclose(file);
    }
}

void searchArguments(char curLine[1024], char arguments[200], int *counter, int numArgs){
// Function takes the current line of the csv file and searching for the given arguments.
// Counter will increase if argument is found
    char temp[100];      

    switch(numArgs){
        case 2: //For 2 arguments
            getChar(1, arguments, temp);
            findKeyword(&counter, temp, curLine, 2);
            getChar(2, arguments, temp);
            findKeyword(&counter, temp, curLine, 11);
            break;
        case 3: //For 3 arguments
            getChar(1, arguments, temp);
            findKeyword(&counter, temp, curLine, 6);
            getChar(2, arguments, temp);
            findKeyword(&counter, temp, curLine, 10);
            getChar(3, arguments, temp);
            findKeyword(&counter, temp, curLine, 11);
            break;
        case 4: //For 4 arguments
            getChar(1, arguments, temp);
            findKeyword(&counter, temp, curLine, 5);
            getChar(2, arguments, temp);
            findKeyword(&counter, temp, curLine, 6);
            getChar(3, arguments, temp);
            findKeyword(&counter, temp, curLine, 10);
            getChar(4, arguments, temp);
            findKeyword(&counter, temp, curLine, 11);
            break;
    }
}


void getChar(int index, char arguments[200], char holder[100]){
//Takes the argument at a specified index of 'arguments' and places it in holder.
    char tempArgs[200];
    strcpy(tempArgs, arguments);                   //Holds arguments string
    int count = 1;
    char *token;
    token = strtok(arguments, ",");

    while(token != NULL){                          //Parses until finding wanted token
        if (count == index){
            strcpy(holder, token);
            break;
        }
        token = strtok(NULL, ",");
        count++;
    }
    strcpy(arguments, tempArgs);                   //Restores original arguments string
}


void findKeyword(int **counter, char keyword[100], char parseLine[1024], int column){
//Checks if a keyword exists at a specified column of the given line.
    char tempLine[1024];
    strcpy(tempLine, parseLine);                   //Holds original line
    int columnComp = 1;                            //Compared to column when searching for keyword
    char *token;
    token = strtok(parseLine, ",");

    while(token!=NULL){
        if(columnComp == column){
            if(strcmp(token, keyword)==0){
                (**counter)++;
            }
        }
        columnComp++;
        token = strtok(NULL, ",");
    }
    strcpy(parseLine, tempLine);                   //Restores original line
}

void flightToFrom(char parseLine[1024], FILE *writeTo, int option){
// Prints the TO-FROM line to an output file.
    char AIRLINE[100];
    char AIRLINE_NAME[100];
    char SRC_CITY[100];
    char SRC_COUNTRY[100];
    char DEST_CITY[100];
    char DEST_COUNTRY[100];

    getChar(1, parseLine, AIRLINE_NAME);
    getChar(2, parseLine, AIRLINE);
    getChar(5, parseLine, SRC_CITY);
    getChar(6, parseLine, SRC_COUNTRY);
    getChar(10, parseLine, DEST_CITY);
    getChar(11, parseLine, DEST_COUNTRY);

    switch(option){
        case 1: //For 2 arguments
            fprintf(writeTo, "FLIGHTS TO %s BY %s (%s):\n", DEST_COUNTRY, AIRLINE_NAME, AIRLINE);
            break;
        case 2: //For 3 arguments
            fprintf(writeTo, "FLIGHTS FROM %s TO %s, %s:\n", SRC_COUNTRY, DEST_CITY, DEST_COUNTRY);
            break;
        case 3: //For 4 arguments 
            fprintf(writeTo, "FLIGHTS FROM %s, %s TO %s, %s:\n", SRC_CITY, SRC_COUNTRY, DEST_CITY, DEST_COUNTRY);
            break;
    }
}


void outputFlight(char parseLine[1024], FILE *writeTo, int cases){
// Prints the found flight to an output file.
    char AIRLINE[100];
    char AIRLINE_CODE[100];
    char AIRPORT_FROM[100];
    char ICAO_FROM[100];
    char CITY_FROM[100];
    char COUNTRY_FROM[100];
    char AIRPORT_TO[100];
    char ICAO_TO[100];
    char CITY_TO[100];
    char COUNTRY_TO[100];

    getChar(1, parseLine, AIRLINE);
    getChar(2, parseLine, AIRLINE_CODE);
    getChar(4, parseLine, AIRPORT_FROM);
    getChar(7, parseLine, ICAO_FROM);
    getChar(5, parseLine, CITY_FROM);
    getChar(6, parseLine, COUNTRY_FROM);
    getChar(9, parseLine, AIRPORT_TO);
    getChar(12, parseLine, ICAO_TO);
    getChar(10, parseLine, CITY_TO);
    getChar(11, parseLine, COUNTRY_TO);

    switch(cases){
        case 0: //No flights found
            fputs("NO RESULTS FOUND.\n", writeTo);
            break;
        case 1: //For 2 arguments
            fprintf(writeTo, "FROM: %s, %s, %s TO: %s (%s), %s\n", ICAO_FROM, CITY_FROM, COUNTRY_FROM, AIRPORT_TO, ICAO_TO, CITY_TO);
            break;
        case 2: //For 3 arguments
             fprintf(writeTo, "AIRLINE: %s (%s) ORIGIN: %s (%s), %s\n", AIRLINE, AIRLINE_CODE, AIRPORT_FROM, ICAO_FROM, CITY_FROM);
            break;
        case 3: //For 4 arguments
            fprintf(writeTo, "AIRLINE: %s (%s) ROUTE: %s-%s\n", AIRLINE, AIRLINE_CODE, ICAO_FROM, ICAO_TO);
            break;
    }
}
