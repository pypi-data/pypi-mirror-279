#include "stack.h"

struct Stack* Stack_Create(void){
    struct Stack* st = calloc(1, sizeof(struct Stack));
    if (st == NULL) return NULL;

    // Array de datos
    st->data = calloc(1, sizeof(void *));
    if (st->data == NULL){
        free(st);
        return NULL;
    }
    // Array de tipos
    st->type = calloc(1, sizeof(int));
    if (st->type == NULL){
        free(st->data);
        free(st);
        return NULL;
    }
    // Centinela
    st->sentinel = calloc(1, 1);
    if (st->sentinel == NULL){
        free(st->type);
        free(st->data);
        free(st);
        return NULL;
    }
    *(st->data) = st->sentinel;
    return st;
}

int Stack_Add(struct Stack* stack, void* item, int type){
    if (stack == NULL) return 1;
    size_t tam = Stack_Size(stack);
    void **data_n = realloc(stack->data, sizeof(void *)*(tam+2));
    if (data_n == NULL) return 2;
    data_n[tam] = item;
    data_n[tam+1] = stack->sentinel;
    stack->data = data_n;
    int* type_n = realloc(stack->type, sizeof(int)*(tam+2));
    if (type_n == NULL) return 3;
    type_n[tam] = type;
    stack->type = type_n;
    return 0;
}

int Stack_Remove(struct Stack* stack){
    if (stack == NULL) return 1;
    size_t tam = Stack_Size(stack);
    void** data_n = realloc(stack->data, sizeof(void *)*tam);
    if (data_n == NULL) return 2;
    data_n[tam-1] = stack->sentinel;
    stack->data = data_n;
    int* type_n = realloc(stack->type, sizeof(int)*tam);
    if (type_n == NULL) return 3;
    stack->type = type_n;
    return 0;
}

size_t Stack_Size(struct Stack* stack){
    size_t tam = 0;
    while (stack->data[tam] != stack->sentinel) tam++;
    return tam;
}

void Stack_Prune(struct Stack* stack){
    free(stack->data);
    free(stack->type);
    free(stack->sentinel);
    return;
}
