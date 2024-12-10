#include <iostream>
using namespace std;

int main(){
    string comida = "Pizza";
    string* ptr = &comida;

    cout << "Variable comida: "<< comida << "\n";
    cout << "Direccion ptr: " << ptr << "\n";
    cout << "Contenido *ptr: " << *ptr << "\n";
}