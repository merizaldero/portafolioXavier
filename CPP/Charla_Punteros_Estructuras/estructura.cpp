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

    carro* miCarro3 = new carro();
    (*miCarro3).marca = "Toyota";  miCarro3->modelo = "Prius";   miCarro3->anio = 2008;
    
    // Print the structure members
    cout << miCarro1.marca << " " << miCarro1.modelo << " " << miCarro1.anio << "\n";
    cout << miCarro2.marca << " " << miCarro2.modelo << " " << miCarro2.anio << "\n";
    cout << miCarro3->marca << " " << miCarro3->modelo << " " << miCarro3->anio << "\n";
    
    return 0;
}