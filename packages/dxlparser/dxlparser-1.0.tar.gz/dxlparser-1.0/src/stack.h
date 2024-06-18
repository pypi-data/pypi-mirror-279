
/**
 * @file stack.h
 * Funciones para manejar pilas dinámicas de punteros
 */

#ifndef DXL_STACK
#define DXL_STACK

#include <stddef.h>
#include <stdlib.h>

/*
 * Estructura para pila
 */
struct Stack {
    void** data;
    int* type;
    char* sentinel;
};

/**
 * Crea una pila vacia
 * @return Puntero a un array
 */
struct Stack* Stack_Create(void);

/**
 * Anade un elemento a la pila
 * @param stack Pila a modificar
 * @param item Puntero al elemento anadido
 * @param type Tipo/clase del elemento anadido
 * @return 0 si la tarea tuvo exito, 1 en otro caso
 */
int Stack_Add(struct Stack* stack, void* item, int type);

/**
 * Quita un elemento de la pila
 * @param stack Pila a modificar
 * @return 0 si la tarea tuvo exito, 1 en otro caso
 */
int Stack_Remove(struct Stack* stack);

/**
 * Cuenta el numero de elementos en la pila
 * @param stack Pila a contar
 * @return El tamano de la pila, en elementos
 */
size_t Stack_Size(struct Stack* stack);

/**
 * Prepara una pila para ser eliminada
 * @param stack Pila a eliminar
 */
void Stack_Prune(struct Stack* stack);

#endif
