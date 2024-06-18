#include <python3.12/Python.h>
#include <iostream>

class base {
public:
    static PyObject* add(PyObject* self, PyObject* args) {
        Py_ssize_t n = PyTuple_Size(args);
        float sum = 0.0f;
        PyObject* item;

        for (Py_ssize_t i = 0; i < n; i++) {
            item = PyTuple_GetItem(args, i);
            if (!PyNumber_Check(item)) {
                PyErr_SetString(PyExc_TypeError, "All arguments must be numbers.");
                return NULL;
            }
            sum += PyFloat_AsDouble(item);
        }
        return PyFloat_FromDouble(sum);
    }

    static PyObject* sub(PyObject* self, PyObject* args) {
        Py_ssize_t n = PyTuple_Size(args);
        if (n < 1) {
            PyErr_SetString(PyExc_TypeError, "Subtraction requires at least one argument.");
            return NULL;
        }

        PyObject* item = PyTuple_GetItem(args, 0);
        if (!PyNumber_Check(item)) {
            PyErr_SetString(PyExc_TypeError, "All arguments must be numbers.");
            return NULL;
        }
        float difference = PyFloat_AsDouble(item);

        for (Py_ssize_t i = 1; i < n; i++) {
            item = PyTuple_GetItem(args, i);
            if (!PyNumber_Check(item)) {
                PyErr_SetString(PyExc_TypeError, "All arguments must be numbers.");
                return NULL;
            }
            difference -= PyFloat_AsDouble(item);
        }
        return PyFloat_FromDouble(difference);
    }

    static PyObject* mul(PyObject* self, PyObject* args) {
        Py_ssize_t n = PyTuple_Size(args);
        if (n < 1) {
            PyErr_SetString(PyExc_TypeError, "Multiplication requires at least one argument.");
            return NULL;
        }

        float product = 1.0f;
        PyObject* item;

        for (Py_ssize_t i = 0; i < n; i++) {
            item = PyTuple_GetItem(args, i);
            if (!PyNumber_Check(item)) {
                PyErr_SetString(PyExc_TypeError, "All arguments must be numbers.");
                return NULL;
            }
            product *= PyFloat_AsDouble(item);
        }
        return PyFloat_FromDouble(product);
    }

    static PyObject* div(PyObject* self, PyObject* args) {
        PyObject *numerator, *denominator;
        if (!PyArg_ParseTuple(args, "OO", &numerator, &denominator)) {
            return NULL;
        }

        if (!PyNumber_Check(numerator) || !PyNumber_Check(denominator)) {
            PyErr_SetString(PyExc_TypeError, "Both argument must be numbers.");
            return NULL;
        }

        float num = static_cast<float>(PyFloat_AsDouble(numerator));
        float den = static_cast<float>(PyFloat_AsDouble(denominator));

        if (den == 0.0f) {
            PyErr_SetString(PyExc_ZeroDivisionError, "A division by zero is not allowed.");
            return NULL;
        }
        
        float result = num / den;
        return PyFloat_FromDouble(result);
    }
};

class equation {
public:
    static PyObject* linear(PyObject* self, PyObject* args) {
        float a, b, c;
        PyObject *aObj = NULL, *bObj = NULL, *cObj = NULL;

        if (!PyArg_ParseTuple(args, "|O!O!O!", &PyFloat_Type, &aObj, &PyFloat_Type, &bObj, &PyFloat_Type, &cObj)) {
            PyErr_SetString(PyExc_TypeError, "Arguments must be typ float and Only 2 arguments.");
            return NULL;
        }

        int provided = (aObj ? 1 : 0) + (bObj ? 1 : 0) + (cObj ? 1 : 0);
        if (provided != 2) {
            PyErr_SetString(PyExc_ValueError, "Only 2 Arguments are Provided");
            return NULL;
        }

        if (!aObj) {
            b = PyFloat_AsDouble(bObj);
            c = PyFloat_AsDouble(cObj);
            if (b == 0) {
                PyErr_SetString(PyExc_ZeroDivisionError, "B cant be 0 if you search a");
                return NULL;
            }
            a = (c - b) / b;
            return PyFloat_FromDouble(a);
        } else if (!bObj) {
            a = PyFloat_AsDouble(aObj);
            c = PyFloat_AsDouble(cObj);
            b = c - a;
            return PyFloat_FromDouble(b);
        } else if (!cObj) {
            a = PyFloat_AsDouble(aObj);
            b = PyFloat_AsDouble(bObj);
            c = a + b;
            return PyFloat_FromDouble(c);
        }

        PyErr_SetString(PyExc_RuntimeError, "Problem with arguments");
        return NULL;
    }
    
    static PyObject* quadratic(PyObject* self, PyObject* args) {
        float a, b, c;
        PyObject *aObj = NULL, *bObj = NULL, *cObj = NULL;

        if (!PyArg_ParseTuple(args, "O!O!O!", &PyFloat_Type, &aObj, &PyFloat_Type, &bObj, &PyFloat_Type, &cObj)) {
            PyErr_SetString(PyExc_TypeError, "Arguments must be from type float.");
            return NULL;
        }

        a = PyFloat_AsDouble(aObj);
        b = PyFloat_AsDouble(bObj);
        c = PyFloat_AsDouble(cObj);

        float discriminant = b * b - 4 * a * c;

        if (discriminant < 0) {
            PyErr_SetString(PyExc_ValueError, "No Real Roots.");
            return NULL;
        } else if (discriminant == 0) {
            float x = -b / (2 * a);
            return Py_BuildValue("(f)", x);
        } else {
            float x1 = (-b + sqrt(discriminant)) / (2 * a);
            float x2 = (-b - sqrt(discriminant)) / (2 * a);
            return Py_BuildValue("(ff)", x1, x2);
        }
    }

    static PyObject* pq(PyObject* self, PyObject* args) {
        float p, q;
        PyObject *pObj = NULL, *qObj = NULL;

        if (!PyArg_ParseTuple(args, "O!O!", &PyFloat_Type, &pObj, &PyFloat_Type, &qObj)) {
            PyErr_SetString(PyExc_TypeError, "All arguments must be have the type float.");
            return NULL;
        }

        p = PyFloat_AsDouble(pObj);
        q = PyFloat_AsDouble(qObj);

        float discriminant = (p / 2) * (p / 2) - q;

        if (discriminant < 0) {
            PyErr_SetString(PyExc_ValueError, "No Real Roots");
            return NULL;
        } else if (discriminant == 0) {
            float x = -p / 2;
            return Py_BuildValue("(f)", x);
        } else {
            float x1 = -p / 2 + sqrt(discriminant);
            float x2 = -p / 2 - sqrt(discriminant);
            return Py_BuildValue("(ff)", x1, x2);
        }
    }
};

static PyMethodDef base_methods[] = {
    {"add", base::add, METH_VARARGS, "add two or more numbers"},
    {"sub", base::sub, METH_VARARGS, "subtract two or more numbers"},
    {"mul", base::mul, METH_VARARGS, "multiply two or more numbers"},
    {"div", base::div, METH_VARARGS, "divide two numbers"},
    {NULL, NULL, 0, NULL}
};

static PyMethodDef equation_methods[] = {
    {"linear", equation::linear, METH_VARARGS, "solve a linear equation"},
    {"quadratic", equation::linear, METH_VARARGS, "solve a quadratic equation"},
    {NULL, NULL, 0, NULL}
};

static PyMethodDef pacflymath_methods[] = {
    {"add", base::add, METH_VARARGS, "add two or more numbers"},
    {"sub", base::sub, METH_VARARGS, "subtract two or more numbers"},
    {"mul", base::mul, METH_VARARGS, "multiply two or more numbers"},
    {"div", base::div, METH_VARARGS, "divide two numbers"},
    {"linear", equation::linear, METH_VARARGS, "solve a linear equation"},
    {"quadratic", equation::linear, METH_VARARGS, "solve a quadratic equation"},
    {"pq", equation::pq, METH_VARARGS, "solve a pq equation"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pacflymath = {
    PyModuleDef_HEAD_INIT,
    "pacflymath",
    "A Module for Math Operations",
    -1,
    pacflymath_methods
};

static PyObject* PyInit_pacflymath(void) {
    return PyModule_Create(&pacflymath);
}