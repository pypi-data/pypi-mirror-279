#include <Python.h>
#include "calc.h"

static PyObject *method_calc(PyObject *self, PyObject *args){
    char *expr, *date, *userclass = NULL;
    unsigned int amount;
    float spent;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "ssifs", &expr, &date, &amount, &spent, &userclass)){
        return NULL;
    }

    return PyLong_FromLong(calc_price(expr, date, amount, spent, userclass));
}

static PyMethodDef DxlMethods[] = {
    {"calc", method_calc, METH_VARARGS, "Calculates the price of a course based on some parameters."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef dxlmodule = {
    PyModuleDef_HEAD_INIT,
    "dxlparser",
    "Python interface for the DXL parser",
    -1,
    DxlMethods
};

PyMODINIT_FUNC PyInit_dxlparser(void) {
    return PyModule_Create(&dxlmodule);
}
