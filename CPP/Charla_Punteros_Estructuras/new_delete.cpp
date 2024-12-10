#include <iostream>
#include <vector>
using namespace std;

void uso_correcto(){
    int *p = NULL;
    p = new int;
    *p = 5;
    cout << "El valor del puntero p es " << *p << " y su direccion es " << p << "\n";
    delete p;
    cout << "La direccion de memoria p ha sido Liberada.\n";
}

void uso_incorrecto1(){
        int *p = NULL;
        p = new int;
        *p = 5;
        cout << "El valor del puntero p es " << *p << " y su direccion es " << p << "\n";
        delete p;        
        cout << "La direccion de memoria p ha sido Liberada.\n";
        cout << "El valor del puntero p es " << *p << " y su direccion es " << p << "\n";
        // *p = 4;
        // cout << "El valor del puntero p es " << *p << " y su direccion es " << p << "\n";
}

int* uso_correcto2(){        
        int *ptr = new int;
        *ptr = 4;
        cout << "El valor del puntero ptr es " << *ptr << " y su direccion es " << ptr << "\n";
        *ptr = 5;
        // return &p;  <- Error de compilacion
        return ptr;
}

int main(){

    cout << "Uso correcto:\n";
    uso_correcto();
    cout << "Uso incorrecto 1:\n";
    uso_incorrecto1();
    cout << "Uso correcto 2:\n";
    int *p = uso_correcto2();    
    cout << "El valor del puntero p es " << *p << " y su direccion es " << p << "\n";
    *p = 7;
    cout << "El valor del puntero p es " << *p << " y su direccion es " << p << "\n";
    delete p;
    cout << "La direccion del puntero fue liberada\n";
    cout << "El valor del puntero p es " << *p << " y su direccion es " << p << "\n";
    return 0;
}