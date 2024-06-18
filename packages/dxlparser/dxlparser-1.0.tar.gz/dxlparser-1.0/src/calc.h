/*
 * @file calc.h
 * Contiene las funciones y objetos para calcular precios.
 */

#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

#include "cadena.h"
#include "stack.h"

#ifndef DXL_CALC
#define DXL_CALC

/*
 * Propiedades que se pueden comprobar dentro de una condicion
 */
enum DXL_Magnitude {
    DXL_Magnitude_Year = 1,
    DXL_Magnitude_Month,
    DXL_Magnitude_Day,
    DXL_Magnitude_Items,
    DXL_Magnitude_Spent
};

/*
 * Operadores disponibles
 */
enum DXL_Operator {
    // Para tipo de descuento
    DXL_Operator_Sum = 1,
    DXL_Operator_Sub,
    DXL_Operator_Mul,
    // Para condiciones multiples
    DXL_Operator_And,
    DXL_Operator_Or,
    // Para comparacion de valores
    DXL_Operator_Is,
    DXL_Operator_Greater,
    DXL_Operator_GreaterEqual,
    DXL_Operator_Lesser,
    DXL_Operator_LesserEqual,
    DXL_Operator_IsNot,
    // Para analisis lexico-sintactico
    DXL_Operator_LeftParen,
    DXL_Operator_RightParen
};

/*
 * Valor, numerico o porcentaje
 */
struct DXL_Quantity {
    unsigned int value;
    bool percentage;
};

/*
 * Condicion atomica
 */
struct DXL_AtomicCond {
    enum DXL_Magnitude* magnitude;
    enum DXL_Operator* operator;
    struct DXL_Quantity* quantity;
};

/*
 * Expresion de descuento
 */
struct DXL_Discount {
    enum DXL_Operator type;
    struct DXL_Quantity* quantity;
    struct Stack* condition;
};

/*
 * Expresion de una regla
 */
struct DXL_Expression {
    struct DXL_Quantity* quantity;
    struct DXL_Discount** discounts;
};

/*
 * Regla para un tipo de usuario
 */
struct DXL_Rule {
    char* userclass;
    struct DXL_Expression* rule_expr;
};

/*
 * Estado del analisis sintactico.
 */
enum DXL_State {
    DXL_State_Start = 1,
    DXL_State_Rule,
    DXL_State_UserClass,
    DXL_State_Expr,
    DXL_State_Quantity,
    DXL_State_CondExpr,
};

/*
 * Procesa un estado determinado del automata que procesa la expresion.
 *
 * @param state Estado a procesar.
 * @param obj Estructura a procesar en ese estado.
 * @param objtype Tipo de la estructura anterior.
 * @param ptr Puntero a la cadena a tratar.
 * @return NULL si la fase tuvo exito, puntero al caracter donde hubo un error en caso contrario.
 */
char* process_state(enum DXL_State state, void* obj, int objtype, char** ptr);

/*
 * Dados ciertos datos en una transaccion, calcula el precio de un elemento.
 *
 * @param expr Expresion DXL que contiene las reglas a ser analizadas.
 * @param date Fecha del sistema.
 * @param amount Numero de elementos en el carrito.
 * @param spent Cantidad, en centavos, ya procesada.
 * @param userclass Categoria del usuario.
 * @return un entero con el precio del producto, en centavos.
 */
unsigned int calc_price(char* expr, char* date, unsigned int amount, unsigned int spent, char* userclass);

#endif
