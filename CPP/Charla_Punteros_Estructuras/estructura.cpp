#include <iostream>
using namespace std;

struct carro {
  string marca; string modelo;  int anio;
};

int main(){
    // Create a car structure and store it in myCar1;
    carro miCarro1;
    miCarro1.marca = "BMW";   miCarro1.modelo = "X5";    miCarro1.anio = 1999;

    // Create another car structure and store it in myCar2;
    carro miCarro2;
    miCarro2.marca = "Ford";  miCarro2.modelo = "Mustang";   miCarro2.anio = 1969;
    
    // Print the structure members
    cout << miCarro1.marca << " " << miCarro1.modelo << " " << miCarro1.anio << "\n";
    cout << miCarro2.marca << " " << miCarro2.modelo << " " << miCarro2.anio << "\n";
    
    return 0;
}