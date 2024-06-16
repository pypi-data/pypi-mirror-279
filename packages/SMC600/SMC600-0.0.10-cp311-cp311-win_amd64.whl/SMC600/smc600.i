%module smc600
%{
#include "smc600.h"
#include "LTSMC.h"
%}

%include "std_string.i"
%include "std_vector.i"
namespace std {
   %template(vectori) vector<int>;
   %template(vectord) vector<double>;
};

%include "cpointer.i"
%pointer_functions(double, doublep);
%pointer_functions(unsigned short, unsigned_short_p);

%include "smc600.h"
