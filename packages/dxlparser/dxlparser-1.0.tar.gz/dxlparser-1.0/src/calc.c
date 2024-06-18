#include "calc.h"
#include <stdio.h>

char* process_state(enum DXL_State state, void* obj, int objtype, char** ptr){
    char* ret = NULL; // Valor de retorno de una llamada a process_state
    switch (state){
        case DXL_State_Start:
            while ((**ptr) != 0){
                ret = process_state(DXL_State_Rule, obj, 0, ptr);
                if (ret != NULL) return ret;
            }
            break;
        case DXL_State_Rule:
            while (isspace(**ptr)) (*ptr)++;

            // Obtener tipo de usuario
            if (islower(**ptr)){
                struct DXL_Rule* rule_obj = (struct DXL_Rule*) calloc(1, sizeof(struct DXL_Rule));
                rule_obj->userclass = NULL;
                rule_obj->rule_expr = NULL;
                ret = process_state(DXL_State_UserClass, rule_obj, 0, ptr);
                if (ret == NULL){
                    // Obtener expresión
                    ret = process_state(DXL_State_Expr, rule_obj, 0, ptr);
                    if (ret == NULL){
                        Stack_Add(obj, rule_obj, 0);
                    } else return ret;
                } else return ret;
            } else {
                puts("Error: se esperaba UserClass");
                return (*ptr);
            }
            break;
        case DXL_State_UserClass:
            size_t tam_userclass = 0;
            char* cad_userclass = Cadena_Create();
            while ((**ptr) != ':' && !isspace(**ptr) && (**ptr) != 0){
                if (islower(**ptr))
                    cad_userclass = Cadena_Add(cad_userclass, (*ptr));
                else {
                    free(cad_userclass);
                    puts("Error: se esperaba minúscula en UserClass");
                    return (*ptr);
                }
                tam_userclass++;
                (*ptr)++;
                if (tam_userclass > 10){
                    free(cad_userclass);
                    puts("Error: UserClass es mayor de 10");
                    return (*ptr);
                }
            }
            while (isspace(**ptr)) (*ptr)++;
            if ((**ptr) == ':') (*ptr)++;
            if ((**ptr) == 0){
                puts("Error: fin de cadena no esperado, se esperaba ':' o minúscula");
                return (*ptr);
            }
            ((struct DXL_Rule*) (obj))->userclass = cad_userclass;
            break;
        case DXL_State_Expr:
            struct DXL_Expression* expr_obj = NULL;
            while (isspace(**ptr)) (*ptr)++;
            if (isdigit(**ptr)){
                expr_obj = (struct DXL_Expression*) calloc(1, sizeof(struct DXL_Expression));
                expr_obj->quantity = NULL;
                expr_obj->discounts = NULL;
                ret = process_state(DXL_State_Quantity, expr_obj, 0, ptr);
                if (ret == NULL){
                    //---Temporal: ~procesar~_ignorar_ condiciones
                    while ((**ptr) != ';' && (**ptr) != 0){
                        (*ptr)++;
                    }
                    if ((**ptr) == 0){
                        puts("Error: fin de cadena no esperado, se esperaba ;");
                    } else if ((**ptr) == ';'){
                        (*ptr)++;
                    }
                } else return ret;
            } else if ((**ptr) == 0){
                puts("Error: fin de cadena no esperado, se esperaba ;");
                return (*ptr);
            } else {
                puts("Error: se esperaba un número");
                return (*ptr);
            }
            ((struct DXL_Rule*) (obj))->rule_expr = expr_obj;
            break;
        case DXL_State_Quantity:
            struct Stack* ints = Stack_Create();
            struct Stack* decs = Stack_Create();
            char* d; //< Puntero para nuevos dígitos
            char tmp[2]; //< Para guardar temporalmente los dígitos
            bool isper = false; //< Bandera para saber si es un porcentaje

            // Leer valores
            while (isdigit(**ptr)){
                d = (char*) malloc(sizeof(char));
                tmp[0] = **ptr;
                tmp[1] = 0;
                //printf("Num: %s (%d)\n", tmp, tmp[0]);
                *d = (char) atoi(tmp);
                Stack_Add(ints, d, 0);
                (*ptr)++;
            }
            if ((**ptr) == '.'){
                // Tenemos decimales
                (*ptr)++;
                while (isdigit(**ptr)){
                    d = (char*) malloc(sizeof(char));
                    tmp[0] = **ptr;
                    tmp[1] = 0;
                    *d = (char) atoi(tmp);
                    Stack_Add(decs, d, 0);
                    (*ptr)++;
                }
                if ((**ptr) == 0){
                    puts("Error: fin de cadena no esperado, se esperaba número, %, o ;");
                    return (*ptr);
                } else if ((**ptr) == '%') isper = true;
                else if (!isspace(**ptr) && (**ptr) != ';'){
                    puts("Error: se esperaba ;");
                    return (*ptr);
                }
            } else if ((**ptr) == 0){
                puts("Error: fin de cadena no esperado, se esperaba número, %, o ;");
                return (*ptr);
            } else if ((**ptr) == '%') isper = true;
            else if (!isspace(**ptr) && (**ptr) != ';'){
                puts("Error: se esperaba ;");
                return (*ptr);
            }
            while (isspace(**ptr)) (*ptr)++;

            // Procesarlos
            struct DXL_Quantity* quantity_obj = (struct DXL_Quantity*) calloc(1, sizeof(struct DXL_Quantity));
            quantity_obj->value = 0;
            if (ret == NULL){
                quantity_obj->percentage = isper;

                // Obtener valor real
                size_t ints_size = Stack_Size(ints);
                for (size_t i=0; i<ints_size; i++){
                    char* digit = ((char**) ints->data)[ints_size-1-i];
                    quantity_obj->value += (*digit)*pow(10,i);
                    free(digit);
                }
                quantity_obj->value *= 100;
                size_t decs_size = Stack_Size(decs);
                if (decs_size >= 1) quantity_obj->value += (*(((char**) decs->data)[0]))*10;
                if (decs_size >= 2) quantity_obj->value += *(((char**) decs->data)[1]);

                ((struct DXL_Expression*) obj)->quantity = quantity_obj;
                ///---Temporal
                ((struct DXL_Expression*) obj)->discounts = NULL;
                ///---

                // Liberar memoria
                for (size_t i=2; i<decs_size; i++) free(((char**) (decs->data))[i]);
                Stack_Prune(ints);
                Stack_Prune(decs);
                free(ints);
                free(decs);
            }
            break;
        case DXL_State_CondExpr:
            break;
    }
    return NULL;
}

unsigned int calc_price(char* expr, char* date, unsigned int amount, unsigned int spent, char* userclass){
    char *ptr = expr; // Puntero para analisis
    struct Stack* userclasses = Stack_Create();

    // Valores para el grupo especificado...
    unsigned int price = 0; // ...si existe en la expresion
    unsigned int all = 0; // ...si no existe en la expresion, y existe all
    bool specified = false;

    // Analisis lexico-sintactico
    char* ret = process_state(DXL_State_Start, userclasses, 0, &ptr);
    if (ret != NULL){
        // Error
        return 1794; // FIX: para saber solamente si hubo errores
    }

    // Seleccionar operación
    for (size_t i=0; i<Stack_Size(userclasses); i++){
        char* userclass_r = ((struct DXL_Rule*) ((userclasses->data)[i]))->userclass;
        unsigned int val = ((struct DXL_Rule*) ((userclasses->data)[i]))->rule_expr->quantity->value;
        if (!strcmp(userclass_r, "all")){
            all = val;
        } else if (!strcmp(userclass_r, userclass)){
            //---Temporal: Calcular precio final, con los descuentos correspondientes
            price = val;
            specified = true;
            //---
            break;
        }
    }

    // Limpiar todo
    for (size_t i=0; i<Stack_Size(userclasses); i++){
        struct DXL_Rule* rule = (struct DXL_Rule*) ((userclasses->data)[i]);
        if (rule->userclass != NULL) free(rule->userclass);
        if (rule->rule_expr->quantity != NULL) free(rule->rule_expr->quantity);
        if (rule->rule_expr != NULL) free(rule->rule_expr);
    }
    Stack_Prune(userclasses);
    free(userclasses);

    return specified?price:all;
}
