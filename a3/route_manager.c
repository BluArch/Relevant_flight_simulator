/** @file route_manager.c
 *  @brief A small program to analyze airline routes data.
 *  @author Mike Z.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Jose O.
 *  @author Saasha J.
 *  @author Victoria L.
 *  @author JJ C.
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list.h"

#define MAX_LINE_LEN 1024

node_t *cycleYAML(char yamlFILE[50], int QUESTION, node_t *list);
FILE* createFile(char* filename);
void closeFile(FILE *file);
void outputCSV(node_t *list, int N, int question, FILE *writeTo);
void checkChar(char word[50]);
void releaseNodes(node_t *list);
// void getArgs(char *argv, char yamlFile[50], char QUESTION[50], char N[50]);
/**
 * @brief Serves as an incremental counter for navigating the list.
 *
 * @param p The pointer of the node to print.
 * @param arg The pointer of the index.
 *
 */
void inccounter(node_t *p, void *arg)
{
    int *ip = (int *)arg;
    (*ip)++;
}

/**
 * @brief Allows to print out the content of a node.
 *
 * @param p The pointer of the node to print.
 * @param arg The format of the string.
 *
 */
void print_node(node_t *p, void *arg)
{
    char *fmt = (char *)arg;
    printf(fmt, p->airline_name);
}

/**
 * @brief Allows to print each node in the list.
 *
 * @param l The first node in the list
 *
 */
void analysis(node_t *l)
{
    int len = 0;

    apply(l, inccounter, &len);
    printf("Number of words: %d\n", len);

    apply(l, print_node, "%s\n");
}

/**
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */
int main(int argc, char *argv[])
{
    FILE *writeTo = createFile("output.csv");
    node_t *list = NULL;

    char yamlFILE[50];
    char QUESTION[10];
    char N[10];

    sscanf(argv[1], "--DATA=%[^\t\n]", yamlFILE);
    sscanf(argv[2], "--QUESTION=%[^\t\n]", QUESTION);
    sscanf(argv[3], "--N=%[^\t\n]", N);

    int argN;
    int Q;
    sscanf(QUESTION, "%d", &Q);
    sscanf(N, "%d", &argN);
 
    list = cycleYAML(yamlFILE, Q, list);
    outputCSV(list, argN, Q, writeTo);
    releaseNodes(list);
    closeFile(writeTo);
    exit(0);
}

/**
 * Function: cycleYAML
 * -------------------
 * @brief Takes a given .yaml file and iterates through it line by line, nodes of each 'flight' are stored in nodes in a sorted list
 * 
 * @param yamlFILE The name of a given .yaml file
 * @param QUESTION A parameter that will determine how the list is sorted
 * @param list A list that will store the sorted nodes, whose values are obtained from yamlFILE
*/
node_t *cycleYAML(char yamlFILE[50], int QUESTION, node_t *list){
    FILE *readFrom = fopen(yamlFILE, "r");
    char *line = NULL;

    line = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
    int counter = 0;

    char airline_name[50];
    char airline_icao_unique_code[50];
    char to_airport_name[50];
    char to_airport_city[50];
    char to_airport_country[50];
    char to_airport_icao_unique_code[50];

    fgets(line, 1024, readFrom);
    while(fgets(line, 1024, readFrom)){
        counter++;

        if (counter == 1) sscanf(line, "%*[^:]: %[^\n]", airline_name);
        if (counter == 2) sscanf(line, "%*[^:]: %[^\n]", airline_icao_unique_code);
        if (counter == 9) sscanf(line, "%*[^:]: %[^\n]", to_airport_name);
        if (counter == 10) sscanf(line, "%*[^:]: %[^\n]", to_airport_city);
        if (counter == 11){
            sscanf(line, "%*[^:]: %[^\n]", to_airport_country);
            checkChar(to_airport_country);
        }
        if (counter == 12) sscanf(line, "%*[^:]: %[^\n]", to_airport_icao_unique_code);

        if(counter == 13){
            counter = 0;
            if (QUESTION == 1 && (strcmp(to_airport_country, "Canada") == 0)){
                list = searchList(list, new_node(airline_name, airline_icao_unique_code, to_airport_name, to_airport_city, to_airport_country, to_airport_icao_unique_code), 1);
            } else if (QUESTION == 2){
                list = searchList(list, new_node(airline_name, airline_icao_unique_code, to_airport_name, to_airport_city, to_airport_country, to_airport_icao_unique_code), 2);
            } else if (QUESTION == 3){
                list = searchList(list, new_node(airline_name, airline_icao_unique_code, to_airport_name, to_airport_city, to_airport_country, to_airport_icao_unique_code), 3);
            }
        }
    }
    free(line);
    return list;
}

/**
 * Function: createFile
 * --------------------
 * @brief Creates and open a file under a given filename
 * 
 * @param filename The name of the file to be opened
*/
FILE* createFile(char* filename){             
    FILE* writeTo = fopen(filename, "w");
    if(writeTo == NULL){
        printf("File open error %s", filename);
        exit(EXIT_FAILURE);
    }
    return writeTo;
}

/**
 * Function: closeFile
 * -------------------
 * @brief Closes a given file
 * 
 * @param file The file that will be closed
*/
void closeFile(FILE *file){                                  
    if (file!= NULL){
        fclose(file);
    }
}

/**
 * Function: checkChar
 * -------------------
 * @brief Checks if a given string contains apostrophes, removes them if true
 * 
 * @param word The string that will be checked
*/
void checkChar(char word[50]){
    int len = strlen(word);
    if(word[0] == '\''){
        for(int i = 0; i<len-3; i++){
            word[i] = word[i+2];
        }
        for(int i = 0; i<4; i++){
            word[len-i] = '\0';
        }
    }
}

/**
 * Function: outputCSV
 * -------------------
 * @brief Outputs the wanted node information into a given .csv file
 * 
 * @param list The list (pointer to the head node) where information will be taken from
 * @param N The number of nodes whose information we want in the .csv file
 * @param question The number of the question we are answering
 * @param writeTo The .csv we are writing our output to
*/
void outputCSV(node_t *list, int N, int question, FILE *writeTo){
    node_t *curr = NULL;
    int count = 0;
    fprintf(writeTo, "subject,statistic\n");

    for(curr = list; curr != NULL; curr = curr->next){
        if(count == N){
            break;
        }
        if(question == 1){
            fprintf(writeTo, "%s (%s),%d\n", curr->airline_name, curr->airline_icao_unique_code, curr->statistic);
        } else if (question == 2){
            fprintf(writeTo, "%s,%d\n", curr->to_airport_country, curr->statistic);
        } else if (question == 3){
            fprintf(writeTo, "\"%s (%s), %s, %s\",%d\n", curr->to_airport_name, curr->to_airport_icao_unique_code, curr->to_airport_city, curr->to_airport_country, curr->statistic);
        }
        count++;
    }
}

/**
 * Function: releaseNodes
 * ----------------------
 * @brief Free the emalloc space given to the nodes of list
 * 
 * @param list The list (pointer to the head node) whose nodes will be freed
*/
void releaseNodes(node_t *list){
    node_t *temp_n = NULL;
        for (; list != NULL; list = temp_n){
            temp_n = list->next;
            free(list->airline_name);
            free(list->airline_icao_unique_code);
            free(list->to_airport_name);
            free(list->to_airport_city);
            free(list->to_airport_country);
            free(list->to_airport_icao_unique_code);
            free(list);
        }
}