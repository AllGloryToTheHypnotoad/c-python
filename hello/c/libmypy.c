#include <stdio.h>
#include <Python.h>
// #include "libmypy.h"
#include "add.h"

char hellofunc_docs[] = "Hello world description.";
char heymanfunc_docs[] = "Echo your name and passed number.";
// char addfunc_docs[] = "Add two numbers function.";

PyObject * hello(PyObject *);
PyObject * heyman(PyObject *, PyObject *);
PyObject * add(PyObject *, PyObject *);

PyMethodDef helloworld_funcs[] = {
  {  "hello",
    (PyCFunction)hello,
    METH_NOARGS,
    hellofunc_docs},
  {  "heyman",
    (PyCFunction)heyman,
    METH_VARARGS,
    heymanfunc_docs},
  {  "add",
    (PyCFunction)add,
    METH_VARARGS,
    addfunc_docs},

  {  NULL}
};

char helloworldmod_docs[] = "This is hello world module.";
char helloworldmod_name[] = "helloworld";

#if PY_MAJOR_VERSION >= 3

PyModuleDef helloworld_mod = {
  PyModuleDef_HEAD_INIT,
  helloworldmod_name,
  helloworldmod_docs,
  -1,
  helloworld_funcs,
  NULL,
  NULL,
  NULL,
  NULL
};

// this is right out of the docs
// https://docs.python.org/3/extending/extending.html

static PyObject *HelloError;

PyMODINIT_FUNC PyInit_helloworld(void) {
  PyObject *m;
  m = PyModule_Create(&helloworld_mod);

  if(m == NULL) return NULL;

  HelloError = PyErr_NewException("helloworld.error", NULL, NULL);
  Py_INCREF(HelloError);
  PyModule_AddObject(m, "error", HelloError);
  return m;
}

#else

void inithelloworld(void) {
  Py_InitModule3(helloworldmod_name, helloworld_funcs, helloworldmod_docs);
}

#endif


PyObject * hello(PyObject * self) {
  return PyUnicode_FromFormat("Hello C extension!");
}

PyObject * heyman(PyObject *self, PyObject *args) {
  int num;
  char *name;

  // is means int string
  if(!PyArg_ParseTuple(args, "is", &num, &name))
    return NULL;

  return PyUnicode_FromFormat("Hay %s!  You gave me %d.", name, num);
}

PyObject * add(PyObject *self, PyObject *args) {
  int num1, num2;
  char eq[20];

  // ii means int int
  if(!PyArg_ParseTuple(args, "ii", &num1, &num2))
    return NULL;

  sprintf(eq, "%d + %d", num1, num2);

  // return Py_BuildValue("is", num1 + num2, eq);
  return Py_BuildValue("is", cadd(num1, num2), eq);
}
